import glob
import json
import logging
import os

from odemis import model
from odemis.util.dataio import data_to_static_streams, open_acquisition

# The current state of the feature
FEATURE_ACTIVE, FEATURE_ROUGH_MILLED, FEATURE_POLISHED, FEATURE_DEACTIVE = "Active", "Rough Milled", "Polished", "Discarded"


class CryoFeature(object):
    """
    Model class for a cryo interesting feature
    """

    def __init__(self, name, x, y, z, streams=None):
        """
        :param name: (string) the feature name
        :param x: (float) the X axis of the feature position
        :param y: (float) the Y axis of the feature position
        :param z: (float) the Z axis of the feature position
        :param streams: (List of StaticStream) list of acquired streams on this feature
        """
        self.name = model.StringVA(name)
        # The 3D position of an interesting point in the site (Typically, the milling should happen around that
        # volume, never touching it.)
        self.pos = model.TupleContinuous((x, y, z), range=((-1, -1, -1), (1, 1, 1)), cls=(int, float), unit="m")

        self.status = model.StringVA(FEATURE_ACTIVE)
        # TODO: Handle acquired files
        self.streams = streams if streams is not None else model.ListVA()


def get_features_dict(features):
    """
    Convert list of features to JSON serializable list of dict
    :param features: (list) list of CryoFeature
    :return: (dict) list of JSON serializable features
    """
    flist = []
    for feature in features:
        feature_item = {'name': feature.name.value, 'pos': feature.pos.value,
                        'status': feature.status.value}
        flist.append(feature_item)
    return {'feature_list': flist}


class FeaturesDecoder(json.JSONDecoder):
    """
    Json decoder for the CryoFeature class and its attributes
    """

    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, obj):
        # Either the object is the feature list or the feature objects inside it
        if 'name' in obj:
            pos = obj['pos']
            feature = CryoFeature(obj['name'], pos[0], pos[1], pos[2])
            feature.status.value = obj['status']
            return feature
        if 'feature_list' in obj:
            return obj['feature_list']


def save_features(project_dir, features):
    """
    Save the whole features list directly to the file
    :param project_dir: (string) directory to save the file to (typically project directory)
    :param features: (list of Features) all the features to serialize
    """
    filename = os.path.join(project_dir, "features.json")
    with open(filename, 'w') as jsonfile:
        json.dump(get_features_dict(features), jsonfile)


def read_features(project_dir):
    """
    Deserialize and return the features list from the json file
    :param project_dir: (string) directory to read the file from (typically project directory)
    :return: (list of CryoFeature) list of deserialized featuers
    """
    filename = os.path.join(project_dir, "features.json")
    if not os.path.exists(filename):
        raise ValueError(f"Features file doesn't exists in this location. {filename}")
    with open(filename, 'r') as jsonfile:
        return json.load(jsonfile, cls=FeaturesDecoder)

def load_project_data(path: str) -> dict:
    """load meteor project data from a directory:
    :param path (str): path to the project directory
    :return (dict): dictionary containing the loaded data (features and overviews)
    """

    # load overview images
    overview_filenames = glob.glob(os.path.join(path, "*overview*.ome.tiff"))
    overview_data = []
    for fname in overview_filenames:
        # note: we only load the overview data, as the conversion to streams
        # is done in the localisation_tab.add_overview_data which also
        # handles assigning the streams throughout the gui
        overview_data.extend(open_acquisition(fname))

    features = []
    try:
        # read features
        features = read_features(path)
    except ValueError:
        logging.warning("No features.json file found in the project directory.")

    # load feature streams
    for f in features:
        # search dir for images matching f.name.value
        stream_filenames = glob.glob(os.path.join(path, f"*{f.name.value}*.ome.tiff"))
        for fname in stream_filenames:
            f.streams.value.extend(data_to_static_streams(open_acquisition(fname)))

    return {"overviews": overview_data, "features": features}
