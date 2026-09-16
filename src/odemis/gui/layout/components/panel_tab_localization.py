# -*- coding: utf-8 -*-
"""
Layout definition for the localization tab panel.

Replaces panel_tab_localization.xrc / xrcpnl_tab_localization from main_xrc.py.

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
    ImageToggleButton,
    ViewButton,
)
from odemis.gui.comp.foldpanelbar import FoldPanelBar, FoldPanelItem
from odemis.gui.comp.grid import ViewportGrid
from odemis.gui.comp.stream_bar import StreamBar
from odemis.gui.comp.text import UnitFloatCtrl
from odemis.gui.comp.viewport import (
    FeatureOverviewViewport,
    LiveViewport,
    MicroscopeViewport,
)
from odemis.gui.cont.tools import ToolBar
from odemis.gui.layout.constants import strings
from odemis.gui.layout.constants.theme import DARK, Theme
from odemis.gui.layout.util.sizers import hbox, vbox


class PnlTabLocalization(wx.Panel):
    """Layout for the cryogenic localization tab."""

    def __init__(self, parent: wx.Window, theme: Theme = DARK) -> None:
        """
        Initialise the panel and build its complete widget hierarchy.

        :param parent: Parent window.
        :param theme: Visual theme to apply.
        """
        super().__init__(parent)
        self._theme = theme
        self.SetBackgroundColour(theme.bg_main)
        self._build_layout()

    def _build_layout(self) -> None:
        """Build the toolbar, viewport grid, and settings column."""
        with hbox() as root_sizer:
            self.SetSizer(root_sizer)
            self._build_toolbar_panel(root_sizer)
            self._build_viewport_grid(root_sizer)
            self._build_right_panel(root_sizer)

        self.Layout()

    def _build_toolbar_panel(self, root_sizer: wx.BoxSizer) -> None:
        """
        Build the left toolbar and viewport-selection controls.

        :param root_sizer: Root horizontal sizer.
        """
        t = self._theme
        panel = wx.Panel(self, size=(200, -1))
        panel.SetBackgroundColour(t.bg_main)
        root_sizer.Add(panel, flag=wx.EXPAND)

        with vbox() as outer:
            panel.SetSizer(outer)

            with vbox() as controls:
                outer.Add(
                    controls,
                    proportion=1,
                    flag=wx.BOTTOM | wx.EXPAND,
                    border=t.border_default,
                )
                controls.Add((0, 0), proportion=1, flag=wx.EXPAND)

                self.secom_toolbar = ToolBar(panel, style=wx.VERTICAL)
                controls.Add(self.secom_toolbar, flag=wx.ALIGN_RIGHT)
                controls.Add((0, 0), proportion=1, flag=wx.EXPAND)

                self._add_view_button(controls, panel, "all", label_top=False)
                self._add_view_button(controls, panel, "tl")
                self._add_view_button(controls, panel, "tr")
                self._add_view_button(controls, panel, "bl")
                self._add_view_button(controls, panel, "br", button_bottom=False)

            self.btn_log = ImageButton(
                panel,
                icon=img.getBitmap("icon/ico_chevron_up.png"),
                height=16,
                face_colour=t.btn_face_default,
                style=wx.ALIGN_CENTRE,
            )
            self.btn_log.SetToolTip(strings.TOOLTIP_LOG)
            outer.Add(
                self.btn_log,
                flag=wx.BOTTOM | wx.LEFT | wx.RIGHT,
                border=t.border_default,
            )

    def _add_view_button(
        self,
        sizer: wx.BoxSizer,
        parent: wx.Panel,
        suffix: str,
        label_top: bool = True,
        button_bottom: bool = True,
    ) -> None:
        """
        Add one viewport label and selection button.

        :param sizer: Vertical sizer receiving the controls.
        :param parent: Parent panel for the controls.
        :param suffix: Attribute suffix identifying the viewport.
        :param label_top: Include the label's top border.
        :param button_bottom: Include the button's bottom border.
        """
        label = wx.StaticText(parent, label=strings.LBL_VIEW_BTN)
        label.SetForegroundColour(self._theme.fg_viewport)
        setattr(self, f"lbl_secom_view_{suffix}", label)

        with vbox() as label_sizer:
            flags = wx.BOTTOM
            if label_top:
                flags |= wx.TOP
            label_sizer.Add(label, flag=flags, border=self._theme.border_tiny)
            sizer.Add(label_sizer, flag=wx.RIGHT | wx.ALIGN_RIGHT, border=18)

        button = ViewButton(parent, face_colour=self._theme.btn_face_default)
        setattr(self, f"btn_secom_view_{suffix}", button)
        flags = wx.ALIGN_RIGHT
        border = 0
        if button_bottom:
            flags |= wx.BOTTOM
            border = 6
        sizer.Add(button, flag=flags, border=border)

    def _build_viewport_grid(self, root_sizer: wx.BoxSizer) -> None:
        """
        Build the four localization viewports.

        :param root_sizer: Root horizontal sizer.
        """
        t = self._theme
        self.pnl_secom_grid = ViewportGrid(self)
        root_sizer.Add(self.pnl_secom_grid, proportion=1, flag=wx.EXPAND)

        self.vp_secom_tl = FeatureOverviewViewport(self.pnl_secom_grid)
        self.vp_secom_tr = MicroscopeViewport(self.pnl_secom_grid)
        self.vp_secom_bl = LiveViewport(self.pnl_secom_grid)
        self.vp_secom_br = LiveViewport(self.pnl_secom_grid)

        for viewport in (
            self.vp_secom_tl,
            self.vp_secom_tr,
            self.vp_secom_bl,
            self.vp_secom_br,
        ):
            viewport.SetForegroundColour(t.fg_viewport)
            viewport.SetBackgroundColour(t.bg_base)

    def _build_right_panel(self, root_sizer: wx.BoxSizer) -> None:
        """
        Build the scrollable fold-panel column.

        :param root_sizer: Root horizontal sizer.
        """
        t = self._theme
        panel = wx.Panel(self, size=(400, -1), style=wx.BORDER_NONE)
        panel.SetBackgroundColour(t.bg_main)
        root_sizer.Add(panel, flag=wx.EXPAND)

        with vbox() as panel_sizer:
            panel.SetSizer(panel_sizer)

            self.scr_win_right = wx.ScrolledWindow(
                panel,
                size=(400, -1),
                style=wx.VSCROLL,
            )
            self.scr_win_right.SetBackgroundColour(t.bg_main)
            self.scr_win_right.EnableScrolling(False, True)
            self.scr_win_right.SetScrollbars(-1, 10, 1, 1)
            panel_sizer.Add(self.scr_win_right, proportion=1, flag=wx.EXPAND)
            panel_sizer.SetItemMinSize(self.scr_win_right, 400, 400)

            with vbox() as scroll_sizer:
                self.scr_win_right.SetSizer(scroll_sizer)

                fold_bar = FoldPanelBar(self.scr_win_right)
                fold_bar.SetBackgroundColour(t.bg_main)
                scroll_sizer.Add(fold_bar, flag=wx.EXPAND)

                self._build_feature_panel(fold_bar)
                self._build_optical_settings_panel(fold_bar)
                self._build_streams_panel(fold_bar)
                self._build_acquisitions_panel(fold_bar)
                self._build_automation_panel(fold_bar)
                self._build_acquired_panel(fold_bar)

                self._build_milling_row(scroll_sizer)

    def _make_combo(
        self,
        parent: wx.Window,
        size: tuple[int, int],
        style: int,
    ) -> wx.adv.OwnerDrawnComboBox:
        """
        Create an owner-drawn combo matching the custom XRC handler.

        :param parent: Parent window.
        :param size: Initial control size.
        :param style: wx control style.
        :return: Configured combo box.
        """
        combo = wx.adv.OwnerDrawnComboBox(parent, size=size, style=style)
        combo.SetButtonBitmaps(img.getBitmap("button/btn_down.png"), pushButtonBg=False)
        combo.SetForegroundColour(self._theme.fg_editable)
        combo.SetBackgroundColour(self._theme.bg_main)
        return combo

    def _build_feature_panel(self, fold_bar: FoldPanelBar) -> None:
        """
        Build feature and Z-localization controls.

        :param fold_bar: Parent fold-panel bar.
        """
        t = self._theme
        self.fp_feature_panel = FoldPanelItem(
            fold_bar,
            label=strings.LBL_FEATURES,
        )
        self.fp_feature_panel.SetForegroundColour(t.fg_caption)
        self.fp_feature_panel.SetBackgroundColour(t.bg_separator)

        self.pnl_features = wx.Panel(self.fp_feature_panel)
        self.pnl_features.SetBackgroundColour(t.bg_main)

        with vbox() as sizer:
            self.pnl_features.SetSizer(sizer)
            self._build_feature_selection_rows(sizer)
            self._build_z_localization_row(sizer)
            self._build_target_size_rows(sizer)
            self._build_target_selection_rows(sizer)

        self.fp_feature_panel.add_item(self.pnl_features)
        fold_bar.add_item(self.fp_feature_panel)

    def _build_feature_selection_rows(self, sizer: wx.BoxSizer) -> None:
        """
        Build feature selection, status, and focus-position rows.

        :param sizer: Feature panel sizer.
        """
        t = self._theme
        panel = self.pnl_features

        with hbox() as row:
            sizer.Add(row, flag=wx.LEFT | wx.TOP, border=t.border_default)

            self.btn_delete_feature = ImageButton(
                panel,
                icon=img.getBitmap("icon/ico_trash.png"),
                height=16,
                style=wx.ALIGN_CENTRE,
            )
            row.Add(self.btn_delete_feature)

            self.cmb_features = self._make_combo(
                panel,
                size=(145, 20),
                style=wx.BORDER_NONE | wx.CB_DROPDOWN | wx.TE_PROCESS_ENTER,
            )
            row.Add(self.cmb_features)

            self.btn_create_move_feature = ImageTextButton(
                panel,
                height=24,
                label=strings.BTN_CREATE_MOVE,
                style=wx.ALIGN_CENTRE,
            )
            self.btn_create_move_feature.SetForegroundColour(wx.WHITE)
            self.btn_create_move_feature.SetBackgroundColour(t.bg_main)
            row.Add(
                self.btn_create_move_feature,
                flag=wx.LEFT | wx.ALIGN_CENTER_VERTICAL,
                border=52,
            )
            row.SetItemMinSize(self.btn_create_move_feature, 120, 24)

        with hbox() as row:
            sizer.Add(row, flag=wx.LEFT | wx.TOP, border=t.border_default)

            label = wx.StaticText(panel, label=strings.LBL_STATUS)
            label.SetForegroundColour(t.fg_subtle)
            row.Add(label)

            self.cmb_feature_status = self._make_combo(
                panel,
                size=(122, 16),
                style=(
                    wx.BORDER_NONE
                    | wx.CB_DROPDOWN
                    | wx.CB_READONLY
                    | wx.TE_PROCESS_ENTER
                ),
            )
            row.Add(self.cmb_feature_status, flag=wx.LEFT, border=t.border_default)

            self.btn_go_to_feature = ImageTextButton(
                panel,
                height=24,
                label=strings.BTN_GO_TO_FEATURE,
                style=wx.ALIGN_CENTRE,
            )
            self.btn_go_to_feature.SetForegroundColour(wx.WHITE)
            self.btn_go_to_feature.SetBackgroundColour(t.bg_main)
            row.Add(
                self.btn_go_to_feature,
                flag=wx.LEFT | wx.ALIGN_CENTER_VERTICAL,
                border=52,
            )
            row.SetItemMinSize(self.btn_go_to_feature, 120, 24)

        with hbox() as row:
            sizer.Add(
                row,
                flag=wx.LEFT | wx.TOP | wx.BOTTOM,
                border=t.border_default,
            )

            self.lbl_feature_z = wx.StaticText(panel, label="Feature Z")
            self.lbl_feature_z.SetForegroundColour(t.fg_subtle)
            row.Add(self.lbl_feature_z)

            self.ctrl_feature_z = UnitFloatCtrl(
                panel,
                size=(-1, 15),
                accuracy=5,
                key_step=0.001,
                unit="m",
            )
            self.ctrl_feature_z.SetBackgroundColour(t.bg_main)
            row.Add(self.ctrl_feature_z, flag=wx.LEFT, border=t.border_default)

            self.btn_use_current_z = ImageTextButton(
                panel,
                height=24,
                label="Use Current Z",
                style=wx.ALIGN_CENTRE,
            )
            self.btn_use_current_z.SetBackgroundColour(t.bg_base)
            self.btn_use_current_z.SetToolTip(
                "Save the current position of the focus as the feature Z position"
            )
            row.Add(self.btn_use_current_z, flag=wx.LEFT, border=65)

    def _build_z_localization_row(self, sizer: wx.BoxSizer) -> None:
        """
        Build the localization stream menu, action button, and progress controls.

        :param sizer: Feature panel sizer.
        """
        panel = self.pnl_features
        with hbox() as row:
            sizer.Add(
                row,
                flag=wx.LEFT | wx.BOTTOM | wx.RIGHT | wx.EXPAND,
                border=self._theme.border_default,
            )

            self.menu_localization_streams = ImageToggleButton(
                panel,
                icon=img.getBitmap("icon/arr_down_s.png"),
                height=24,
                size=(20, 24),
                face_colour=self._theme.btn_face_default,
                label="",
            )
            self.menu_localization_streams.SetForegroundColour("#1A1A1A")
            row.Add(
                self.menu_localization_streams,
                flag=wx.RIGHT,
                border=1,
            )

            self.btn_z_localization = ImageTextButton(
                panel,
                height=24,
                label="Locate Z...",
                style=wx.ALIGN_CENTRE,
            )
            self.btn_z_localization.SetBackgroundColour(self._theme.bg_base)
            row.Add(self.btn_z_localization, flag=wx.RIGHT, border=2)

            self.lbl_z_localization = wx.StaticText(
                panel,
                label="~ 4 seconds",
                style=wx.ALIGN_CENTRE,
            )
            self.lbl_z_localization.SetForegroundColour(self._theme.fg_subtle)
            row.Add(self.lbl_z_localization, flag=wx.TOP, border=3)

            self.gauge_z_localization = wx.Gauge(
                panel,
                range=100,
                size=(-1, 10),
                style=wx.GA_HORIZONTAL | wx.GA_SMOOTH,
            )
            self.gauge_z_localization.Hide()
            row.Add(
                self.gauge_z_localization,
                proportion=1,
                flag=wx.TOP,
                border=4,
            )

    def _build_target_size_rows(self, sizer: wx.BoxSizer) -> None:
        """
        Build fiducial and point-of-interest size selectors.

        :param sizer: Feature panel sizer.
        """
        panel = self.pnl_features
        entries = (
            ("lbl_fiducial_size", "Fiducial size", "cmb_fiducial_size", 10),
            ("lbl_poi_size", "POI size     ", "cmb_poi_size", 17),
        )
        for label_attr, label_text, combo_attr, combo_border in entries:
            with hbox() as row:
                sizer.Add(
                    row,
                    flag=wx.LEFT | wx.BOTTOM,
                    border=self._theme.border_default,
                )

                label = wx.StaticText(panel, label=label_text)
                label.SetForegroundColour(self._theme.fg_subtle)
                setattr(self, label_attr, label)
                row.Add(label)

                combo = self._make_combo(
                    panel,
                    size=(92, 16),
                    style=(
                        wx.BORDER_NONE
                        | wx.CB_DROPDOWN
                        | wx.CB_READONLY
                        | wx.TE_PROCESS_ENTER
                    ),
                )
                setattr(self, combo_attr, combo)
                row.Add(combo, flag=wx.LEFT, border=combo_border)

    def _build_target_selection_rows(self, sizer: wx.BoxSizer) -> None:
        """
        Build target selection and target focus-position rows.

        :param sizer: Feature panel sizer.
        """
        panel = self.pnl_features
        with hbox() as row:
            sizer.Add(row, flag=wx.LEFT, border=self._theme.border_default)

            self.btn_delete_target = ImageButton(
                panel,
                icon=img.getBitmap("icon/ico_trash.png"),
                height=16,
                style=wx.ALIGN_CENTRE,
            )
            row.Add(self.btn_delete_target)

            self.cmb_targets = self._make_combo(
                panel,
                size=(145, 20),
                style=wx.BORDER_NONE | wx.CB_DROPDOWN | wx.TE_PROCESS_ENTER,
            )
            row.Add(self.cmb_targets)

            self.btn_go_to_target = ImageTextButton(
                panel,
                height=24,
                label="Go to Target Z",
                style=wx.ALIGN_CENTRE,
            )
            self.btn_go_to_target.SetBackgroundColour(self._theme.bg_base)
            row.Add(self.btn_go_to_target, flag=wx.LEFT, border=52)

        with hbox() as row:
            sizer.Add(
                row,
                flag=wx.LEFT | wx.TOP | wx.BOTTOM,
                border=self._theme.border_default,
            )

            self.lbl_target_z = wx.StaticText(panel, label="Target Z")
            self.lbl_target_z.SetForegroundColour(self._theme.fg_subtle)
            row.Add(self.lbl_target_z)

            self.ctrl_target_z = UnitFloatCtrl(
                panel,
                size=(-1, 15),
                accuracy=5,
                key_step=0.001,
                unit="m",
            )
            self.ctrl_target_z.SetBackgroundColour(self._theme.bg_main)
            row.Add(self.ctrl_target_z, flag=wx.LEFT, border=self._theme.border_default)

            self.btn_use_current_target_z = ImageTextButton(
                panel,
                height=24,
                label="Use Current Z ",
                style=wx.ALIGN_CENTRE,
            )
            self.btn_use_current_target_z.SetBackgroundColour(self._theme.bg_base)
            self.btn_use_current_target_z.SetToolTip(
                "Save the current position of the focus as the target Z position"
            )
            row.Add(self.btn_use_current_target_z, flag=wx.LEFT, border=73)

    def _build_optical_settings_panel(self, fold_bar: FoldPanelBar) -> None:
        """
        Build the initially empty optical-settings section.

        :param fold_bar: Parent fold-panel bar.
        """
        self.fp_settings_secom_optical = FoldPanelItem(
            fold_bar,
            label=strings.LBL_OPTICAL_SETTINGS,
        )
        self.fp_settings_secom_optical.SetForegroundColour(self._theme.fg_caption)
        self.fp_settings_secom_optical.SetBackgroundColour(self._theme.bg_separator)
        fold_bar.add_item(self.fp_settings_secom_optical)

    def _build_streams_panel(self, fold_bar: FoldPanelBar) -> None:
        """
        Build the live-stream section.

        :param fold_bar: Parent fold-panel bar.
        """
        self.fp_secom_streams = FoldPanelItem(
            fold_bar,
            label=strings.LBL_STREAMS,
        )
        self.fp_secom_streams.SetForegroundColour(self._theme.fg_caption)
        self.fp_secom_streams.SetBackgroundColour(self._theme.bg_separator)

        self.pnl_secom_streams = StreamBar(
            self.fp_secom_streams,
            size=(300, -1),
            add_button=True,
        )
        self.pnl_secom_streams.SetForegroundColour(self._theme.fg_stream_bar)
        self.pnl_secom_streams.SetBackgroundColour(self._theme.bg_main)
        self.pnl_secom_streams.btn_add_stream.SetBackgroundColour(
            self.pnl_secom_streams.GetBackgroundColour()
        )

        self.fp_secom_streams.add_item(self.pnl_secom_streams)
        fold_bar.add_item(self.fp_secom_streams)

    def _build_acquisitions_panel(self, fold_bar: FoldPanelBar) -> None:
        """
        Build acquisition controls, including Z-stack inputs.

        :param fold_bar: Parent fold-panel bar.
        """
        self.fp_acquisitions = FoldPanelItem(
            fold_bar,
            label=strings.LBL_ACQUISITIONS,
        )
        self.fp_acquisitions.SetForegroundColour(self._theme.fg_caption)
        self.fp_acquisitions.SetBackgroundColour(self._theme.bg_separator)

        panel = wx.Panel(
            self.fp_acquisitions,
            size=(400, -1),
            style=wx.BORDER_NONE,
        )
        panel.SetBackgroundColour(self._theme.bg_main)

        with vbox() as sizer:
            panel.SetSizer(sizer)
            self._build_stream_checklist(panel, sizer)
            self._build_z_stack_controls(panel, sizer)
            self._build_filename_row(panel, sizer)
            self._build_acquisition_progress(panel, sizer)

            self.btn_acquire_overview = ImageTextButton(
                panel,
                height=48,
                face_colour=self._theme.btn_face_default,
                label=strings.BTN_ACQUIRE_OVERVIEW,
                style=wx.ALIGN_CENTRE,
            )
            font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
            font.SetPointSize(14)
            self.btn_acquire_overview.SetFont(font)
            sizer.Add(
                self.btn_acquire_overview,
                flag=wx.TOP | wx.BOTTOM | wx.LEFT,
                border=self._theme.border_default,
            )

        self.fp_acquisitions.add_item(panel)
        fold_bar.add_item(self.fp_acquisitions)

    def _build_stream_checklist(
        self,
        parent: wx.Panel,
        sizer: wx.BoxSizer,
    ) -> None:
        """
        Build the acquisition stream checklist.

        :param parent: Acquisition panel.
        :param sizer: Acquisition panel sizer.
        """
        self.streams_chk_list = wx.CheckListBox(parent)
        font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        font.SetPointSize(10)
        self.streams_chk_list.SetFont(font)
        sizer.Add(
            self.streams_chk_list,
            proportion=1,
            flag=wx.RIGHT | wx.LEFT | wx.EXPAND,
            border=self._theme.border_default,
        )

    def _build_z_stack_controls(
        self,
        parent: wx.Panel,
        sizer: wx.BoxSizer,
    ) -> None:
        """
        Build the Z-stack enable checkbox and range controls.

        :param parent: Acquisition panel.
        :param sizer: Acquisition panel sizer.
        """
        with vbox() as checkbox_sizer:
            sizer.Add(checkbox_sizer, flag=wx.LEFT, border=5)
            self.z_stack_chkbox = wx.CheckBox(
                parent,
                label="Z-stack acquisition",
            )
            self.z_stack_chkbox.SetForegroundColour(self._theme.fg_label)
            checkbox_sizer.Add(
                self.z_stack_chkbox,
                flag=wx.TOP,
                border=self._theme.border_default,
            )

        with hbox() as controls:
            sizer.Add(controls, flag=wx.TOP, border=9)
            entries = (
                ("Zmin =", "param_Zmin", 10.0, -1000, 0, 25),
                ("Zstep =", "param_Zstep", 10.0, -100, 100, 1),
                ("Zmax =", "param_Zmax", 1.0, 0, 1000, -5),
            )
            for label_text, attr, value, minimum, maximum, left_border in entries:
                grid = wx.FlexGridSizer(rows=1, cols=2, vgap=3, hgap=6)
                grid.AddGrowableCol(1)
                controls.Add(grid, flag=wx.LEFT, border=left_border)

                label = wx.StaticText(parent, label=label_text)
                label.SetForegroundColour(self._theme.fg_label)
                grid.Add(label, flag=wx.TOP, border=3)

                ctrl = UnitFloatCtrl(
                    parent,
                    value=value,
                    size=(-1, 15),
                    key_step=0.000001,
                    min_val=minimum,
                    max_val=maximum,
                    unit="m",
                    accuracy=4,
                    style=wx.BORDER_NONE,
                )
                font = wx.Font(
                    8,
                    wx.FONTFAMILY_DEFAULT,
                    wx.FONTSTYLE_NORMAL,
                    wx.FONTWEIGHT_NORMAL,
                )
                ctrl.SetFont(font)
                setattr(self, attr, ctrl)
                grid.Add(ctrl, flag=wx.TOP, border=3)

    def _build_filename_row(
        self,
        parent: wx.Panel,
        sizer: wx.BoxSizer,
    ) -> None:
        """
        Build the destination filename row.

        :param parent: Acquisition panel.
        :param sizer: Acquisition panel sizer.
        """
        with hbox() as row:
            sizer.Add(
                row,
                flag=wx.TOP | wx.LEFT | wx.RIGHT | wx.EXPAND,
                border=self._theme.border_default,
            )

            label = wx.StaticText(parent, label=strings.LBL_FILENAME)
            label.SetForegroundColour(self._theme.fg_label)
            row.Add(label, flag=wx.ALIGN_CENTER_VERTICAL)

            self.txt_filename = wx.TextCtrl(
                parent,
                value=strings.TXT_PROJECT_PATH_DEFAULT,
                size=(-1, 20),
                style=wx.BORDER_NONE | wx.TE_READONLY,
            )
            self.txt_filename.SetForegroundColour(self._theme.fg_editable)
            self.txt_filename.SetBackgroundColour(self._theme.bg_main)
            row.Add(
                self.txt_filename,
                proportion=1,
                flag=wx.LEFT | wx.EXPAND,
                border=5,
            )

            self.btn_cryosecom_change_file = ImageTextButton(
                parent,
                height=24,
                face_colour=self._theme.btn_face_default,
                label=strings.BTN_CHANGE_FILE,
            )
            row.Add(self.btn_cryosecom_change_file, flag=wx.LEFT, border=5)

    def _build_acquisition_progress(
        self,
        parent: wx.Panel,
        sizer: wx.BoxSizer,
    ) -> None:
        """
        Build the acquisition action and progress row.

        :param parent: Acquisition panel.
        :param sizer: Acquisition panel sizer.
        """
        grid = wx.FlexGridSizer(rows=1, cols=3, vgap=0, hgap=5)
        grid.AddGrowableCol(1)
        sizer.Add(
            grid,
            flag=wx.ALL | wx.EXPAND,
            border=self._theme.border_default,
        )

        self.btn_cryosecom_acquire = ImageTextButton(
            parent,
            icon=img.getBitmap("icon/ico_acqui.png"),
            height=48,
            face_colour=self._theme.btn_face_primary,
            label=strings.BTN_ACQUIRE,
            style=wx.ALIGN_CENTRE,
        )
        self.btn_cryosecom_acquire.SetForegroundColour(wx.WHITE)
        font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        font.SetPointSize(15)
        self.btn_cryosecom_acquire.SetFont(font)
        grid.Add(
            self.btn_cryosecom_acquire,
            flag=wx.ALL | wx.EXPAND,
            border=2,
        )

        with hbox() as estimated_sizer:
            grid.Add(estimated_sizer, flag=wx.TOP, border=17)
            self.txt_cryosecom_est_time = wx.StaticText(
                parent,
                label=strings.LBL_ESTIMATED_TIME,
            )
            self.txt_cryosecom_est_time.SetForegroundColour(self._theme.fg_label)
            self.txt_cryosecom_est_time.Hide()
            estimated_sizer.Add(self.txt_cryosecom_est_time, flag=wx.LEFT, border=-2)

        with hbox() as progress_sizer:
            grid.Add(progress_sizer, flag=wx.EXPAND)

            with vbox() as gauge_sizer:
                progress_sizer.Add(gauge_sizer, flag=wx.TOP, border=-8)

                self.gauge_cryosecom_acq = wx.Gauge(
                    parent,
                    range=100,
                    size=(-1, 10),
                    style=wx.GA_SMOOTH,
                )
                gauge_sizer.Add(
                    self.gauge_cryosecom_acq,
                    proportion=1,
                    flag=wx.TOP,
                    border=self._theme.border_default,
                )

                self.txt_cryosecom_left_time = wx.StaticText(parent, label="")
                self.txt_cryosecom_left_time.SetForegroundColour(self._theme.fg_label)
                self.txt_cryosecom_left_time.Hide()
                gauge_sizer.Add(
                    self.txt_cryosecom_left_time,
                    proportion=1,
                    flag=wx.TOP,
                    border=self._theme.border_default,
                )

            self.btn_cryosecom_acqui_cancel = ImageTextButton(
                parent,
                height=24,
                face_colour=self._theme.btn_face_default,
                label="cancel",
            )
            progress_sizer.Add(
                self.btn_cryosecom_acqui_cancel,
                flag=wx.TOP,
                border=12,
            )

    def _build_automation_panel(self, fold_bar: FoldPanelBar) -> None:
        """
        Build advanced acquisition-at-features controls.

        :param fold_bar: Parent fold-panel bar.
        """
        self.fp_automation = FoldPanelItem(fold_bar)

        panel = wx.Panel(self.fp_automation)
        with vbox() as sizer:
            panel.SetSizer(sizer)

            self.acquire_features_chk_list = wx.CheckListBox(panel)
            font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
            font.SetPointSize(10)
            self.acquire_features_chk_list.SetFont(font)
            sizer.Add(
                self.acquire_features_chk_list,
                proportion=1,
                flag=wx.RIGHT | wx.LEFT | wx.EXPAND,
                border=self._theme.border_default,
            )

            self.chk_use_autofocus_acquire_features = wx.CheckBox(
                panel,
                label="AutoFocus before acquiring at features",
            )
            self.chk_use_autofocus_acquire_features.SetForegroundColour(
                self._theme.fg_label
            )
            sizer.Add(
                self.chk_use_autofocus_acquire_features,
                flag=wx.LEFT,
                border=15,
            )

            self.btn_acquire_features = ImageTextButton(
                panel,
                icon=img.getBitmap("icon/ico_acqui.png"),
                height=48,
                face_colour=self._theme.btn_face_primary,
                label="ACQUIRE AT FEATURES",
                style=wx.ALIGN_CENTRE,
            )
            font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
            font.SetPointSize(14)
            self.btn_acquire_features.SetFont(font)
            sizer.Add(
                self.btn_acquire_features,
                flag=wx.TOP | wx.BOTTOM | wx.LEFT,
                border=self._theme.border_default,
            )

            self.txt_acquire_features_est_time = wx.StaticText(
                panel,
                label=strings.LBL_ESTIMATED_TIME,
            )
            self.txt_acquire_features_est_time.SetForegroundColour(
                self._theme.fg_label
            )
            self.txt_acquire_features_est_time.Hide()
            sizer.Add(
                self.txt_acquire_features_est_time,
                flag=wx.LEFT,
                border=15,
            )

        self.fp_automation.add_item(panel)
        fold_bar.add_item(self.fp_automation)

    def _build_acquired_panel(self, fold_bar: FoldPanelBar) -> None:
        """
        Build the acquired-stream section.

        :param fold_bar: Parent fold-panel bar.
        """
        item = FoldPanelItem(fold_bar, label=strings.LBL_ACQUIRED)
        item.SetForegroundColour(self._theme.fg_caption)
        item.SetBackgroundColour(self._theme.bg_separator)

        self.pnl_cryosecom_acquired = StreamBar(
            item,
            size=(300, -1),
            add_button=False,
        )
        self.pnl_cryosecom_acquired.SetForegroundColour(
            self._theme.fg_stream_bar
        )
        self.pnl_cryosecom_acquired.SetBackgroundColour(self._theme.bg_main)

        item.add_item(self.pnl_cryosecom_acquired)
        fold_bar.add_item(item)

    def _build_milling_row(self, sizer: wx.BoxSizer) -> None:
        """
        Build the legacy milling progress row below the fold-panel bar.

        :param sizer: Scrolled-window sizer.
        """
        grid = wx.FlexGridSizer(rows=1, cols=3, vgap=0, hgap=5)
        grid.AddGrowableCol(1)
        sizer.Add(grid, flag=wx.EXPAND)

        button = ImageTextButton(
            self.scr_win_right,
            icon=img.getBitmap("icon/ico_sem.png"),
            height=48,
            face_colour=self._theme.btn_face_primary,
            label="MILL",
            style=wx.ALIGN_CENTRE,
        )
        button.SetForegroundColour(wx.WHITE)
        font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        font.SetPointSize(15)
        button.SetFont(font)
        button.Hide()
        grid.Add(
            button,
            flag=wx.ALL | wx.EXPAND,
            border=self._theme.border_default,
        )

        with hbox() as estimated_sizer:
            grid.Add(estimated_sizer, flag=wx.TOP, border=17)
            estimated = wx.StaticText(
                self.scr_win_right,
                label=strings.LBL_ESTIMATED_TIME,
            )
            estimated.SetForegroundColour(self._theme.fg_label)
            estimated_sizer.Add(estimated, flag=wx.LEFT, border=-2)

        with hbox() as progress_sizer:
            grid.Add(progress_sizer, flag=wx.EXPAND)

            with vbox() as gauge_sizer:
                progress_sizer.Add(gauge_sizer, flag=wx.TOP, border=-8)
                gauge = wx.Gauge(
                    self.scr_win_right,
                    range=100,
                    size=(-1, 10),
                    style=wx.GA_SMOOTH,
                )
                gauge.Hide()
                gauge_sizer.Add(
                    gauge,
                    proportion=1,
                    flag=wx.TOP,
                    border=self._theme.border_default,
                )

                left_time = wx.StaticText(self.scr_win_right, label="")
                left_time.SetForegroundColour(self._theme.fg_label)
                gauge_sizer.Add(
                    left_time,
                    proportion=1,
                    flag=wx.TOP,
                    border=self._theme.border_default,
                )

            cancel = ImageTextButton(
                self.scr_win_right,
                height=24,
                face_colour=self._theme.btn_face_default,
                label="cancel",
            )
            cancel.Hide()
            progress_sizer.Add(cancel, flag=wx.TOP, border=12)


if __name__ == "__main__":
    from odemis.gui.layout.util.preview import run_preview

    run_preview(PnlTabLocalization)
