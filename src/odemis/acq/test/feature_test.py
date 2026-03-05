# -*- coding: utf-8 -*-
"""
Created on Oct 2021

Copyright © Delmic

This file is part of Odemis.

Odemis is free software: you can redistribute it and/or modify it under the terms
of the GNU General Public License version 2 as published by the Free Software
Foundation.

Odemis is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
Odemis. If not, see http://www.gnu.org/licenses/.
"""

import json
import logging
import os
import random
import shutil
import tempfile
import unittest

import numpy

from odemis import model
from odemis.acq.feature import (
    CryoFeature,
    FeaturesDecoder,
    get_features_dict,
    read_features,
    save_features,
    load_milling_tasks,
    FEATURE_READY_TO_MILL,
    MILLING,
    REFERENCE_IMAGE_FILENAME,
    is_stream_removed,
    mark_stream_as_removed,
)
from odemis.acq.milling import DEFAULT_MILLING_TASKS_PATH

logging.getLogger().setLevel(logging.DEBUG)

# store the test-features as json for easier editting
TEST_FEATURES_PATH = os.path.join(os.path.dirname(__file__), "test-features.json")
with open(TEST_FEATURES_PATH, "r") as f:
    TEST_FEATURES_STR = f.read()

class TestFeatureEncoderDecoder(unittest.TestCase):
    """
    Test the json encoder and decoder of the CryoFeature class
    """
    path = ""

    def tearDown(self):
        if os.path.exists(self.path):
            filename = os.path.join(self.path, f"TestFeature-1-{REFERENCE_IMAGE_FILENAME}")
            if os.path.exists(filename):
                os.remove(filename)
            os.rmdir(self.path)

    def test_feature_encoder(self):
        feature1 = CryoFeature("Feature-1", stage_position={"x": 0, "y": 0, "z": 0}, fm_focus_position={"z": 0})
        feature2 = CryoFeature("Feature-2", stage_position={"x": 1e-3, "y": 1e-3, "z": 1e-3}, fm_focus_position={"z": 2e-3})
        feature1.milling_tasks = {}
        feature2.milling_tasks = {}
        features = [feature1, feature2]
        json_str = json.dumps(get_features_dict(features))
        self.assertEqual(json_str, TEST_FEATURES_STR)

    def test_feature_decoder(self):
        features = json.loads(TEST_FEATURES_STR, cls=FeaturesDecoder)
        self.assertEqual(len(features), 2)
        self.assertEqual(features[0].name.value, "Feature-1")
        self.assertEqual(features[0].status.value, "Active")
        self.assertEqual(features[1].stage_position.value, {"x": 1e-3, "y": 1e-3, "z": 1e-3})
        self.assertEqual(features[1].fm_focus_position.value, {"z": 2e-3})

    def test_save_read_features(self):
        feature1 = CryoFeature("Feature-1", stage_position={"x": 0, "y": 0, "z": 0}, fm_focus_position={"z": 0})
        feature2 = CryoFeature("Feature-2", stage_position={"x": 1e-3, "y": 1e-3, "z": 1e-3}, fm_focus_position={"z": 2e-3})

        features = [feature1, feature2]
        save_features("", features)
        r_features = read_features("")
        self.assertEqual(len(features), len(r_features))
        self.assertEqual(features[0].name.value, r_features[0].name.value)

    def test_feature_milling_tasks(self):
        feature = CryoFeature(
            name="TestFeature-1",
            stage_position={"x": 50e-6, "y": 25e-6, "z": 32e-3, "rx": 0.61, "rz": 0},
            fm_focus_position={"z": 1.69e-3}
        )
        stage_position = {"x": 25e-6, "y": 40e-6, "z": 32e-3, "rx": 0.31, "rz": 0}
        self.path = os.path.join(os.getcwd(), feature.name.value)
        reference_image = model.DataArray(numpy.zeros(shape=(1024, 1536)), metadata={})
        milling_tasks = load_milling_tasks(DEFAULT_MILLING_TASKS_PATH)

        # randomly remove some milling tasks (to simulate user choice)
        task_name = random.choice(list(milling_tasks.keys()))
        del milling_tasks[task_name]

        # save milling task data
        feature.save_milling_task_data(
            stage_position=stage_position,
            path=self.path,
            reference_image=reference_image,
            milling_tasks=milling_tasks
        )

        self.assertEqual(feature.path, self.path)
        self.assertEqual(feature.reference_image.shape, reference_image.shape)
        self.assertEqual(feature.get_posture_position(MILLING), stage_position)
        self.assertEqual(feature.status.value, FEATURE_READY_TO_MILL)
        self.assertEqual(set(feature.milling_tasks.keys()), set(milling_tasks.keys()))

        # assert directory and file is created
        self.assertTrue(os.path.exists(feature.path))

        filename = os.path.join(feature.path, f"{feature.name.value}-{REFERENCE_IMAGE_FILENAME}")
        self.assertTrue(os.path.exists(filename))


