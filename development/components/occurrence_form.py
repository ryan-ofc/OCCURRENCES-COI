from PySide6.QtWidgets import QFrame, QSpacerItem, QSizePolicy
from development.styles import Colors, Border, type_border, Border, BorderRadius, Padding
from development.elements import CTooltip, CLayout, CFrame, CInput
from development.model import Instances


class OccurrenceForm(QFrame, Instances):
    def __init__(
        self,
        objectName: str = "OccurrenceForm",
        width: int = None,
        height: int = None,
        minimumWidth: int = None,
        minimumHeight: int = None,
        maximumWidth: int = 4096,
        maximumHeight: int = 2160,
        bg_color: Colors = Colors.white,
        text_color: Colors = Colors.black,
        border: int = None,
        border_radius: BorderRadius = None,
        hover_bg_color: Colors = None,
        hover_border: Border = None,
        input_bg_color = Colors.white.adjust_tonality(40),
        padding: Padding = None,
    ):
        QFrame.__init__(self)
        Instances.__init__(
            self,
            objectName=objectName,
            width=width,
            height=height,
            minimumWidth=minimumWidth,
            minimumHeight=minimumHeight,
            maximumWidth=maximumWidth,
            maximumHeight=maximumHeight,
            bg_color=bg_color,
            hover_bg_color=hover_bg_color,
            hover_border=hover_border,
            border=border,
            border_radius=border_radius,
            text_color=text_color,
            padding=padding,
        )
        self._input_bg_color = input_bg_color

        self._toolTip = CTooltip(
            bg_color=self._bg_color,
            color=self._text_color,
            border=Border(
                pixel=1,
                type_border=type_border.solid,
                color=self._text_color,
            ),
            border_radius=3,
            padding=5,
            font_size=12,
        )

        self.__setup__()

    def __setup__(self):
        self.__config__()
        self.__ui__()
        self.__layout__()
        self.__style__()

    def __config__(self):
        self.setObjectName(self._objectName)

        if self._width is not None and self._height is not None:
            self.resize(self._width, self._height)

        if self._minimumWidth is not None and self._minimumHeight is not None:
            self.setMinimumSize(self._minimumWidth, self._minimumHeight)

        if self._maximumWidth is not None and self._maximumHeight is not None:
            self.setMaximumSize(self._maximumWidth, self._maximumHeight)

    def __style__(self):
        self.update_styles()

    def __layout__(self):
        layout = CLayout(self)

        self.main_layout = layout.vertical()

        self.main_layout.addWidget(self.form_box_1)
        self.main_layout.addWidget(self.form_box_2)
        self.main_layout.addWidget(self.form_box_3)
        self.main_layout.addWidget(self.form_box_4)
        self.main_layout.addWidget(self.form_box_5)
        self.main_layout.addWidget(self.form_box_6)

        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.main_layout.addItem(spacer)

    def __ui__(self):
        self.ui_inputs()
        self.ui_boxes()

    def ui_inputs(self):
        self.input_name = CInput(label="Nome", bg_color=self._input_bg_color)
        self.input_phone = CInput(label="Telefone", bg_color=self._input_bg_color)
        self.input_highway = CInput(label="Rodovia", bg_color=self._input_bg_color)
        self.input_km = CInput(label="Km", bg_color=self._input_bg_color)
        self.input_direction = CInput(label="Sentido", bg_color=self._input_bg_color)
        self.input_vehicle_model = CInput(label="Modelo", bg_color=self._input_bg_color)
        self.input_vehicle_color = CInput(label="Cor", bg_color=self._input_bg_color)
        self.input_vehicle_license_plate = CInput(label="Placa", bg_color=self._input_bg_color)
        self.input_problem = CInput(label="Problema", bg_color=self._input_bg_color)
        self.input_vehicle_occupants = CInput(label="Ocupantes", bg_color=self._input_bg_color)
        self.input_local = CInput(label="Encontra-se", bg_color=self._input_bg_color)
        self.input_reference_point = CInput(label="Ponto de referência", bg_color=self._input_bg_color)

    def ui_boxes(self):
        self.form_box_1 = CFrame(bg_color=Colors.transparent,border_radius=BorderRadius(top_left=20,top_right=20))
        self.form_box_2 = CFrame(bg_color=Colors.transparent)
        self.form_box_3 = CFrame(bg_color=Colors.transparent)
        self.form_box_4 = CFrame(bg_color=Colors.transparent)
        self.form_box_5 = CFrame(bg_color=Colors.transparent)
        self.form_box_6 = CFrame(bg_color=Colors.transparent,border_radius=BorderRadius(bottom_left=20,bottom_right=20))

        # Criando layouts separados para cada box
        self.form_layout_1 = CLayout(self.form_box_1).horizontal()
        self.form_layout_2 = CLayout(self.form_box_2).horizontal()
        self.form_layout_3 = CLayout(self.form_box_3).horizontal()
        self.form_layout_4 = CLayout(self.form_box_4).horizontal()
        self.form_layout_5 = CLayout(self.form_box_5).horizontal()
        self.form_layout_6 = CLayout(self.form_box_6).horizontal()

        self.form_layout_1.addWidget(self.input_name)
        self.form_layout_1.addWidget(self.input_phone)

        self.form_layout_2.addWidget(self.input_highway)
        self.form_layout_2.addWidget(self.input_km)
        self.form_layout_2.addWidget(self.input_direction)

        self.form_layout_3.addWidget(self.input_vehicle_model)
        self.form_layout_3.addWidget(self.input_vehicle_color)
        self.form_layout_3.addWidget(self.input_vehicle_license_plate)

        self.form_layout_4.addWidget(self.input_vehicle_occupants)
        self.form_layout_4.addWidget(self.input_problem)

        self.form_layout_5.addWidget(self.input_local)
        self.form_layout_5.addWidget(self.input_reference_point)

    def update_styles(self):
        hover_style = (
            f"""
            #{self._objectName}:hover {{
                background-color: {self._hover_bg_color};
            }}
        """
            if self._hover_bg_color
            else ""
        )

        hover_border = (
            f"""
            #{self._objectName}:hover {{
                border: {self._hover_border};
            }}
        """
            if self._hover_border
            else ""
        )

        border = (
            f"""
            #{self._objectName} {{
                border: {self._border};
            }}
        """
            if self._border
            else ""
        )

        border_radius = (
            f"""
            #{self._objectName} {{
                border-top-left-radius: {self._border_radius.top_left};
                border-top-right-radius: {self._border_radius.top_right};
                border-bottom-left-radius: {self._border_radius.bottom_left};
                border-bottom-right-radius: {self._border_radius.bottom_right};
            }}
        """
            if self._border_radius
            else ""
        )

        padding = (
            f"""
            #{self._objectName} {{
                padding-top: {self._padding.top};
                padding-right: {self._padding.right};
                padding-bottom: {self._padding.bottom};
                padding-left: {self._padding.left};
            }}
        """
            if self._padding
            else ""
        )

        style_sheet = f"""
            #{self._objectName} {{
                color: {self._text_color};
                background-color: {self._bg_color};
            }}
            {hover_style}
            {border}
            {border_radius}
            {padding}
            {hover_border}
            {self._toolTip.styleSheet()}
        """
        self.setStyleSheet(style_sheet)

        inputs = [
            self.input_name,
            self.input_phone,
            self.input_highway,
            self.input_km,
            self.input_direction,
            self.input_vehicle_model,
            self.input_vehicle_color,
            self.input_vehicle_license_plate,
            self.input_problem,
            self.input_vehicle_occupants,
            self.input_local,
            self.input_reference_point,
        ]

        for input_field in inputs:
            input_field._text_color = self._text_color
            input_field._bg_color = self._input_bg_color
            input_field.update_styles()

        self.update()
