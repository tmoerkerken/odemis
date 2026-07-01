# -*- coding: utf-8 -*-
"""
User-visible string constants shared across layout modules.

Centralising labels here makes them easy to update, translate, or reference
from tests without importing full layout classes.

Access as a namespace::

    from odemis.gui.layout import strings
    label = strings.BTN_CLOSE

:author: Delmic
:copyright: © Delmic

.. license::

    This file is part of Odemis.

    Odemis is free software: you can redistribute it and/or modify it under the
    terms of the GNU General Public License version 2 as published by the Free
    Software Foundation.

    Odemis is distributed in the hope that it will be useful, but WITHOUT ANY
    WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
    FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
    details.

    You should have received a copy of the GNU General Public License along with
    Odemis. If not, see http://www.gnu.org/licenses/.

"""

# ── Button labels ────────────────────────────────────────────────────────────
BTN_CLOSE = "Close"
BTN_REFINE = "Refine"

# ── Section / fold-panel labels ──────────────────────────────────────────────
LBL_STREAMS = "STREAMS"

# ── Dialog titles ────────────────────────────────────────────────────────────
TITLE_CORRELATION = "Multipoint Correlation"

# ── Status / info labels ─────────────────────────────────────────────────────
LBL_CORRELATION_RMS = "Correlation RMS Deviation :"

# ── CryoSECOM chamber panel ───────────────────────────────────────────────────
# Project section
LBL_PROJECT = "Project"
TXT_PROJECT_PATH_DEFAULT = "Select a destination file"
BTN_NEW_PROJECT = "New Project"
BTN_LOAD_PROJECT = "Load Project"

# Position section — names for positions not covered by odemis.acq.move.POSITION_NAMES
LBL_POSITION = "Position"
BTN_OPTICAL = "OPTICAL"
BTN_FIB = "FIB"
BTN_CANCEL = "Cancel"

# Advanced section
BTN_ADVANCED = "Advanced"
LBL_STAGE = "Stage"
LBL_RX_ANGLE = "RX Angle"
LBL_STEP_SIZE = "Step size"
BTN_FACTORY_ALIGNMENT = "FACTORY ALIGNMENT"

# Temperature section
LBL_TEMPERATURE = "Temperature"
LBL_SAMPLE_HEATER = "Sample heater"
LBL_TARGET_TEMPERATURE = "Target temperature"

# Log button
TOOLTIP_LOG = "Open log panel"

# ── FIBSEM tab ────────────────────────────────────────────────────────────────
# Fold-panel section headings
LBL_FEATURES = "FEATURES"
LBL_STAGE_POSITION = "STAGE POSITION"
LBL_OPTICAL_SETTINGS = "OPTICAL SETTINGS"
LBL_ACQUISITIONS = "ACQUISITIONS"
LBL_ACQUIRED = "ACQUIRED"
LBL_MILLING = "MILLING"
LBL_PATTERNS = "PATTERNS"

# Generic labels
LBL_STATUS = "Status"
LBL_FILENAME = "Filename"
LBL_MILLING_ANGLE = "Milling angle"
LBL_AUTO_SAVE = "Auto save acquisition"
LBL_ESTIMATED_TIME = "Estimated time ..."
LBL_VIEW_BTN = "view"

# Button labels
BTN_CREATE_MOVE = "Create / Move"
BTN_GO_TO_FEATURE = "Go to Feature"
BTN_SAVE_POSITION = "SAVE POSITION"
BTN_SEM_IMAGING = "SEM IMAGING"
BTN_MILLING = "MILLING"
BTN_ACQUIRE = "ACQUIRE"
BTN_CHANGE_FILE = "change\u2026"
BTN_ACQUIRE_BOTH = "ACQUIRE BOTH"
BTN_ACQUIRE_OVERVIEW = "ACQUIRE OVERVIEW"
BTN_CORRELATE_FIB_FM = "Correlate FIB/FM"
BTN_MILL = "MILL"
