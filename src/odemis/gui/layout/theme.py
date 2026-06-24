# -*- coding: utf-8 -*-
"""
Theme definitions for layout modules.

A Theme groups all colour and font-size values that a layout module needs.
Layout classes accept an optional theme parameter so the visual style can be
changed at instantiation time without touching layout code.

Usage::

    from odemis.gui.layout.theme import DARK
    dialog = FrCorrelation(parent, theme=DARK)

To switch to a different theme, define another Theme instance and pass it in.

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

from dataclasses import dataclass

from odemis import gui


@dataclass(frozen=True)
class Theme:
    """
    Immutable collection of colour and font-size values for a GUI layout.

    All colour fields are CSS hex strings (e.g. "#333333") so this class
    carries no wx dependency and can be imported freely.

    Attributes
    ----------
    bg_base : str
        Pure-black background for the dialog chrome and viewport canvases.
    bg_main : str
        Primary panel background (sidebars, scrolled panes, fold bars).
    bg_panel : str
        Secondary panel background (e.g. bottom button bar).
    bg_separator : str
        Background of section separators / caption bars.
    fg_viewport : str
        Foreground colour for MicroscopeViewport panels.
    fg_label : str
        Foreground colour for static text labels inside panels.
    fg_stream_bar : str
        Foreground colour for stream-bar panels.
    fg_caption : str
        Foreground colour for fold-panel caption bars.
    font_size_default : int
        Standard dialog / panel font size in points.
    font_size_button_large : int
        Large button label font size in points (e.g. height-48 Close button).
    """

    bg_base: str
    bg_main: str
    bg_panel: str
    bg_separator: str
    fg_viewport: str
    fg_label: str
    fg_stream_bar: str
    fg_caption: str
    font_size_default: int
    font_size_button_large: int


#: Default dark theme – mirrors the colours that were previously hardcoded in
#: the XRC files and in ``odemis.gui``.
DARK = Theme(
    bg_base="#000000",
    bg_main=gui.BG_COLOUR_MAIN,
    bg_panel=gui.BG_COLOUR_PANEL,
    bg_separator=gui.BG_COLOUR_SEPARATOR,
    fg_viewport=gui.FG_COLOUR_VIEWPORT,
    fg_label=gui.FG_COLOUR_LABEL,
    fg_stream_bar=gui.FG_COLOUR_STREAM_BAR,
    fg_caption=gui.BG_COLOUR_LEGEND,
    font_size_default=gui.FONT_SIZE_DEFAULT,
    font_size_button_large=gui.FONT_SIZE_BUTTON_LARGE,
)

#: Light theme – inverted luminance mapping of DARK, suitable for bright
#: environments or accessibility needs.
DARK_BIG = Theme(
    bg_base="#000000",
    bg_main=gui.BG_COLOUR_MAIN,
    bg_panel=gui.BG_COLOUR_PANEL,
    bg_separator=gui.BG_COLOUR_SEPARATOR,
    fg_viewport=gui.FG_COLOUR_VIEWPORT,
    fg_label=gui.FG_COLOUR_LABEL,
    fg_stream_bar=gui.FG_COLOUR_STREAM_BAR,
    fg_caption=gui.BG_COLOUR_LEGEND,
    font_size_default=int(gui.FONT_SIZE_DEFAULT * 1.5),
    font_size_button_large=int(gui.FONT_SIZE_BUTTON_LARGE * 1.5),
)
