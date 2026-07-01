# -*- coding: utf-8 -*-
"""
Layout definition for the FIBSEM tab panel.

Replaces panel_tab_fibsem.xrc / xrcpnl_tab_fibsem from main_xrc.py.

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
import wx.adv

from odemis.gui import img
from odemis.gui.comp.buttons import (
    ImageButton,
    ImageTextButton,
    ProgressRadioButton,
    ViewButton,
)
from odemis.gui.comp.foldpanelbar import FoldPanelBar, FoldPanelItem
from odemis.gui.comp.grid import ViewportGrid
from odemis.gui.comp.stream_bar import StreamBar
from odemis.gui.comp.text import UnitFloatCtrl
from odemis.gui.comp.viewport import FeatureOverviewViewport, LiveViewport
from odemis.gui.cont.tools import ToolBar
from odemis.gui.layout.constants import strings
from odemis.gui.layout.constants.theme import DARK, Theme
from odemis.gui.layout.util.sizers import hbox, vbox


class PnlTabFibsem(wx.Panel):
    """
    Layout for the FIBSEM tab panel.

    Provides the same named widget attributes as the XRC-generated class
    xrcpnl_tab_fibsem so that FibsemTab can use it as a drop-in replacement.

    Attributes
    ----------
    secom_toolbar : ToolBar
        Vertical toolbar on the left side.
    pnl_secom_grid : ViewportGrid
        Grid panel holding the four microscope viewports.
    vp_secom_tl : LiveViewport
        Top-left viewport (SEM live).
    vp_secom_tr : LiveViewport
        Top-right viewport (FIB live).
    vp_secom_bl : FeatureOverviewViewport
        Bottom-left viewport (feature overview).
    vp_secom_br : LiveViewport
        Bottom-right viewport (FIB static).
    lbl_secom_view_all : wx.StaticText
        Label for the all-viewports view-select button.
    btn_secom_view_all : ViewButton
        Button to show all four viewports.
    lbl_secom_view_tl : wx.StaticText
        Label for the top-left view-select button.
    btn_secom_view_tl : ViewButton
        Button to zoom the top-left viewport to full screen.
    lbl_secom_view_tr : wx.StaticText
        Label for the top-right view-select button.
    btn_secom_view_tr : ViewButton
        Button to zoom the top-right viewport to full screen.
    lbl_secom_view_bl : wx.StaticText
        Label for the bottom-left view-select button.
    btn_secom_view_bl : ViewButton
        Button to zoom the bottom-left viewport to full screen.
    lbl_secom_view_br : wx.StaticText
        Label for the bottom-right view-select button.
    btn_secom_view_br : ViewButton
        Button to zoom the bottom-right viewport to full screen.
    btn_log : ImageButton
        Button to open or close the log panel.
    scr_win_right : wx.ScrolledWindow
        Scrollable right-hand panel.
    fp_feature_panel : FoldPanelItem
        Fold panel item containing feature management controls.
    pnl_features : wx.Panel
        Panel inside fp_feature_panel holding the feature controls.
    btn_delete_feature : ImageButton
        Button to delete the currently selected feature.
    cmb_features : wx.adv.OwnerDrawnComboBox
        Combo box for selecting features.
    btn_create_move_feature : ImageTextButton
        Button to create or move a feature to the current position.
    cmb_feature_status : wx.adv.OwnerDrawnComboBox
        Combo box for setting the status of the current feature.
    btn_go_to_feature : ImageTextButton
        Button to move the stage to the selected feature.
    btn_feature_save_position : ImageTextButton
        Button to save the current stage position as the feature milling position.
    fp_stage_position : FoldPanelItem
        Fold panel item containing stage-position / posture controls.
    pnl_stage_position : wx.Panel
        Panel inside fp_stage_position.
    btn_switch_sem_imaging : ProgressRadioButton
        Button to switch to the SEM imaging posture.
    btn_switch_milling : ProgressRadioButton
        Button to switch to the milling posture.
    lbl_milling_angle : wx.StaticText
        Label for the milling angle control.
    ctrl_milling_angle : UnitFloatCtrl
        Float input for the milling angle in degrees.
    fp_settings_secom_optical : FoldPanelItem
        Fold panel item for optical settings (empty, hidden by default).
    fp_secom_streams : FoldPanelItem
        Fold panel item containing the live-stream bar.
    pnl_secom_streams : StreamBar
        Stream bar for managing live acquisition streams.
    fp_acquisitions : FoldPanelItem
        Fold panel item containing acquisition controls.
    streams_chk_list : wx.CheckListBox
        Checklist of streams available for acquisition.
    chkbox_save_acquisition : wx.CheckBox
        Checkbox to enable automatic saving after acquisition.
    txt_filename : wx.TextCtrl
        Read-only text control showing the current acquisition filename.
    btn_cryosecom_change_file : ImageTextButton
        Button to change the acquisition filename.
    btn_cryosecom_acquire : ImageTextButton
        Button to start acquisition.
    txt_cryosecom_est_time : wx.StaticText
        Label showing the estimated acquisition time.
    gauge_cryosecom_acq : wx.Gauge
        Progress gauge for the acquisition.
    txt_cryosecom_left_time : wx.StaticText
        Label showing remaining acquisition time.
    btn_cryosecom_acqui_cancel : ImageTextButton
        Button to cancel a running acquisition.
    btn_acquire_all : ImageTextButton
        Button to acquire both SEM and FIB.
    btn_acquire_overview : ImageTextButton
        Button to acquire an overview image.
    btn_tdct : ImageTextButton
        Button to open the FIB/FM correlation dialog.
    fp_acquired : FoldPanelItem
        Fold panel item containing the acquired-streams bar.
    pnl_cryosecom_acquired : StreamBar
        Stream bar for browsing acquired static streams.
    fp_automation : FoldPanelItem
        Fold panel item containing the automated milling workflow.
    pnl_automation : wx.Panel
        Panel inside fp_automation.
    workflow_features_chk_list : wx.CheckListBox
        Checklist of features included in the automated milling run.
    workflow_task_chk_list : wx.CheckListBox
        Checklist of milling tasks included in the automated run.
    btn_run_automated_milling : ImageTextButton
        Button to start the automated milling workflow.
    txt_automated_milling_est_time : wx.StaticText
        Label showing the estimated time for the automated milling run.
    gauge_automated_milling : wx.Gauge
        Progress gauge for the automated milling run.
    txt_automated_milling_left_time : wx.StaticText
        Label showing remaining time for the automated milling run.
    btn_automated_milling_cancel : ImageTextButton
        Button to cancel the automated milling run.
    txt_automated_milling_status : wx.StaticText
        Label showing the current status of the automated milling run.
    fp_milling : FoldPanelItem
        Fold panel item containing the milling pattern controls.
    pnl_milling : wx.Panel
        Panel inside fp_milling holding the task list and run controls.
    milling_task_chk_list : wx.CheckListBox
        Checklist of milling patterns/tasks.
    btn_run_milling : ImageTextButton
        Button to start the milling run.
    txt_milling_est_time : wx.StaticText
        Label showing the estimated milling time.
    gauge_milling_series : wx.Gauge
        Progress gauge for the milling series.
    txt_milling_series_left_time : wx.StaticText
        Label showing remaining time for the milling series.
    btn_milling_cancel : ImageTextButton
        Button to cancel the milling run.
    pnl_milling_settings : wx.Panel
        Panel for additional milling settings (populated dynamically).
    pnl_patterns : wx.Panel
        Panel for milling pattern sub-panels (populated dynamically).
    """

    def __init__(self, parent: wx.Window, theme: Theme = DARK) -> None:
        """
        Initialise the panel and build the complete widget hierarchy.

        :param parent: Parent window.
        :param theme: Visual theme to apply. Defaults to DARK.
        """
        super().__init__(parent)
        self._theme = theme
        self.SetBackgroundColour(theme.bg_main)

        font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        font.SetPointSize(theme.font_size_default)
        self.SetFont(font)

        self._build_layout()

    def _build_layout(self) -> None:
        """
        Construct the root horizontal sizer: left toolbar | viewport grid | right panel.
        """
        root_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(root_sizer)

        self._build_toolbar_panel(root_sizer)
        self._build_viewport_grid(root_sizer)
        self._build_right_panel(root_sizer)

        self.Layout()

    # ── Column 0: left toolbar panel ────────────────────────────────────────────

    def _build_toolbar_panel(self, root_sizer: wx.BoxSizer) -> None:
        """
        Build the left-hand toolbar panel with posture-view buttons.

        :param root_sizer: Root horizontal sizer to attach the panel to.
        """
        t = self._theme

        toolbar_panel = wx.Panel(self, size=(200, -1))
        toolbar_panel.SetBackgroundColour(t.bg_main)
        root_sizer.Add(toolbar_panel, flag=wx.EXPAND)

        with vbox() as outer:
            toolbar_panel.SetSizer(outer)

            inner = wx.BoxSizer(wx.VERTICAL)
            outer.Add(inner, proportion=1, flag=wx.BOTTOM | wx.EXPAND, border=t.border_default)

            # Top spacer — centres the toolbar vertically
            inner.Add((0, 0), proportion=1, flag=wx.EXPAND)

            self.secom_toolbar = ToolBar(toolbar_panel, style=wx.VERTICAL)
            inner.Add(self.secom_toolbar, flag=wx.ALIGN_RIGHT)

            # Middle spacer
            inner.Add((0, 0), proportion=1, flag=wx.EXPAND)

            # View-all button
            self._add_view_button_pair(
                inner, toolbar_panel,
                "lbl_secom_view_all", "btn_secom_view_all",
                top_bottom_border=False,
            )

            # View TL, TR, BL, BR
            for name in ("tl", "tr", "bl", "br"):
                self._add_view_button_pair(
                    inner, toolbar_panel,
                    f"lbl_secom_view_{name}", f"btn_secom_view_{name}",
                    top_bottom_border=True,
                )

            # Remove bottom border from the very last button
            btn_br = getattr(self, "btn_secom_view_br")
            item = inner.GetItem(btn_br)
            if item is not None:
                item.SetFlag(wx.ALIGN_RIGHT)

            # Log button at the bottom
            self.btn_log = ImageButton(
                toolbar_panel,
                icon=img.getBitmap("icon/ico_chevron_up.png"),
                height=16,
                style=wx.ALIGN_CENTRE,
            )
            self.btn_log.SetToolTip(strings.TOOLTIP_LOG)
            outer.Add(self.btn_log, flag=wx.BOTTOM | wx.LEFT | wx.RIGHT, border=t.border_default)

    def _add_view_button_pair(
        self,
        sizer: wx.BoxSizer,
        parent: wx.Panel,
        lbl_attr: str,
        btn_attr: str,
        top_bottom_border: bool,
    ) -> None:
        """
        Add a (label, ViewButton) pair to a vertical sizer and store them as attributes.

        :param sizer: Vertical BoxSizer to add the pair into.
        :param parent: Parent panel for the label and button widgets.
        :param lbl_attr: Attribute name under which the label is stored.
        :param btn_attr: Attribute name under which the button is stored.
        :param top_bottom_border: Whether to add TOP and BOTTOM borders to the label.
        """
        t = self._theme

        lbl = wx.StaticText(parent, label=strings.LBL_VIEW_BTN)
        lbl.SetForegroundColour(t.fg_viewport)
        setattr(self, lbl_attr, lbl)

        lbl_sizer = wx.BoxSizer(wx.VERTICAL)
        lbl_flag = wx.BOTTOM
        if top_bottom_border:
            lbl_flag |= wx.TOP
        lbl_sizer.Add(lbl, flag=lbl_flag, border=t.border_tiny)
        sizer.Add(lbl_sizer, flag=wx.RIGHT | wx.ALIGN_RIGHT, border=18)

        btn = ViewButton(parent)
        setattr(self, btn_attr, btn)
        sizer.Add(btn, flag=wx.BOTTOM | wx.ALIGN_RIGHT, border=6)

    # ── Column 1: viewport grid ──────────────────────────────────────────────────

    def _build_viewport_grid(self, root_sizer: wx.BoxSizer) -> None:
        """
        Build the ViewportGrid with four child viewports.

        :param root_sizer: Root horizontal sizer to attach the grid to.
        """
        t = self._theme

        self.pnl_secom_grid = ViewportGrid(self)
        root_sizer.Add(self.pnl_secom_grid, proportion=1, flag=wx.EXPAND)

        self.vp_secom_tl = LiveViewport(self.pnl_secom_grid)
        self.vp_secom_tl.SetForegroundColour(t.fg_viewport)
        self.vp_secom_tl.SetBackgroundColour(wx.BLACK)

        self.vp_secom_tr = LiveViewport(self.pnl_secom_grid)
        self.vp_secom_tr.SetForegroundColour(t.fg_viewport)
        self.vp_secom_tr.SetBackgroundColour(wx.BLACK)

        self.vp_secom_bl = FeatureOverviewViewport(self.pnl_secom_grid)
        self.vp_secom_bl.SetForegroundColour(t.fg_viewport)
        self.vp_secom_bl.SetBackgroundColour(wx.BLACK)

        self.vp_secom_br = LiveViewport(self.pnl_secom_grid)
        self.vp_secom_br.SetForegroundColour(t.fg_viewport)
        self.vp_secom_br.SetBackgroundColour(wx.BLACK)

    # ── Column 2: right panel ────────────────────────────────────────────────────

    def _build_right_panel(self, root_sizer: wx.BoxSizer) -> None:
        """
        Build the right scrollable panel containing all fold-panel items.

        :param root_sizer: Root horizontal sizer to attach the right panel to.
        """
        t = self._theme

        right_panel = wx.Panel(self, size=(400, -1))
        right_panel.SetBackgroundColour(t.bg_main)
        right_panel.SetWindowStyle(wx.BORDER_NONE)
        root_sizer.Add(right_panel, flag=wx.EXPAND)

        with vbox() as right_sizer:
            right_panel.SetSizer(right_sizer)

            self.scr_win_right = wx.ScrolledWindow(
                right_panel,
                size=(400, -1),
                style=wx.VSCROLL,
            )
            self.scr_win_right.SetBackgroundColour(t.bg_main)
            self.scr_win_right.EnableScrolling(False, True)
            self.scr_win_right.SetScrollbars(-1, 10, 1, 1)
            right_sizer.Add(self.scr_win_right, proportion=1, flag=wx.EXPAND)
            right_sizer.SetItemMinSize(self.scr_win_right, 400, 400)

            with vbox() as scroll_sizer:
                self.scr_win_right.SetSizer(scroll_sizer)

                fold_bar = FoldPanelBar(self.scr_win_right)
                fold_bar.SetBackgroundColour(t.bg_main)
                scroll_sizer.Add(fold_bar, flag=wx.EXPAND)

                self._build_fp_feature_panel(fold_bar)
                self._build_fp_stage_position(fold_bar)
                self._build_fp_settings_secom_optical(fold_bar)
                self._build_fp_secom_streams(fold_bar)
                self._build_fp_acquisitions(fold_bar)
                self._build_fp_acquired(fold_bar)
                self._build_fp_automation(fold_bar)
                self._build_fp_milling(fold_bar)

    # ── Fold panel: FEATURES ─────────────────────────────────────────────────────

    def _build_fp_feature_panel(self, fold_bar: FoldPanelBar) -> None:
        """
        Build the FEATURES fold panel item and its contents.

        :param fold_bar: Parent FoldPanelBar to which this item is added.
        """
        t = self._theme

        self.fp_feature_panel = FoldPanelItem(fold_bar, label=strings.LBL_FEATURES)
        self.fp_feature_panel.SetForegroundColour(t.fg_caption)
        self.fp_feature_panel.SetBackgroundColour(t.bg_separator)

        self.pnl_features = wx.Panel(self.fp_feature_panel)
        self.pnl_features.SetBackgroundColour(t.bg_main)

        with vbox() as pnl_sizer:
            self.pnl_features.SetSizer(pnl_sizer)

            # Row 1: delete icon | feature combo | create/move button
            with hbox() as row1:
                pnl_sizer.Add(row1, flag=wx.LEFT | wx.TOP, border=t.border_default)

                self.btn_delete_feature = ImageButton(
                    self.pnl_features,
                    icon=img.getBitmap("icon/ico_trash.png"),
                    height=16,
                    style=wx.ALIGN_CENTRE,
                )
                self.btn_delete_feature.SetForegroundColour(wx.WHITE)
                self.btn_delete_feature.SetBackgroundColour(t.bg_main)
                row1.Add(self.btn_delete_feature)

                self.cmb_features = wx.adv.OwnerDrawnComboBox(
                    self.pnl_features,
                    size=(156, 20),
                    style=wx.BORDER_NONE | wx.CB_DROPDOWN | wx.TE_PROCESS_ENTER,
                )
                self.cmb_features.SetForegroundColour(t.fg_editable)
                self.cmb_features.SetBackgroundColour(t.bg_main)
                row1.Add(self.cmb_features)

                btn_panel = wx.Panel(self.pnl_features, size=(120, 24))
                btn_panel.SetBackgroundColour(t.bg_main)
                row1.Add(btn_panel, flag=wx.LEFT | wx.ALIGN_CENTER_VERTICAL, border=t.indent_feature)

                with hbox() as bp_sizer:
                    btn_panel.SetSizer(bp_sizer)
                    self.btn_create_move_feature = ImageTextButton(
                        btn_panel,
                        height=24,
                        label=strings.BTN_CREATE_MOVE,
                        style=wx.ALIGN_CENTRE,
                    )
                    self.btn_create_move_feature.SetForegroundColour(wx.WHITE)
                    bp_sizer.Add(
                        self.btn_create_move_feature,
                        proportion=1,
                        flag=wx.ALIGN_CENTER,
                    )

            # Row 2: status label | status combo | go-to-feature button
            with hbox() as row2:
                pnl_sizer.Add(row2, flag=wx.LEFT | wx.TOP, border=t.border_default)

                status_lbl = wx.StaticText(self.pnl_features, label=strings.LBL_STATUS)
                status_lbl.SetForegroundColour(t.fg_subtle)
                row2.Add(status_lbl)

                self.cmb_feature_status = wx.adv.OwnerDrawnComboBox(
                    self.pnl_features,
                    size=(133, 16),
                    style=(
                        wx.BORDER_NONE | wx.CB_DROPDOWN | wx.CB_READONLY | wx.TE_PROCESS_ENTER
                    ),
                )
                self.cmb_feature_status.SetForegroundColour(t.fg_editable)
                self.cmb_feature_status.SetBackgroundColour(t.bg_main)
                row2.Add(self.cmb_feature_status, flag=wx.LEFT, border=t.border_default)

                go_panel = wx.Panel(self.pnl_features, size=(120, 24))
                go_panel.SetBackgroundColour(t.bg_main)
                row2.Add(go_panel, flag=wx.LEFT | wx.ALIGN_CENTER_VERTICAL, border=t.indent_feature)

                with hbox() as go_sizer:
                    go_panel.SetSizer(go_sizer)
                    self.btn_go_to_feature = ImageTextButton(
                        go_panel,
                        height=24,
                        label=strings.BTN_GO_TO_FEATURE,
                        style=wx.ALIGN_CENTRE,
                    )
                    self.btn_go_to_feature.SetForegroundColour(wx.WHITE)
                    go_sizer.Add(
                        self.btn_go_to_feature,
                        proportion=1,
                        flag=wx.ALIGN_CENTER,
                    )

            # Row 3: save position button
            with hbox() as row3:
                pnl_sizer.Add(row3, flag=wx.LEFT | wx.TOP | wx.BOTTOM, border=t.border_small)

                self.btn_feature_save_position = ImageTextButton(
                    self.pnl_features,
                    icon=img.getBitmap("icon/ico_save.png"),
                    height=48,
                    face_colour=t.btn_face_primary,
                    label=strings.BTN_SAVE_POSITION,
                    style=wx.ALIGN_CENTRE,
                )
                self.btn_feature_save_position.SetForegroundColour(wx.WHITE)
                font12 = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
                font12.SetPointSize(12)
                self.btn_feature_save_position.SetFont(font12)
                row3.Add(
                    self.btn_feature_save_position,
                    flag=wx.ALL | wx.EXPAND,
                    border=t.border_small,
                )

        self.fp_feature_panel.add_item(self.pnl_features)
        fold_bar.add_item(self.fp_feature_panel)

    # ── Fold panel: STAGE POSITION ───────────────────────────────────────────────

    def _build_fp_stage_position(self, fold_bar: FoldPanelBar) -> None:
        """
        Build the STAGE POSITION fold panel item with posture-switch buttons.

        :param fold_bar: Parent FoldPanelBar to which this item is added.
        """
        t = self._theme

        self.fp_stage_position = FoldPanelItem(fold_bar, label=strings.LBL_STAGE_POSITION)
        self.fp_stage_position.SetForegroundColour(t.fg_caption)
        self.fp_stage_position.SetBackgroundColour(t.bg_separator)

        self.pnl_stage_position = wx.Panel(self.fp_stage_position)
        self.pnl_stage_position.SetForegroundColour(t.fg_stream_bar)
        self.pnl_stage_position.SetBackgroundColour(t.bg_main)

        with vbox() as pnl_sizer:
            self.pnl_stage_position.SetSizer(pnl_sizer)

            # Posture switch buttons row
            with hbox() as btn_row:
                pnl_sizer.Add(btn_row, proportion=1, flag=wx.EXPAND)

                self.btn_switch_sem_imaging = ProgressRadioButton(
                    self.pnl_stage_position,
                    height=48,
                    face_colour=t.btn_face_default,
                    label=strings.BTN_SEM_IMAGING,
                    icon=img.getBitmap("icon/ico_sem.png"),
                    icon_progress=img.getBitmap("icon/ico_sem_orange.png"),
                    icon_on=img.getBitmap("icon/ico_sem_green.png"),
                    style=wx.ALIGN_CENTRE,
                )
                self.btn_switch_sem_imaging.SetForegroundColour(t.fg_caption)
                font11 = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
                font11.SetPointSize(11)
                self.btn_switch_sem_imaging.SetFont(font11)
                btn_row.Add(
                    self.btn_switch_sem_imaging,
                    proportion=1,
                    flag=wx.EXPAND | wx.ALL,
                    border=t.border_default,
                )

                self.btn_switch_milling = ProgressRadioButton(
                    self.pnl_stage_position,
                    height=48,
                    face_colour=t.btn_face_default,
                    label=strings.BTN_MILLING,
                    icon=img.getBitmap("icon/ico_milling.png"),
                    icon_progress=img.getBitmap("icon/ico_milling_orange.png"),
                    icon_on=img.getBitmap("icon/ico_milling_green.png"),
                    style=wx.ALIGN_CENTRE,
                )
                self.btn_switch_milling.SetForegroundColour(t.fg_caption)
                self.btn_switch_milling.SetFont(font11)
                btn_row.Add(
                    self.btn_switch_milling,
                    proportion=1,
                    flag=wx.EXPAND | wx.ALL,
                    border=t.border_default,
                )

            # Milling angle row
            with hbox() as angle_row:
                pnl_sizer.Add(angle_row, flag=wx.ALIGN_CENTRE)

                self.lbl_milling_angle = wx.StaticText(
                    self.pnl_stage_position,
                    label=strings.LBL_MILLING_ANGLE,
                )
                self.lbl_milling_angle.SetForegroundColour(t.fg_viewport)
                font10 = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
                font10.SetPointSize(10)
                self.lbl_milling_angle.SetFont(font10)
                angle_row.Add(
                    self.lbl_milling_angle,
                    flag=wx.LEFT | wx.BOTTOM,
                    border=t.border_default,
                )

                self.ctrl_milling_angle = UnitFloatCtrl(
                    self.pnl_stage_position,
                    value=10,
                    accuracy=2,
                    key_step=0.1,
                    unit="°",
                    size=(-1, 20),
                    style=wx.BORDER_NONE,
                )
                self.ctrl_milling_angle.SetFont(font10)
                angle_row.Add(
                    self.ctrl_milling_angle,
                    flag=wx.LEFT | wx.BOTTOM,
                    border=t.border_default,
                )

        self.fp_stage_position.add_item(self.pnl_stage_position)
        fold_bar.add_item(self.fp_stage_position)

    # ── Fold panel: OPTICAL SETTINGS (empty) ─────────────────────────────────────

    def _build_fp_settings_secom_optical(self, fold_bar: FoldPanelBar) -> None:
        """
        Build the OPTICAL SETTINGS fold panel item (initially empty / hidden).

        :param fold_bar: Parent FoldPanelBar to which this item is added.
        """
        t = self._theme

        self.fp_settings_secom_optical = FoldPanelItem(
            fold_bar, label=strings.LBL_OPTICAL_SETTINGS
        )
        self.fp_settings_secom_optical.SetForegroundColour(t.fg_caption)
        self.fp_settings_secom_optical.SetBackgroundColour(t.bg_separator)

        fold_bar.add_item(self.fp_settings_secom_optical)

    # ── Fold panel: STREAMS ──────────────────────────────────────────────────────

    def _build_fp_secom_streams(self, fold_bar: FoldPanelBar) -> None:
        """
        Build the STREAMS fold panel item with the live stream bar.

        :param fold_bar: Parent FoldPanelBar to which this item is added.
        """
        t = self._theme

        self.fp_secom_streams = FoldPanelItem(fold_bar, label=strings.LBL_STREAMS)
        self.fp_secom_streams.SetForegroundColour(t.fg_caption)
        self.fp_secom_streams.SetBackgroundColour(t.bg_separator)

        self.pnl_secom_streams = StreamBar(
            self.fp_secom_streams,
            size=(300, -1),
            add_button=False,
        )
        self.pnl_secom_streams.SetForegroundColour(t.fg_stream_bar)
        self.pnl_secom_streams.SetBackgroundColour(t.bg_main)

        self.fp_secom_streams.add_item(self.pnl_secom_streams)
        fold_bar.add_item(self.fp_secom_streams)

    # ── Fold panel: ACQUISITIONS ─────────────────────────────────────────────────

    def _build_fp_acquisitions(self, fold_bar: FoldPanelBar) -> None:
        """
        Build the ACQUISITIONS fold panel item with all acquisition controls.

        :param fold_bar: Parent FoldPanelBar to which this item is added.
        """
        t = self._theme

        self.fp_acquisitions = FoldPanelItem(fold_bar, label=strings.LBL_ACQUISITIONS)
        self.fp_acquisitions.SetForegroundColour(t.fg_caption)
        self.fp_acquisitions.SetBackgroundColour(t.bg_separator)

        acq_panel = wx.Panel(self.fp_acquisitions, size=(400, -1))
        acq_panel.SetBackgroundColour(t.bg_main)
        acq_panel.SetWindowStyle(wx.BORDER_NONE)

        with vbox() as pnl_sizer:
            acq_panel.SetSizer(pnl_sizer)

            # Stream checklist
            self.streams_chk_list = wx.CheckListBox(acq_panel)
            font10_sys = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
            font10_sys.SetPointSize(10)
            self.streams_chk_list.SetFont(font10_sys)
            pnl_sizer.Add(
                self.streams_chk_list,
                proportion=1,
                flag=wx.RIGHT | wx.LEFT | wx.EXPAND,
                border=t.border_default,
            )

            # Auto-save checkbox
            self.chkbox_save_acquisition = wx.CheckBox(
                acq_panel, label=strings.LBL_AUTO_SAVE
            )
            self.chkbox_save_acquisition.SetForegroundColour(t.fg_label)
            pnl_sizer.Add(
                self.chkbox_save_acquisition,
                flag=wx.ALL | wx.EXPAND,
                border=t.border_default,
            )

            # Filename row
            with hbox() as fn_row:
                pnl_sizer.Add(
                    fn_row,
                    flag=wx.TOP | wx.LEFT | wx.RIGHT | wx.EXPAND,
                    border=t.border_default,
                )

                fn_lbl = wx.StaticText(acq_panel, label=strings.LBL_FILENAME)
                fn_lbl.SetForegroundColour(t.fg_label)
                fn_row.Add(fn_lbl, flag=wx.ALIGN_CENTER_VERTICAL)

                self.txt_filename = wx.TextCtrl(
                    acq_panel,
                    value=strings.TXT_PROJECT_PATH_DEFAULT,
                    size=(-1, 20),
                    style=wx.BORDER_NONE | wx.TE_READONLY,
                )
                self.txt_filename.SetForegroundColour(t.fg_editable)
                self.txt_filename.SetBackgroundColour(t.bg_main)
                fn_row.Add(
                    self.txt_filename,
                    proportion=1,
                    flag=wx.LEFT | wx.EXPAND,
                    border=t.border_small,
                )

                self.btn_cryosecom_change_file = ImageTextButton(
                    acq_panel,
                    height=24,
                    face_colour=t.btn_face_default,
                    label=strings.BTN_CHANGE_FILE,
                )
                fn_row.Add(self.btn_cryosecom_change_file, flag=wx.LEFT, border=t.border_small)

            # Acquire row (button | est. time | gauge+cancel)
            acq_grid = wx.FlexGridSizer(rows=1, cols=3, vgap=0, hgap=5)
            acq_grid.AddGrowableCol(1)
            pnl_sizer.Add(acq_grid, flag=wx.ALL | wx.EXPAND, border=t.border_default)

            acquire_btn_panel = wx.Panel(acq_panel, size=(200, 48))
            acquire_btn_panel.SetBackgroundColour(t.bg_main)
            acq_grid.Add(acquire_btn_panel, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=t.border_tiny)

            with hbox() as abp_sizer:
                acquire_btn_panel.SetSizer(abp_sizer)
                self.btn_cryosecom_acquire = ImageTextButton(
                    acquire_btn_panel,
                    icon=img.getBitmap("icon/ico_acqui.png"),
                    height=48,
                    face_colour=t.btn_face_primary,
                    label=strings.BTN_ACQUIRE,
                    style=wx.ALIGN_CENTRE,
                )
                self.btn_cryosecom_acquire.SetForegroundColour(wx.WHITE)
                font15 = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
                font15.SetPointSize(15)
                self.btn_cryosecom_acquire.SetFont(font15)
                abp_sizer.Add(
                    self.btn_cryosecom_acquire,
                    proportion=1,
                    flag=wx.ALIGN_CENTER,
                )

            # Estimated time label
            with hbox() as est_row:
                acq_grid.Add(est_row, flag=wx.TOP, border=t.border_gauge)
                self.txt_cryosecom_est_time = wx.StaticText(
                    acq_panel, label=strings.LBL_ESTIMATED_TIME
                )
                self.txt_cryosecom_est_time.SetForegroundColour(t.fg_label)
                est_row.Add(self.txt_cryosecom_est_time, flag=wx.LEFT, border=0)

            # Gauge + left-time + cancel
            with hbox() as cancel_outer:
                acq_grid.Add(cancel_outer, flag=wx.EXPAND)

                gauge_panel = wx.Panel(acq_panel)
                with vbox() as gp_sizer:
                    gauge_panel.SetSizer(gp_sizer)
                    self.gauge_cryosecom_acq = wx.Gauge(
                        gauge_panel,
                        range=100,
                        size=(-1, 10),
                        style=wx.GA_SMOOTH,
                    )
                    gp_sizer.Add(
                        self.gauge_cryosecom_acq,
                        proportion=1,
                        flag=wx.TOP,
                        border=t.border_default,
                    )
                    self.txt_cryosecom_left_time = wx.StaticText(gauge_panel, label="")
                    self.txt_cryosecom_left_time.SetForegroundColour(t.fg_label)
                    gp_sizer.Add(
                        self.txt_cryosecom_left_time,
                        proportion=1,
                        flag=wx.TOP,
                        border=t.border_default,
                    )
                cancel_outer.Add(gauge_panel, flag=wx.TOP, border=t.border_tiny)

                self.btn_cryosecom_acqui_cancel = ImageTextButton(
                    acq_panel,
                    height=24,
                    face_colour=t.btn_face_default,
                   label=strings.BTN_CANCEL,
                )
                cancel_outer.Add(
                    self.btn_cryosecom_acqui_cancel,
                    flag=wx.TOP | wx.LEFT,
                    border=t.border_medium,
                )

            # Acquire both button
            self.btn_acquire_all = ImageTextButton(
                acq_panel,
                icon=img.getBitmap("icon/ico_acqui.png"),
                height=48,
                face_colour=t.btn_face_primary,
                label=strings.BTN_ACQUIRE_BOTH,
                style=wx.ALIGN_CENTRE,
            )
            self.btn_acquire_all.SetForegroundColour(wx.WHITE)
            self.btn_acquire_all.SetFont(font15)
            pnl_sizer.Add(
                self.btn_acquire_all, flag=wx.ALL | wx.EXPAND, border=t.border_default
            )

            # Acquire overview button
            self.btn_acquire_overview = ImageTextButton(
                acq_panel,
                height=48,
                face_colour=t.btn_face_default,
                label=strings.BTN_ACQUIRE_OVERVIEW,
                style=wx.ALIGN_CENTRE,
            )
            font14 = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
            font14.SetPointSize(14)
            self.btn_acquire_overview.SetFont(font14)
            pnl_sizer.Add(
                self.btn_acquire_overview,
                flag=wx.TOP | wx.BOTTOM | wx.LEFT,
                border=t.border_default,
            )

            # Correlate FIB/FM button
            with hbox() as tdct_row:
                pnl_sizer.Add(
                    tdct_row, flag=wx.TOP | wx.BOTTOM | wx.LEFT, border=t.border_default
                )
                self.btn_tdct = ImageTextButton(
                    acq_panel,
                    height=48,
                    face_colour=t.btn_face_default,
                    label=strings.BTN_CORRELATE_FIB_FM,
                    style=wx.ALIGN_CENTRE,
                )
                self.btn_tdct.SetFont(font14)
                tdct_row.Add(self.btn_tdct)

        self.fp_acquisitions.add_item(acq_panel)
        fold_bar.add_item(self.fp_acquisitions)

    # ── Fold panel: ACQUIRED ─────────────────────────────────────────────────────

    def _build_fp_acquired(self, fold_bar: FoldPanelBar) -> None:
        """
        Build the ACQUIRED fold panel item with the acquired stream bar.

        :param fold_bar: Parent FoldPanelBar to which this item is added.
        """
        t = self._theme

        self.fp_acquired = FoldPanelItem(fold_bar, label=strings.LBL_ACQUIRED)
        self.fp_acquired.SetForegroundColour(t.fg_caption)
        self.fp_acquired.SetBackgroundColour(t.bg_separator)

        self.pnl_cryosecom_acquired = StreamBar(
            self.fp_acquired,
            size=(300, -1),
            add_button=False,
        )
        self.pnl_cryosecom_acquired.SetForegroundColour(t.fg_stream_bar)
        self.pnl_cryosecom_acquired.SetBackgroundColour(t.bg_main)

        self.fp_acquired.add_item(self.pnl_cryosecom_acquired)
        fold_bar.add_item(self.fp_acquired)

    # ── Fold panel: MILLING (automation) ────────────────────────────────────────

    def _build_fp_automation(self, fold_bar: FoldPanelBar) -> None:
        """
        Build the MILLING automation fold panel item.

        :param fold_bar: Parent FoldPanelBar to which this item is added.
        """
        t = self._theme

        self.fp_automation = FoldPanelItem(fold_bar, label=strings.LBL_MILLING)
        self.fp_automation.SetForegroundColour(t.fg_caption)
        self.fp_automation.SetBackgroundColour(t.bg_separator)

        self.pnl_automation = wx.Panel(self.fp_automation)
        self.pnl_automation.SetForegroundColour(t.fg_caption)
        self.pnl_automation.SetBackgroundColour(t.bg_separator)

        with vbox() as pnl_sizer:
            self.pnl_automation.SetSizer(pnl_sizer)

            # Features checklist
            self.workflow_features_chk_list = wx.CheckListBox(self.pnl_automation)
            font10_sys = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
            font10_sys.SetPointSize(10)
            self.workflow_features_chk_list.SetFont(font10_sys)
            pnl_sizer.Add(
                self.workflow_features_chk_list,
                proportion=1,
                flag=wx.RIGHT | wx.LEFT | wx.EXPAND,
                border=t.border_default,
            )

            # Task checklist
            self.workflow_task_chk_list = wx.CheckListBox(self.pnl_automation)
            self.workflow_task_chk_list.SetFont(font10_sys)
            pnl_sizer.Add(
                self.workflow_task_chk_list,
                proportion=1,
                flag=wx.RIGHT | wx.LEFT | wx.TOP | wx.EXPAND,
                border=t.border_default,
            )

            # Run milling button
            self.btn_run_automated_milling = ImageTextButton(
                self.pnl_automation,
                icon=img.getBitmap("icon/ico_milling.png"),
                height=48,
                face_colour=t.btn_face_primary,
                label=strings.BTN_MILL,
                style=wx.ALIGN_CENTRE,
            )
            self.btn_run_automated_milling.SetForegroundColour(wx.WHITE)
            font15 = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
            font15.SetPointSize(15)
            self.btn_run_automated_milling.SetFont(font15)
            pnl_sizer.Add(
                self.btn_run_automated_milling,
                flag=wx.LEFT | wx.RIGHT | wx.TOP | wx.EXPAND,
                border=t.border_default,
            )

            # Estimated time label
            self.txt_automated_milling_est_time = wx.StaticText(
                self.pnl_automation, label=strings.LBL_ESTIMATED_TIME
            )
            self.txt_automated_milling_est_time.SetForegroundColour(t.fg_label)
            pnl_sizer.Add(
                self.txt_automated_milling_est_time,
                flag=wx.LEFT | wx.RIGHT | wx.TOP | wx.EXPAND,
                border=t.border_default,
            )

            # Gauge / left-time / cancel row
            with hbox() as gauge_row:
                pnl_sizer.Add(gauge_row, flag=wx.ALL | wx.EXPAND, border=0)

                gauge_outer = wx.Panel(self.pnl_automation, size=(200, 8))
                with vbox() as go_sizer:
                    gauge_outer.SetSizer(go_sizer)
                    go_sizer.Add((0, 0), proportion=1)
                    self.gauge_automated_milling = wx.Gauge(
                        gauge_outer,
                        range=100,
                        size=(200, 8),
                        style=wx.GA_SMOOTH,
                    )
                    go_sizer.Add(self.gauge_automated_milling)
                    go_sizer.Add((0, 0), proportion=1)
                gauge_row.Add(
                    gauge_outer,
                    flag=wx.LEFT | wx.RIGHT | wx.ALIGN_CENTER_VERTICAL,
                    border=t.border_default,
                )

                left_time_panel = wx.Panel(self.pnl_automation, size=(80, 24))
                with hbox() as ltp_sizer:
                    left_time_panel.SetSizer(ltp_sizer)
                    self.txt_automated_milling_left_time = wx.StaticText(
                        left_time_panel, label=""
                    )
                    self.txt_automated_milling_left_time.SetForegroundColour(t.fg_label)
                    ltp_sizer.Add(
                        self.txt_automated_milling_left_time,
                        proportion=1,
                        flag=wx.ALIGN_CENTER,
                    )
                gauge_row.Add(
                    left_time_panel,
                    flag=wx.LEFT | wx.RIGHT | wx.TOP | wx.ALIGN_CENTER_VERTICAL,
                    border=t.border_default,
                )

                self.btn_automated_milling_cancel = ImageTextButton(
                    self.pnl_automation,
                    height=24,
                    face_colour=t.btn_face_default,
                    label=strings.BTN_CANCEL,
                )
                gauge_row.Add(
                    self.btn_automated_milling_cancel,
                    flag=wx.LEFT | wx.RIGHT | wx.TOP | wx.ALIGN_CENTER_VERTICAL,
                    border=t.border_default,
                )

            # Status label
            self.txt_automated_milling_status = wx.StaticText(
                self.pnl_automation, label=""
            )
            self.txt_automated_milling_status.SetForegroundColour(t.fg_label)
            pnl_sizer.Add(
                self.txt_automated_milling_status,
                flag=wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND,
                border=t.border_default,
            )

        self.fp_automation.add_item(self.pnl_automation)
        fold_bar.add_item(self.fp_automation)

    # ── Fold panel: PATTERNS ─────────────────────────────────────────────────────

    def _build_fp_milling(self, fold_bar: FoldPanelBar) -> None:
        """
        Build the PATTERNS fold panel item for milling task control.

        :param fold_bar: Parent FoldPanelBar to which this item is added.
        """
        t = self._theme

        self.fp_milling = FoldPanelItem(fold_bar, label=strings.LBL_PATTERNS)
        self.fp_milling.SetForegroundColour(t.fg_caption)
        self.fp_milling.SetBackgroundColour(t.bg_separator)

        self.pnl_milling = wx.Panel(self.fp_milling)
        self.pnl_milling.SetForegroundColour(t.fg_caption)
        self.pnl_milling.SetBackgroundColour(t.bg_separator)

        with vbox() as pnl_sizer:
            self.pnl_milling.SetSizer(pnl_sizer)

            # Task checklist
            self.milling_task_chk_list = wx.CheckListBox(self.pnl_milling)
            font10_sys = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
            font10_sys.SetPointSize(10)
            self.milling_task_chk_list.SetFont(font10_sys)
            pnl_sizer.Add(
                self.milling_task_chk_list,
                proportion=1,
                flag=wx.RIGHT | wx.LEFT | wx.EXPAND,
                border=t.border_default,
            )

            # Spacer
            pnl_sizer.Add((0, 10))

            # Run milling button (hidden initially per XRC)
            self.btn_run_milling = ImageTextButton(
                self.pnl_milling,
                icon=img.getBitmap("icon/ico_milling.png"),
                height=48,
                face_colour=t.btn_face_primary,
                label=strings.BTN_MILL,
                style=wx.ALIGN_CENTRE,
            )
            self.btn_run_milling.SetForegroundColour(wx.WHITE)
            font15 = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
            font15.SetPointSize(15)
            self.btn_run_milling.SetFont(font15)
            self.btn_run_milling.Hide()
            pnl_sizer.Add(
                self.btn_run_milling, flag=wx.ALL | wx.EXPAND, border=t.border_default
            )

            # Estimated time label
            self.txt_milling_est_time = wx.StaticText(
                self.pnl_milling, label=strings.LBL_ESTIMATED_TIME
            )
            self.txt_milling_est_time.SetForegroundColour(t.fg_label)
            pnl_sizer.Add(
                self.txt_milling_est_time, flag=wx.TOP, border=t.border_gauge
            )

            # Gauge + left-time row
            with hbox() as gauge_row:
                pnl_sizer.Add(gauge_row, flag=wx.EXPAND)

                with vbox() as gauge_vbox:
                    gauge_row.Add(gauge_vbox, flag=wx.TOP, border=-8)
                    self.gauge_milling_series = wx.Gauge(
                        self.pnl_milling,
                        range=100,
                        size=(-1, 10),
                        style=wx.GA_SMOOTH,
                    )
                    self.gauge_milling_series.Hide()
                    gauge_vbox.Add(
                        self.gauge_milling_series,
                        proportion=1,
                        flag=wx.TOP,
                        border=t.border_default,
                    )
                    self.txt_milling_series_left_time = wx.StaticText(
                        self.pnl_milling, label=""
                    )
                    self.txt_milling_series_left_time.SetForegroundColour(t.fg_label)
                    gauge_vbox.Add(
                        self.txt_milling_series_left_time,
                        proportion=1,
                        flag=wx.TOP,
                        border=t.border_default,
                    )

            # Cancel button (hidden initially per XRC)
            self.btn_milling_cancel = ImageTextButton(
                self.pnl_milling,
                height=24,
                face_colour=t.btn_face_default,
                label=strings.BTN_CANCEL,
            )
            self.btn_milling_cancel.Hide()
            pnl_sizer.Add(
                self.btn_milling_cancel, flag=wx.TOP, border=t.border_medium
            )

        self.fp_milling.add_item(self.pnl_milling)

        # Settings panel (populated dynamically by the milling controller)
        self.pnl_milling_settings = wx.Panel(self.fp_milling)
        self.pnl_milling_settings.SetForegroundColour(t.fg_caption)
        self.pnl_milling_settings.SetBackgroundColour(t.bg_separator)
        self.fp_milling.add_item(self.pnl_milling_settings)

        # Patterns panel (populated dynamically by the milling controller)
        self.pnl_patterns = wx.Panel(self.fp_milling)
        self.pnl_patterns.SetForegroundColour(t.fg_caption)
        self.pnl_patterns.SetBackgroundColour(t.bg_separator)
        self.fp_milling.add_item(self.pnl_patterns)

        fold_bar.add_item(self.fp_milling)


if __name__ == "__main__":
    from odemis.gui.layout.util.preview import run_preview
    run_preview(PnlTabFibsem)
