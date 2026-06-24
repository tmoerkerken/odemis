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
