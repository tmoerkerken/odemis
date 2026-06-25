# -*- coding: utf-8 -*-
"""
Layout definition for the CryoSECOM chamber tab panel.

Replaces panel_tab_cryosecom_chamber.xrc.

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

from odemis.acq.move import (
    COATING,
    FIB_IMAGING,
    FM_IMAGING,
    GRID_1,
    GRID_2,
    LOADING,
    MILLING,
    POSITION_NAMES,
    SEM_IMAGING,
    THREE_BEAMS,
)
from odemis.gui import img
from odemis.gui.comp.buttons import (
    ImageButton,
    ImageTextButton,
    ImageTextToggleButton,
    ProgressRadioButton,
)
from odemis.gui.comp.slider import UnitFloatSlider
from odemis.gui.comp.text import UnitFloatCtrl
from odemis.gui.comp.viewport import FeatureOverviewViewport
from odemis.gui.layout.constants import strings
from odemis.gui.layout.constants.theme import DARK, Theme
from odemis.gui.layout.util.sizers import hbox, vbox


class PnlTabCryosecomChamber(wx.Panel):
    """
    Layout for the CryoSECOM chamber tab panel.

    Provides the same named widget attributes as the XRC-generated class so
    that the chamber tab controller can use this as a drop-in replacement.

    Attributes
    ----------
    txt_projectpath : wx.TextCtrl
        Read-only text control showing the current project destination path.
    btn_change_folder : ImageTextButton
        Button to create a new project / change destination folder.
    btn_load_project : ImageTextButton
        Button to load an existing project.
    btn_switch_sem_imaging : ProgressRadioButton
        Position switch button for SEM imaging.
    btn_switch_fm_imaging : ProgressRadioButton
        Position switch button for FM imaging.
    btn_switch_milling : ProgressRadioButton
        Position switch button for milling.
    btn_switch_fib_imaging : ProgressRadioButton
        Position switch button for FIB imaging.
    btn_switch_grid1 : ProgressRadioButton
        Position switch button for Grid 1.
    btn_switch_grid2 : ProgressRadioButton
        Position switch button for Grid 2.
    btn_switch_loading : ProgressRadioButton
        Position switch button for loading position.
    btn_switch_imaging : ProgressRadioButton
        Position switch button for 3-beam imaging.
    btn_switch_zero_tilt_imaging : ProgressRadioButton
        Position switch button for zero-tilt SEM imaging.
    btn_switch_coating : ProgressRadioButton
        Position switch button for coating.
    btn_switch_loading_chamber_tab : ProgressRadioButton
        Loading position button for the chamber tab.
    btn_switch_optical_chamber_tab : ProgressRadioButton
        Optical position button for the chamber tab.
    btn_switch_milling_chamber_tab : ProgressRadioButton
        FIB/milling position button for the chamber tab.
    btn_switch_coating_chamber_tab : ProgressRadioButton
        Coating position button for the chamber tab.
    gauge_move : wx.Gauge
        Progress gauge displayed while a stage move is in progress.
    btn_cancel : ImageTextButton
        Button to cancel an in-progress stage move (initially disabled).
    pnl_ref_msg : wx.Panel
        Panel displaying a warning icon and message text.
    txt_warning : wx.StaticText
        Warning/status message text inside pnl_ref_msg.
    btn_switch_advanced : ImageTextToggleButton
        Toggle button that shows/hides the advanced alignment panel (initially hidden).
    pnl_advanced_align : wx.Panel
        Advanced alignment controls panel (initially hidden).
    lbl_milling_angle : wx.StaticText
        Label for the RX angle control.
    ctrl_rx : UnitFloatCtrl
        Float input for the RX (milling) angle in degrees.
    stage_align_slider_aligner : UnitFloatSlider
        Logarithmic slider controlling the jog step size in metres.
    lbl_py : wx.StaticText
        +Y axis direction label in the jog grid.
    lbl_my : wx.StaticText
        -Y axis direction label in the jog grid.
    lbl_px : wx.StaticText
        +X axis direction label in the jog grid.
    lbl_mx : wx.StaticText
        -X axis direction label in the jog grid.
    lbl_pz : wx.StaticText
        +Z axis direction label in the jog grid.
    lbl_mz : wx.StaticText
        -Z axis direction label in the jog grid.
    stage_align_btn_p_aligner_y : ImageTextButton
        Jog button for +Y stage movement.
    stage_align_btn_m_aligner_y : ImageTextButton
        Jog button for -Y stage movement.
    stage_align_btn_p_aligner_x : ImageTextButton
        Jog button for +X stage movement.
    stage_align_btn_m_aligner_x : ImageTextButton
        Jog button for -X stage movement.
    stage_align_btn_p_aligner_z : ImageTextButton
        Jog button for +Z stage movement.
    stage_align_btn_m_aligner_z : ImageTextButton
        Jog button for -Z stage movement.
    btn_switch_align : ProgressRadioButton
        Button to trigger factory alignment (initially hidden).
    pnl_temperature : wx.Panel
        Temperature controls panel (initially hidden).
    ctrl_sample_heater : wx.CheckBox
        Checkbox to enable/disable the sample heater.
    ctrl_sample_target_tmp : UnitFloatCtrl
        Float input for the target sample temperature in degrees Celsius.
    btn_log : ImageButton
        Button to open/close the log panel.
    vp_overview_map : FeatureOverviewViewport
        Overview map viewport on the right side of the panel.
    """

    def __init__(self, parent: wx.Window, theme: Theme = DARK) -> None:
        """
        Initialise the panel and build the complete widget hierarchy.

        :param parent: Parent window.
        :param theme: Visual theme to apply. Defaults to DARK.
        """
        super().__init__(parent, style=wx.WANTS_CHARS)
        self._theme = theme
        self.SetBackgroundColour(theme.bg_main)

        font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        font.SetPointSize(theme.font_size_default)
        self.SetFont(font)

        self._build_layout()

    def _build_layout(self) -> None:
        """
        Construct the root horizontal sizer: left control panel and overview viewport.
        """
        with hbox() as root_sizer:
            self.SetSizer(root_sizer)

            left_panel = self._build_left_panel()
            root_sizer.Add(
                left_panel,
                flag=wx.ALL | wx.EXPAND,
                border=self._theme.border_default,
            )
            root_sizer.SetItemMinSize(left_panel, 400, -1)

            self.vp_overview_map = FeatureOverviewViewport(self)
            self.vp_overview_map.SetForegroundColour(self._theme.fg_viewport)
            self.vp_overview_map.SetBackgroundColour(self._theme.bg_base)
            root_sizer.Add(self.vp_overview_map, proportion=1, flag=wx.EXPAND)

    def _build_left_panel(self) -> wx.Panel:
        """
        Build and return the left control panel with all sub-panels.

        :return: Configured left wx.Panel instance.
        """
        t = self._theme
        panel = wx.Panel(self, size=(t.side_panel_width, -1))
        panel.SetBackgroundColour(t.bg_main)
        panel.SetForegroundColour(t.fg_label)

        with vbox() as sizer:
            panel.SetSizer(sizer)

            pnl_project = wx.Panel(panel)
            pnl_project.SetName("pnl_project")
            pnl_project.SetBackgroundColour(t.bg_panel)
            pnl_project.SetForegroundColour(t.fg_label)
            self._build_pnl_project(pnl_project)
            sizer.Add(pnl_project, flag=wx.BOTTOM | wx.EXPAND, border=t.border_small)

            pnl_switch = wx.Panel(panel)
            pnl_switch.SetName("pnl_switch_buttons")
            pnl_switch.SetBackgroundColour(t.bg_panel)
            pnl_switch.SetForegroundColour(t.fg_label)
            self._build_pnl_switch_buttons(pnl_switch)
            sizer.Add(pnl_switch, flag=wx.BOTTOM | wx.EXPAND, border=t.border_small)

            self.pnl_temperature = wx.Panel(panel)
            self.pnl_temperature.SetName("pnl_temperature")
            self.pnl_temperature.SetBackgroundColour(t.bg_panel)
            self.pnl_temperature.SetForegroundColour(t.fg_label)
            self._build_pnl_temperature()
            self.pnl_temperature.Show(False)
            sizer.Add(self.pnl_temperature, flag=wx.BOTTOM | wx.EXPAND, border=t.border_small)

            sizer.Add((0, 0), proportion=1, flag=wx.EXPAND)

            self.btn_log = ImageButton(
                panel,
                icon=img.getBitmap("icon/ico_chevron_up.png"),
                height=16,
                face_colour="def",
                style=wx.ALIGN_CENTRE,
            )
            self.btn_log.SetToolTip(strings.TOOLTIP_LOG)
            sizer.Add(self.btn_log)

        return panel

    def _build_pnl_project(self, panel: wx.Panel) -> None:
        """
        Populate the project panel with a header, path display, and action buttons.

        :param panel: The pnl_project wx.Panel to populate.
        """
        t = self._theme
        gb_sizer = wx.GridBagSizer(hgap=50)
        panel.SetSizer(gb_sizer)

        hdr_font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        hdr_font.SetPointSize(t.font_size_section_header)

        lbl_project = wx.StaticText(panel, label=strings.LBL_PROJECT)
        lbl_project.SetForegroundColour(t.fg_label)
        lbl_project.SetFont(hdr_font)
        gb_sizer.Add(
            lbl_project,
            pos=(0, 0),
            span=(1, 3),
            flag=wx.ALL | wx.EXPAND,
            border=t.border_default,
        )

        input_font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        input_font.SetPointSize(t.font_size_input)

        self.txt_projectpath = wx.TextCtrl(
            panel,
            value=strings.TXT_PROJECT_PATH_DEFAULT,
            style=wx.BORDER_NONE | wx.TE_READONLY,
        )
        self.txt_projectpath.SetForegroundColour(t.fg_project_path)
        self.txt_projectpath.SetBackgroundColour(t.bg_project_path)
        self.txt_projectpath.SetFont(input_font)
        gb_sizer.Add(
            self.txt_projectpath,
            pos=(1, 0),
            span=(1, 3),
            flag=wx.ALL | wx.EXPAND,
            border=t.border_default,
        )
        gb_sizer.AddGrowableCol(0)

        btn_font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        btn_font.SetPointSize(t.font_size_button_large)

        self.btn_change_folder = ImageTextButton(
            panel,
            height=24,
            face_colour="blue",
            label=strings.BTN_NEW_PROJECT,
            style=wx.ALIGN_CENTRE,
        )
        self.btn_change_folder.SetForegroundColour(t.fg_caption)
        self.btn_change_folder.SetFont(btn_font)
        gb_sizer.Add(
            self.btn_change_folder,
            pos=(2, 0),
            flag=wx.ALL | wx.EXPAND,
            border=t.border_default,
        )

        self.btn_load_project = ImageTextButton(
            panel,
            height=24,
            face_colour="blue",
            label=strings.BTN_LOAD_PROJECT,
            style=wx.ALIGN_CENTRE,
        )
        self.btn_load_project.SetForegroundColour(t.fg_caption)
        self.btn_load_project.SetFont(btn_font)
        gb_sizer.Add(
            self.btn_load_project,
            pos=(2, 1),
            flag=wx.ALL | wx.EXPAND,
            border=t.border_default,
        )

    def _build_pnl_switch_buttons(self, panel: wx.Panel) -> None:
        """
        Populate the position switch panel with position grids and supporting controls.

        :param panel: The pnl_switch_buttons wx.Panel to populate.
        """
        t = self._theme

        with vbox() as sizer:
            panel.SetSizer(sizer)

            hdr_font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
            hdr_font.SetPointSize(t.font_size_section_header)

            lbl_position = wx.StaticText(panel, label=strings.LBL_POSITION)
            lbl_position.SetForegroundColour(t.fg_label)
            lbl_position.SetFont(hdr_font)
            sizer.Add(lbl_position, flag=wx.BOTTOM | wx.ALL, border=t.border_default)

            meteor_grid = wx.GridBagSizer(vgap=5, hgap=20)
            self._build_switch_grid_meteor(panel, meteor_grid)
            sizer.Add(meteor_grid, flag=wx.ALL | wx.ALIGN_CENTRE)

            cryofib_grid = wx.GridBagSizer(vgap=5, hgap=20)
            self._build_switch_grid_cryofib(panel, cryofib_grid)
            sizer.Add(cryofib_grid, flag=wx.ALL | wx.ALIGN_CENTRE)

            chamber_grid = wx.GridBagSizer(vgap=5, hgap=20)
            self._build_switch_grid_chamber(panel, chamber_grid)
            sizer.Add(chamber_grid, flag=wx.ALL | wx.ALIGN_CENTRE)

            self._build_move_row(panel, sizer)
            self._build_pnl_ref_msg(panel, sizer)
            self._build_btn_switch_advanced(panel, sizer)
            self._build_pnl_advanced_align(panel, sizer)

    def _make_position_button(
        self,
        parent: wx.Window,
        attr_name: str,
        icon: str,
        icon_progress: str,
        icon_on: str,
        label: str,
        size: wx.Size = wx.DefaultSize,
    ) -> ProgressRadioButton:
        """
        Create a ProgressRadioButton and assign it to self.<attr_name>.

        :param parent: Parent window for the button.
        :param attr_name: Name of the instance attribute to assign the button to.
        :param icon: Path to the default (untoggled) icon, relative to img root.
        :param icon_progress: Path to the in-progress icon.
        :param icon_on: Path to the completed (on) icon.
        :param label: Button label text.
        :param size: Optional explicit button size; defaults to wx.DefaultSize.
        :return: The newly created ProgressRadioButton.
        """
        t = self._theme
        btn_font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        btn_font.SetPointSize(t.font_size_button_medium)

        btn = ProgressRadioButton(
            parent,
            icon=img.getBitmap(icon),
            icon_progress=img.getBitmap(icon_progress),
            icon_on=img.getBitmap(icon_on),
            height=48,
            face_colour="def",
            label=label,
            size=size,
            style=wx.ALIGN_CENTRE,
        )
        btn.SetForegroundColour(t.fg_caption)
        btn.SetFont(btn_font)
        btn.Show(False)
        setattr(self, attr_name, btn)
        return btn

    def _build_switch_grid_meteor(
        self, parent: wx.Panel, grid: wx.GridBagSizer
    ) -> None:
        """
        Populate the 3x2 Meteor position button grid.

        :param parent: Parent panel for the buttons.
        :param grid: GridBagSizer to add buttons into.
        """
        t = self._theme
        entries = [
            ("btn_switch_sem_imaging", "icon/ico_sem.png", "icon/ico_sem_orange.png",
             "icon/ico_sem_green.png", POSITION_NAMES[SEM_IMAGING], (0, 0)),
            ("btn_switch_fm_imaging", "icon/ico_meteorimaging.png",
             "icon/ico_meteorimaging_orange.png", "icon/ico_meteorimaging_green.png",
             POSITION_NAMES[FM_IMAGING], (0, 1)),
            ("btn_switch_milling", "icon/ico_milling.png", "icon/ico_milling_orange.png",
             "icon/ico_milling_green.png", POSITION_NAMES[MILLING], (1, 0)),
            ("btn_switch_fib_imaging", "icon/ico_imaging.png", "icon/ico_imaging_orange.png",
             "icon/ico_imaging_green.png", POSITION_NAMES[FIB_IMAGING], (1, 1)),
            ("btn_switch_grid1", "icon/ico_meteorgrid.png", "icon/ico_meteorgrid_orange.png",
             "icon/ico_meteorgrid_green.png", POSITION_NAMES[GRID_1], (2, 0)),
            ("btn_switch_grid2", "icon/ico_meteorgrid.png", "icon/ico_meteorgrid_orange.png",
             "icon/ico_meteorgrid_green.png", POSITION_NAMES[GRID_2], (2, 1)),
        ]
        for attr, icon, icon_prog, icon_on, label, pos in entries:
            btn = self._make_position_button(parent, attr, icon, icon_prog, icon_on, label)
            grid.Add(
                btn,
                pos=pos,
                flag=wx.ALL | wx.EXPAND,
                border=t.border_default,
            )

    def _build_switch_grid_cryofib(
        self, parent: wx.Panel, grid: wx.GridBagSizer
    ) -> None:
        """
        Populate the 2x2 CryoFIB position button grid.

        :param parent: Parent panel for the buttons.
        :param grid: GridBagSizer to add buttons into.
        """
        t = self._theme
        entries = [
            ("btn_switch_loading", "icon/ico_eject.png", "icon/ico_eject_orange.png",
             "icon/ico_eject_green.png", POSITION_NAMES[LOADING], (0, 0)),
            ("btn_switch_imaging", "icon/ico_imaging.png", "icon/ico_imaging_orange.png",
             "icon/ico_imaging_green.png", POSITION_NAMES[THREE_BEAMS], (0, 1)),
            ("btn_switch_zero_tilt_imaging", "icon/ico_sem.png", "icon/ico_sem_orange.png",
             "icon/ico_sem_green.png", POSITION_NAMES[SEM_IMAGING], (1, 0)),
            ("btn_switch_coating", "icon/ico_coating.png", "icon/ico_coating_orange.png",
             "icon/ico_coating_green.png", POSITION_NAMES[COATING], (1, 1)),
        ]
        for attr, icon, icon_prog, icon_on, label, pos in entries:
            btn = self._make_position_button(parent, attr, icon, icon_prog, icon_on, label)
            grid.Add(
                btn,
                pos=pos,
                flag=wx.ALL | wx.EXPAND,
                border=t.border_default,
            )

    def _build_switch_grid_chamber(
        self, parent: wx.Panel, grid: wx.GridBagSizer
    ) -> None:
        """
        Populate the 2x2 chamber-tab position button grid (fixed width 140px).

        :param parent: Parent panel for the buttons.
        :param grid: GridBagSizer to add buttons into.
        """
        t = self._theme
        btn_size = wx.Size(140, -1)
        entries = [
            ("btn_switch_loading_chamber_tab", "icon/ico_eject.png",
             "icon/ico_eject_orange.png", "icon/ico_eject_green.png",
             POSITION_NAMES[LOADING], (0, 0)),
            ("btn_switch_optical_chamber_tab", "icon/ico_optical.png",
             "icon/ico_optical_orange.png", "icon/ico_optical_green.png",
             strings.BTN_OPTICAL, (0, 1)),
            ("btn_switch_milling_chamber_tab", "icon/ico_sem.png",
             "icon/ico_sem_orange.png", "icon/ico_sem_green.png",
             strings.BTN_FIB, (1, 0)),
            ("btn_switch_coating_chamber_tab", "icon/ico_coating.png",
             "icon/ico_coating_orange.png", "icon/ico_coating_green.png",
             POSITION_NAMES[COATING], (1, 1)),
        ]
        for attr, icon, icon_prog, icon_on, label, pos in entries:
            btn = self._make_position_button(
                parent, attr, icon, icon_prog, icon_on, label, size=btn_size
            )
            grid.Add(
                btn,
                pos=pos,
                flag=wx.ALL | wx.EXPAND,
                border=t.border_default,
            )

    def _build_move_row(self, parent: wx.Panel, sizer: wx.BoxSizer) -> None:
        """
        Build the move-progress row containing a gauge and a cancel button.

        :param parent: Parent panel for the widgets.
        :param sizer: Parent VBox sizer to add the row into.
        """
        t = self._theme

        with hbox() as row:
            sizer.Add(row, flag=wx.ALIGN_CENTRE)

            self.gauge_move = wx.Gauge(
                parent,
                range=100,
                size=(150, 10),
                style=wx.GA_SMOOTH,
            )
            row.Add(
                self.gauge_move,
                proportion=1,
                flag=wx.TOP | wx.BOTTOM | wx.EXPAND,
                border=t.border_default,
            )

            self.btn_cancel = ImageTextButton(
                parent,
                height=24,
                face_colour="def",
                label=strings.BTN_CANCEL,
                style=wx.ALIGN_CENTRE,
            )
            self.btn_cancel.Enable(False)
            row.Add(self.btn_cancel, flag=wx.LEFT, border=t.border_default)

    def _build_pnl_ref_msg(self, parent: wx.Panel, sizer: wx.BoxSizer) -> None:
        """
        Build the reference/warning message panel with an icon and text.

        :param parent: Parent panel for pnl_ref_msg.
        :param sizer: Parent VBox sizer to add the panel into.
        """
        t = self._theme

        self.pnl_ref_msg = wx.Panel(parent)
        self.pnl_ref_msg.SetName("pnl_ref_msg")
        self.pnl_ref_msg.SetBackgroundColour(t.bg_panel)

        with hbox() as msg_sizer:
            self.pnl_ref_msg.SetSizer(msg_sizer)

            warning_bmp = wx.StaticBitmap(
                self.pnl_ref_msg,
                bitmap=img.getBitmap("icon/dialog_warning.png"),
            )
            msg_sizer.Add(warning_bmp, flag=wx.RIGHT, border=t.border_small)

            self.txt_warning = wx.StaticText(
                self.pnl_ref_msg,
                size=(-1, 20),
            )
            self.txt_warning.SetForegroundColour(t.fg_label)
            msg_sizer.Add(self.txt_warning, proportion=1, flag=wx.EXPAND)

        sizer.Add(
            self.pnl_ref_msg,
            flag=wx.ALL | wx.EXPAND,
            border=t.border_default,
        )

    def _build_btn_switch_advanced(
        self, parent: wx.Panel, sizer: wx.BoxSizer
    ) -> None:
        """
        Build the advanced-toggle button (initially hidden).

        :param parent: Parent panel for the button.
        :param sizer: Parent VBox sizer to add the button into.
        """
        t = self._theme
        btn_font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        btn_font.SetPointSize(t.font_size_button_medium)

        self.btn_switch_advanced = ImageTextToggleButton(
            parent,
            icon=img.getBitmap("icon/arr_down_s.png"),
            icon_on=img.getBitmap("icon/arr_down_s.png"),
            height=48,
            face_colour="def",
            label=strings.BTN_ADVANCED,
            style=wx.ALIGN_CENTRE,
        )
        self.btn_switch_advanced.SetForegroundColour(t.fg_caption)
        self.btn_switch_advanced.SetFont(btn_font)
        self.btn_switch_advanced.Show(False)
        sizer.Add(self.btn_switch_advanced, flag=wx.ALL, border=t.border_default)

    def _build_pnl_advanced_align(
        self, parent: wx.Panel, sizer: wx.BoxSizer
    ) -> None:
        """
        Build the advanced alignment panel with stage jog controls (initially hidden).

        :param parent: Parent panel for pnl_advanced_align.
        :param sizer: Parent VBox sizer to add the panel into.
        """
        t = self._theme

        self.pnl_advanced_align = wx.Panel(parent)
        self.pnl_advanced_align.SetName("pnl_advanced_align")
        self.pnl_advanced_align.SetBackgroundColour(t.bg_panel)
        self.pnl_advanced_align.SetForegroundColour(t.fg_label)
        self.pnl_advanced_align.Show(False)

        with vbox() as adv_sizer:
            self.pnl_advanced_align.SetSizer(adv_sizer)

            hdr_font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
            hdr_font.SetPointSize(t.font_size_section_header)
            input_font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
            input_font.SetPointSize(t.font_size_input)

            lbl_stage = wx.StaticText(self.pnl_advanced_align, label=strings.LBL_STAGE)
            lbl_stage.SetForegroundColour(t.fg_label)
            lbl_stage.SetFont(hdr_font)
            adv_sizer.Add(lbl_stage, flag=wx.BOTTOM | wx.ALL, border=t.border_small)

            with hbox() as angle_row:
                adv_sizer.Add(angle_row, flag=wx.ALIGN_CENTRE)

                self.lbl_milling_angle = wx.StaticText(
                    self.pnl_advanced_align,
                    label=strings.LBL_RX_ANGLE,
                )
                self.lbl_milling_angle.SetForegroundColour(t.fg_viewport)
                self.lbl_milling_angle.SetFont(input_font)
                angle_row.Add(
                    self.lbl_milling_angle,
                    flag=wx.TOP | wx.LEFT,
                    border=25,
                )

                self.ctrl_rx = UnitFloatCtrl(
                    self.pnl_advanced_align,
                    value=10,
                    accuracy=3,
                    key_step=0.1,
                    unit="°",
                    size=(-1, 20),
                    style=wx.BORDER_NONE,
                )
                self.ctrl_rx.SetFont(input_font)
                angle_row.Add(
                    self.ctrl_rx,
                    flag=wx.LEFT | wx.TOP | wx.BOTTOM,
                    border=25,
                )

            with hbox() as step_row:
                adv_sizer.Add(
                    step_row,
                    flag=wx.LEFT | wx.RIGHT | wx.EXPAND,
                    border=t.border_small,
                )

                lbl_step = wx.StaticText(
                    self.pnl_advanced_align,
                    label=strings.LBL_STEP_SIZE,
                )
                lbl_step.SetFont(input_font)
                step_row.Add(lbl_step, flag=wx.RIGHT, border=t.border_small)

                self.stage_align_slider_aligner = UnitFloatSlider(
                    self.pnl_advanced_align,
                    value=0.000001,
                    min_val=0.0000001,
                    max_val=0.001,
                    unit="m",
                    scale="log",
                    accuracy=2,
                    style=wx.BORDER_NONE,
                )
                self.stage_align_slider_aligner.SetForegroundColour(t.fg_label)
                step_row.Add(
                    self.stage_align_slider_aligner,
                    proportion=1,
                    flag=wx.EXPAND,
                )

            jog_grid = self._build_jog_grid()
            adv_sizer.Add(jog_grid)

            with vbox() as align_vbox:
                adv_sizer.Add(align_vbox, flag=wx.ALIGN_CENTRE)
                self._make_position_button(
                    self.pnl_advanced_align,
                    "btn_switch_align",
                    "icon/ico_lens.png",
                    "icon/ico_lens_orange.png",
                    "icon/ico_lens_green.png",
                    strings.BTN_FACTORY_ALIGNMENT,
                )
                align_vbox.Add(self.btn_switch_align)

        sizer.Add(
            self.pnl_advanced_align,
            flag=wx.BOTTOM | wx.EXPAND,
            border=t.border_small,
        )

    def _build_jog_grid(self) -> wx.GridBagSizer:
        """
        Build the GridBagSizer containing stage jog buttons and axis labels.

        :return: Configured GridBagSizer with all jog controls added.
        """
        t = self._theme
        adv_panel = self.pnl_advanced_align

        arrow_font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        arrow_font.SetPointSize(t.font_size_arrow)
        arrow_font.SetWeight(wx.FONTWEIGHT_BOLD)

        lbl_font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        lbl_font.SetPointSize(t.font_size_section_header)
        lbl_font.SetWeight(wx.FONTWEIGHT_BOLD)

        jog_grid = wx.GridBagSizer(vgap=0, hgap=5)

        def _lbl(name: str, text: str) -> wx.StaticText:
            lbl = wx.StaticText(adv_panel, label=text)
            lbl.SetForegroundColour(t.fg_label)
            lbl.SetFont(lbl_font)
            setattr(self, name, lbl)
            return lbl

        def _jog_btn(name: str, label: str) -> ImageTextButton:
            btn = ImageTextButton(
                adv_panel,
                height=48,
                face_colour="def",
                label=label,
                size=(64, -1),
                style=wx.ALIGN_CENTRE,
            )
            btn.SetFont(arrow_font)
            setattr(self, name, btn)
            return btn

        jog_grid.Add(
            _lbl("lbl_py", "+Y"),
            pos=(0, 2),
            flag=wx.TOP | wx.BOTTOM | wx.ALIGN_CENTRE,
            border=t.border_small,
        )
        jog_grid.Add(
            _lbl("lbl_my", "-Y"),
            pos=(4, 2),
            flag=wx.TOP | wx.BOTTOM | wx.ALIGN_CENTRE,
            border=t.border_small,
        )
        jog_grid.Add(
            _lbl("lbl_px", "+X"),
            pos=(2, 4),
            flag=wx.LEFT | wx.ALIGN_CENTRE_VERTICAL,
            border=t.border_small,
        )
        jog_grid.Add(
            _lbl("lbl_mx", "-X"),
            pos=(2, 0),
            flag=wx.RIGHT | wx.ALIGN_RIGHT | wx.ALIGN_CENTRE_VERTICAL,
            border=t.border_small,
        )
        jog_grid.Add(
            _lbl("lbl_pz", "+Z"),
            pos=(0, 5),
            flag=wx.TOP | wx.BOTTOM | wx.ALIGN_CENTRE,
            border=t.border_small,
        )
        jog_grid.Add(
            _lbl("lbl_mz", "-Z"),
            pos=(4, 5),
            flag=wx.TOP | wx.BOTTOM | wx.ALIGN_CENTRE,
            border=t.border_small,
        )

        jog_grid.Add(
            _jog_btn("stage_align_btn_p_aligner_y", "↑"),
            pos=(1, 2),
            flag=wx.LEFT | wx.RIGHT,
            border=7,
        )
        jog_grid.Add(
            _jog_btn("stage_align_btn_m_aligner_y", "↓"),
            pos=(3, 2),
            flag=wx.LEFT | wx.RIGHT,
            border=7,
        )
        jog_grid.Add(_jog_btn("stage_align_btn_m_aligner_x", "←"), pos=(2, 1))
        jog_grid.Add(_jog_btn("stage_align_btn_p_aligner_x", "→"), pos=(2, 3))
        jog_grid.Add(
            _jog_btn("stage_align_btn_p_aligner_z", "↑"),
            pos=(1, 5),
            flag=wx.LEFT | wx.RIGHT,
            border=7,
        )
        jog_grid.Add(
            _jog_btn("stage_align_btn_m_aligner_z", "↓"),
            pos=(3, 5),
            flag=wx.LEFT | wx.RIGHT,
            border=7,
        )

        return jog_grid

    def _build_pnl_temperature(self) -> None:
        """
        Populate the temperature panel with heater toggle and target temperature input.
        """
        t = self._theme
        panel = self.pnl_temperature

        with vbox() as sizer:
            panel.SetSizer(sizer)

            hdr_font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
            hdr_font.SetPointSize(t.font_size_section_header)
            input_font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
            input_font.SetPointSize(t.font_size_input)

            lbl_temp = wx.StaticText(panel, label=strings.LBL_TEMPERATURE)
            lbl_temp.SetForegroundColour(t.fg_label)
            lbl_temp.SetFont(hdr_font)
            sizer.Add(lbl_temp, flag=wx.BOTTOM | wx.ALL, border=t.border_small)

            with hbox() as heater_row:
                sizer.Add(heater_row)

                lbl_heater = wx.StaticText(panel, label=strings.LBL_SAMPLE_HEATER)
                lbl_heater.SetForegroundColour(t.fg_viewport)
                lbl_heater.SetFont(input_font)
                heater_row.Add(
                    lbl_heater,
                    flag=wx.TOP | wx.LEFT | wx.RIGHT,
                    border=t.border_small,
                )

                self.ctrl_sample_heater = wx.CheckBox(panel, label="")
                self.ctrl_sample_heater.SetForegroundColour(t.fg_label)
                heater_row.Add(
                    self.ctrl_sample_heater,
                    flag=wx.TOP | wx.LEFT,
                    border=t.border_small,
                )

            with hbox() as tmp_row:
                sizer.Add(tmp_row)

                lbl_target = wx.StaticText(panel, label=strings.LBL_TARGET_TEMPERATURE)
                lbl_target.SetForegroundColour(t.fg_viewport)
                lbl_target.SetFont(input_font)
                tmp_row.Add(
                    lbl_target,
                    flag=wx.TOP | wx.LEFT,
                    border=t.border_small,
                )

                self.ctrl_sample_target_tmp = UnitFloatCtrl(
                    panel,
                    value=-100,
                    accuracy=4,
                    key_step=0.1,
                    unit="°C",
                    size=(-1, 20),
                    style=wx.BORDER_NONE,
                )
                self.ctrl_sample_target_tmp.SetFont(input_font)
                tmp_row.Add(
                    self.ctrl_sample_target_tmp,
                    flag=wx.LEFT | wx.TOP | wx.BOTTOM,
                    border=t.border_small,
                )


if __name__ == "__main__":
    from odemis.gui.layout.util.preview import run_preview
    run_preview(PnlTabCryosecomChamber)
