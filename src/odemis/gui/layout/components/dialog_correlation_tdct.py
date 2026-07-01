# -*- coding: utf-8 -*-
"""
Layout definition for the Multipoint Correlation (TDCT) dialog.

Replaces dialog_correlation_tdct.xrc / xrcfr_correlation from main_xrc.py.

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

import wx
import wx.grid

from odemis.gui import img
from odemis.gui.comp.buttons import ImageButton, ImageTextButton
from odemis.gui.comp.foldpanelbar import FoldPanelBar, FoldPanelItem
from odemis.gui.comp.grid import ViewportGrid
from odemis.gui.comp.stream_bar import StreamBar
from odemis.gui.comp.viewport import MicroscopeViewport
from odemis.gui.cont.tools import ToolBar
from odemis.gui.layout.constants import strings
from odemis.gui.layout.util.sizers import hbox, vbox
from odemis.gui.layout.constants.theme import DARK, Theme


class FrCorrelation(wx.Dialog):
    """
    Layout for the Multipoint Correlation (TDCT) dialog.

    Provides the same named widget attributes as the xrcfr_correlation class generated
    from dialog_correlation_tdct.xrc, so that CorrelationDialog can use it as a drop-in
    replacement by inheriting from this class instead.

    Attributes
    ----------
    correlation_toolbar : ToolBar
        Vertical toolbar on the left side.
    pnl_correlation_grid : ViewportGrid
        Grid panel holding the two microscope viewports.
    vp_correlation_tl : MicroscopeViewport
        Top-left (FLM) viewport.
    vp_correlation_tr : MicroscopeViewport
        Top-right (FIB) viewport.
    scr_win_right : wx.ScrolledWindow
        Scrollable right-hand panel.
    fp_correlation_panel : FoldPanelItem
        Fold panel item containing the correlation controls.
    pnl_correlation : wx.Panel
        Panel inside fp_correlation_panel holding the grid and buttons.
    btn_delete_row : ImageButton
        Button to delete a selected row from the correlation table.
    btn_xyz_targeting : wx.Button
        Button to trigger XYZ-refinement.
    txt_refine_xyz_active : wx.StaticText
        Status label shown while XYZ-refinement is active.
    table_grid : wx.grid.Grid
        Grid widget for displaying and editing correlation points.
    txt_correlation_rms : wx.StaticText
        Label displaying the correlation RMS deviation.
    fp_correlation_streams : FoldPanelItem
        Fold panel item containing the stream bar.
    pnl_correlation_streams : StreamBar
        Stream bar for managing correlation streams.
    btn_close : ImageTextButton
        Close button at the bottom of the right panel.
    """

    def __init__(self, parent: wx.Window, theme: Theme = DARK) -> None:
        """
        Initialise the dialog and build the complete widget hierarchy.

        :param parent: Parent window.
        :param theme: Visual theme to apply. Defaults to DARK.
        """
        super().__init__(
            parent,
            title=strings.TITLE_CORRELATION,
            style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER,
        )
        self._theme = theme
        self.SetBackgroundColour(theme.bg_base)

        font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        font.SetPointSize(theme.font_size_default)
        self.SetFont(font)

        self._build_layout()

    def _build_layout(self) -> None:
        """
        Construct all child widgets and sizers.
        """
        # --- Root sizer: 3-column FlexGrid (left toolbar | viewport grid | right panel) ---
        root_sizer = wx.FlexGridSizer(rows=1, cols=3, vgap=0, hgap=0)
        root_sizer.AddGrowableCol(1)  # viewport grid grows horizontally
        root_sizer.AddGrowableRow(0)
        self.SetSizer(root_sizer)

        t = self._theme

        # ── Column 0: toolbar panel ─────────────────────────────────────────────
        toolbar_panel = wx.Panel(self)
        toolbar_panel.SetBackgroundColour(t.bg_main)
        root_sizer.Add(toolbar_panel, flag=wx.EXPAND)

        with vbox() as tb_outer:
            toolbar_panel.SetSizer(tb_outer)

            with hbox() as tb_row:
                tb_outer.Add(tb_row)
                tb_row.Add((0, 0), proportion=1, flag=wx.EXPAND)
                self.correlation_toolbar = ToolBar(toolbar_panel, style=wx.VERTICAL)
                tb_row.Add(self.correlation_toolbar)
                tb_row.Add((0, 0), proportion=1, flag=wx.EXPAND)

        # ── Column 1: viewport grid ─────────────────────────────────────────────
        self.pnl_correlation_grid = ViewportGrid(self)
        root_sizer.Add(self.pnl_correlation_grid, proportion=1, flag=wx.EXPAND)

        self.vp_correlation_tl = MicroscopeViewport(self.pnl_correlation_grid)
        self.vp_correlation_tl.SetForegroundColour(t.fg_viewport)
        self.vp_correlation_tl.SetBackgroundColour(t.bg_base)

        self.vp_correlation_tr = MicroscopeViewport(self.pnl_correlation_grid)
        self.vp_correlation_tr.SetForegroundColour(t.fg_viewport)
        self.vp_correlation_tr.SetBackgroundColour(t.bg_base)

        # ── Column 2: right panel ───────────────────────────────────────────────
        right_panel = wx.Panel(self, size=(400, -1))
        right_panel.SetBackgroundColour(t.bg_main)
        right_panel.SetWindowStyle(wx.BORDER_NONE)
        root_sizer.Add(right_panel, flag=wx.EXPAND)

        with vbox() as right_sizer:
            right_panel.SetSizer(right_sizer)
            self._build_scroll_panel(right_panel, right_sizer)
            self._build_close_bar(right_panel, right_sizer)

        # Trigger a layout pass so that all child windows receive EVT_SIZE,
        # matching the implicit behaviour of XRC's LoadDialog.  This ensures
        # that ViewportGrid.viewports (populated on first EVT_SIZE) is set
        # before CorrelationDialog.__init__ accesses it.
        self.Layout()

    def _build_scroll_panel(self, right_panel: wx.Panel, right_sizer: wx.BoxSizer) -> None:
        """
        Build the scrollable right pane that holds the fold panels.

        :param right_panel: Parent panel for the scrolled window.
        :param right_sizer: Sizer of right_panel to attach the scrolled window to.
        """
        t = self._theme

        self.scr_win_right = wx.ScrolledWindow(
            right_panel,
            size=(400, -1),
            style=wx.VSCROLL,
        )
        self.scr_win_right.SetBackgroundColour(t.bg_main)
        self.scr_win_right.EnableScrolling(False, True)
        self.scr_win_right.SetScrollbars(-1, 10, 1, 1)
        right_sizer.Add(
            self.scr_win_right,
            proportion=1,
            flag=wx.EXPAND,
        )
        right_sizer.SetItemMinSize(self.scr_win_right, 400, 400)

        with vbox() as scroll_sizer:
            self.scr_win_right.SetSizer(scroll_sizer)

            fold_bar = FoldPanelBar(self.scr_win_right)
            fold_bar.SetBackgroundColour(t.bg_main)
            scroll_sizer.Add(fold_bar, flag=wx.EXPAND)

            self._build_fp_correlation_panel(fold_bar)
            self._build_fp_correlation_streams(fold_bar)

    def _build_fp_correlation_panel(self, fold_bar: FoldPanelBar) -> None:
        """
        Build the fp_correlation_panel fold-panel item and its contents.

        :param fold_bar: Parent FoldPanelBar to which this item is added.
        """
        t = self._theme

        self.fp_correlation_panel = FoldPanelItem(fold_bar, label="")

        self.pnl_correlation = wx.Panel(self.fp_correlation_panel)

        with vbox() as pnl_sizer:
            self.pnl_correlation.SetSizer(pnl_sizer)

            with hbox() as btn_row:
                pnl_sizer.Add(btn_row)

                self.btn_delete_row = ImageButton(
                    self.pnl_correlation,
                    icon=img.getBitmap("icon/ico_trash.png"),
                    height=16,
                    style=wx.ALIGN_CENTRE,
                )

                btn_row.Add(self.btn_delete_row, flag=wx.ALL | wx.EXPAND, border=t.border_default)
                self.btn_xyz_targeting = wx.Button(self.pnl_correlation, label=strings.BTN_REFINE)
                btn_row.Add(self.btn_xyz_targeting)

                self.txt_refine_xyz_active = wx.StaticText(self.pnl_correlation, label=" ")
                self.txt_refine_xyz_active.SetForegroundColour(t.fg_label)
                self.txt_refine_xyz_active.Show(False)
                btn_row.Add(
                    self.txt_refine_xyz_active,
                    flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL,
                    border=t.border_default,
                )

            # Correlation table
            self.table_grid = wx.grid.Grid(self.pnl_correlation, style=wx.WANTS_CHARS)
            pnl_sizer.Add(self.table_grid)

            # RMS label (hidden initially)
            self.txt_correlation_rms = wx.StaticText(
                self.pnl_correlation,
                label=strings.LBL_CORRELATION_RMS,
            )
            self.txt_correlation_rms.SetForegroundColour(t.fg_label)
            self.txt_correlation_rms.Show(False)
            pnl_sizer.Add(self.txt_correlation_rms, flag=wx.LEFT, border=t.border_default)

        self.fp_correlation_panel.add_item(self.pnl_correlation)
        fold_bar.add_item(self.fp_correlation_panel)

    def _build_fp_correlation_streams(self, fold_bar: FoldPanelBar) -> None:
        """
        Build the fp_correlation_streams fold-panel item and its stream bar.

        :param fold_bar: Parent FoldPanelBar to which this item is added.
        """
        t = self._theme

        self.fp_correlation_streams = FoldPanelItem(fold_bar, label=strings.LBL_STREAMS)
        self.fp_correlation_streams.SetForegroundColour(t.fg_caption)
        self.fp_correlation_streams.SetBackgroundColour(t.bg_separator)

        self.pnl_correlation_streams = StreamBar(
            self.fp_correlation_streams,
            size=(t.side_panel_width, -1),
        )
        self.pnl_correlation_streams.SetForegroundColour(t.fg_stream_bar)
        self.pnl_correlation_streams.SetBackgroundColour(t.bg_main)

        self.fp_correlation_streams.add_item(self.pnl_correlation_streams)
        fold_bar.add_item(self.fp_correlation_streams)

    def _build_close_bar(self, right_panel: wx.Panel, right_sizer: wx.BoxSizer) -> None:
        """
        Build the bottom close-button bar.

        :param right_panel: Parent panel for the close bar.
        :param right_sizer: Sizer of right_panel to attach the close bar to.
        """
        t = self._theme

        close_bar = wx.Panel(right_panel)
        close_bar.SetBackgroundColour(t.bg_panel)
        right_sizer.Add(close_bar, flag=wx.EXPAND)

        with hbox() as close_bar_sizer:
            close_bar.SetSizer(close_bar_sizer)

            self.btn_close = ImageTextButton(
                close_bar,
                height=48,
                face_colour=t.btn_face_default,
                label=strings.BTN_CLOSE,
                style=wx.ALIGN_CENTRE,
            )
            close_btn_font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
            close_btn_font.SetPointSize(t.font_size_button_large)
            self.btn_close.SetFont(close_btn_font)
            close_bar_sizer.Add(
                self.btn_close,
                proportion=1,
                flag=wx.TOP | wx.BOTTOM | wx.LEFT | wx.EXPAND,
                border=t.border_default,
            )


if __name__ == "__main__":
    from odemis.gui.layout.util.preview import run_preview
    run_preview(FrCorrelation)