class TestStreamRemovalRegistry(unittest.TestCase):
    """
    Test the stream removal registry functions
    """

    def setUp(self):
        """
        Create a temporary directory for testing
        """
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        """
        Clean up temporary directory
        """
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_mark_stream_as_removed(self) -> None:
        """
        Test marking a stream as removed and verifying the registry is created
        """
        stream_file = os.path.join(self.test_dir, "test-feature-Active-001.tif")

        # Mark stream as removed
        mark_stream_as_removed(self.test_dir, stream_file)

        # Verify registry file was created
        registry_path = os.path.join(self.test_dir, "removed_streams.json")
        self.assertTrue(os.path.exists(registry_path))

        # Verify registry contains the stream
        with open(registry_path, "r") as f:
            registry = json.load(f)
        self.assertIn("test-feature-Active-001", registry)
        self.assertIn("filepath", registry["test-feature-Active-001"])
        self.assertIn("timestamp", registry["test-feature-Active-001"])

    def test_is_stream_removed(self) -> None:
        """
        Test checking if a stream is marked as removed
        """
        stream_file = os.path.join(self.test_dir, "test-feature-Active-001.tif")

        # Initially, stream should not be marked as removed
        self.assertFalse(is_stream_removed(self.test_dir, stream_file))

        # Mark stream as removed
        mark_stream_as_removed(self.test_dir, stream_file)

        # Now it should be marked as removed
        self.assertTrue(is_stream_removed(self.test_dir, stream_file))

    def test_is_stream_removed_multiple_streams(self) -> None:
        """
        Test that removing one stream doesn't affect others
        """
        stream_file1 = os.path.join(self.test_dir, "test-feature-Active-001.tif")
        stream_file2 = os.path.join(self.test_dir, "test-feature-Active-002.tif")

        # Mark only the first stream as removed
        mark_stream_as_removed(self.test_dir, stream_file1)

        # Verify only the first is removed
        self.assertTrue(is_stream_removed(self.test_dir, stream_file1))
        self.assertFalse(is_stream_removed(self.test_dir, stream_file2))

        # Mark the second one
        mark_stream_as_removed(self.test_dir, stream_file2)

        # Now both should be marked as removed
        self.assertTrue(is_stream_removed(self.test_dir, stream_file1))
        self.assertTrue(is_stream_removed(self.test_dir, stream_file2))

    def test_is_stream_removed_with_empty_path(self) -> None:
        """
        Test that empty project path is handled gracefully
        """
        self.assertFalse(is_stream_removed("", "some_file.tif"))
        self.assertFalse(is_stream_removed(None, "some_file.tif"))

    def test_is_stream_removed_nonexistent_registry(self) -> None:
        """
        Test that checking a stream when registry doesn't exist returns False
        """
        stream_file = os.path.join(self.test_dir, "nonexistent.tif")
        # Registry file doesn't exist yet
        self.assertFalse(os.path.exists(os.path.join(self.test_dir, "removed_streams.json")))

        # Should return False without error
        self.assertFalse(is_stream_removed(self.test_dir, stream_file))

    def test_mark_stream_with_empty_path(self) -> None:
        """
        Test that marking with empty path is handled gracefully
        """
        # Should not raise an error
        mark_stream_as_removed("", "some_file.tif")
        mark_stream_as_removed(None, "some_file.tif")

        # Registry should not be created for empty path
        self.assertFalse(os.path.exists(os.path.join("", "removed_streams.json")))

    def test_stream_removal_persists_across_loads(self) -> None:
        """
        Test the core workflow: mark stream as removed, then load streams again
        and verify the removed stream is not loaded
        """
        from odemis.util.dataio import data_to_static_streams
        from odemis.acq.stream import StaticSEMStream

        # Create a feature
        feature = CryoFeature("TestFeature", stage_position={"x": 0, "y": 0, "z": 0}, 
                             fm_focus_position={"z": 0})
        
        # Create mock stream files (empty TIFF data)
        stream_file1 = os.path.join(self.test_dir, "test-TestFeature-001.tif")
        stream_file2 = os.path.join(self.test_dir, "test-TestFeature-002.tif")
        
        # Create minimal TIFF files with proper metadata
        import tifffile
        data1 = numpy.zeros((512, 512), dtype=numpy.uint8)
        data2 = numpy.ones((512, 512), dtype=numpy.uint8)
        
        # Create tiff files with OME metadata
        tifffile.imwrite(stream_file1, data1, metadata={"MD_POS": (0, 0)})
        tifffile.imwrite(stream_file2, data2, metadata={"MD_POS": (1e-3, 1e-3)})
        
        # Verify files were created
        self.assertTrue(os.path.exists(stream_file1))
        self.assertTrue(os.path.exists(stream_file2))
        
        # Load streams initially - both should load
        from odemis.acq.feature import load_feature_streams_from_disk
        load_feature_streams_from_disk(feature, self.test_dir)
        initial_stream_count = len(feature.streams.value)
        self.assertEqual(initial_stream_count, 2, "Should have loaded 2 streams initially")
        
        # Clear streams for next test
        feature.streams.value.clear()
        
        # Mark the first stream as removed
        mark_stream_as_removed(self.test_dir, stream_file1)
        
        # Load streams again - only the second one should load
        load_feature_streams_from_disk(feature, self.test_dir)
        final_stream_count = len(feature.streams.value)
        self.assertEqual(final_stream_count, 1, "Should have loaded only 1 stream after removal")
        
        # Verify that the remaining stream is the one we wanted to keep
        self.assertTrue(is_stream_removed(self.test_dir, stream_file1))
        self.assertFalse(is_stream_removed(self.test_dir, stream_file2))


if __name__ == "__main__":
    unittest.main()
