from PySide6.QtWidgets import QFrame, QSpacerItem, QSizePolicy
from development.styles import Colors, Border, type_border, Border, BorderRadius, Padding
from development.elements import CTooltip, CLayout, CFrame, CInput, CButton, CTextArea, CSwitch, CMessageBox
from development.model import Instances
from development.utils import Occurrence


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
        self.is_vehicle = True
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

        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.main_layout.addWidget(self.form_box_1)
        self.main_layout.addWidget(self.form_box_2)
        self.main_layout.addWidget(self.form_box_3)
        self.main_layout.addWidget(self.form_box_4)
        self.main_layout.addWidget(self.form_box_5)
        self.main_layout.addItem(spacer)
        self.main_layout.addWidget(self.form_box_6)
        self.main_layout.addWidget(self.form_box_7)

    def __ui__(self):
        self.ui_inputs()
        self.ui_boxes()

    def ui_inputs(self):
        self.input_name = CInput(label="Nome", bg_color=self._input_bg_color, icon_path="app/icons/svg/user.svg")
        self.input_phone = CInput(label="Telefone", bg_color=self._input_bg_color, icon_path="app/icons/svg/phone.svg")
        self.input_highway = CInput(label="Rodovia", bg_color=self._input_bg_color, icon_path="app/icons/svg/highway.svg")
        self.input_km = CInput(label="Km", bg_color=self._input_bg_color, icon_path="app/icons/svg/km.svg")
        self.input_direction = CInput(label="Sentido", bg_color=self._input_bg_color, icon_path="app/icons/svg/sentido.svg")
        self.input_vehicle_model = CInput(label="Veículo", bg_color=self._input_bg_color, icon_path="app/icons/svg/carro.svg")
        self.input_vehicle_color = CInput(label="Cor", bg_color=self._input_bg_color, icon_path="app/icons/svg/cor.svg")
        self.input_vehicle_license_plate = CInput(label="Placa", bg_color=self._input_bg_color, icon_path="app/icons/svg/placa.svg")
        self.input_problem = CInput(label="Problema", bg_color=self._input_bg_color, icon_path="app/icons/svg/sirene.svg")
        self.input_vehicle_occupants = CInput(label="Ocupantes", bg_color=self._input_bg_color, icon_path="app/icons/svg/ocupantes.svg")
        self.input_local = CInput(label="Encontra-se", bg_color=self._input_bg_color, icon_path="app/icons/svg/local.svg")
        self.input_reference_point = CInput(label="Ponto de referência", bg_color=self._input_bg_color, icon_path="app/icons/svg/mapa.svg")
        self.input_description = CTextArea(label="Observações", bg_color=self._input_bg_color)

        self.btn_save = CButton(text="Salvar", bg_color=Colors.blue, text_color=Colors.white, onClick=self.confirm_save_form)
        self.btn_clear = CButton(text="Limpar", bg_color=Colors.gray.adjust_tonality(60), text_color=Colors.white, onClick=self.confirm_clear_form)
        self.btn_alter = CSwitch(on_switch=self.alter_form)

        self.btn_save.setToolTip("CTRL + ENTER")
        self.btn_clear.setToolTip("CTRL + BACKSPACE")
        self.btn_alter.setToolTip("CTRL + TAB")

    def clear_form(self):
        self.input_name.clear()
        self.input_phone.clear()
        self.input_highway.clear()
        self.input_km.clear()
        self.input_direction.clear()
        self.input_problem.clear()
        self.input_local.clear()
        self.input_reference_point.clear()
        self.input_description.clear()

        if self.is_vehicle:
            self.input_vehicle_model.clear()
            self.input_vehicle_color.clear()
            self.input_vehicle_license_plate.clear()
            self.input_vehicle_occupants.clear()

        self.form_occurrence = {
            "name": None,
            "number_phone": None,
            "highway": None,
            "km": None,
            "direction": None,
            "vehicle_model": None,
            "vehicle_color": None,
            "vehicle_license_plate": None,
            "vehicle_occupants": None,
            "problem": None,
            "local": None,
            "reference_point": None,
            "description": None,
        }

    def save_form(self):
        self.form_occurrence = {
            "is_vehicle": self.is_vehicle,
            "name": self.input_name.text() or None,
            "number_phone": self.input_phone.text() or None,
            "highway": self.input_highway.text() or None,
            "km": self.input_km.text() or None,
            "direction": self.input_direction.text() or None,
            "vehicle_model": None,
            "vehicle_color": None,
            "vehicle_license_plate": None,
            "vehicle_occupants": None,
            "problem": self.input_problem.text() or None,
            "local": self.input_local.text() or None,
            "reference_point": self.input_reference_point.text() or None,
            "description": self.input_description.text() or None,
        }
        if self.is_vehicle:
            self.form_occurrence["vehicle_model"] = self.input_vehicle_model.text()
            self.form_occurrence["vehicle_color"] = self.input_vehicle_color.text()
            self.form_occurrence["vehicle_license_plate"] = self.input_vehicle_license_plate.text()
            self.form_occurrence["vehicle_occupants"] = self.input_vehicle_occupants.text()

        try:
            self.new_occurrence = Occurrence(
            name=self.form_occurrence.get("name"),
            phone=self.form_occurrence.get("number_phone"),
            highway=self.form_occurrence.get("highway"),
            km=self.form_occurrence.get("km"),
            direction=self.form_occurrence.get("direction"),
            vehicle=self.form_occurrence.get("vehicle_model"),
            color=self.form_occurrence.get("vehicle_color"),
            license_plate=self.form_occurrence.get("vehicle_license_plate"),
            occupantes=self.form_occurrence.get("vehicle_occupants"),
            problem=self.form_occurrence.get("problem"),
            local=self.form_occurrence.get("local"),
            reference_point=self.form_occurrence.get("reference_point"),
            observations=self.form_occurrence.get("description"),
            is_vehicle=self.is_vehicle,
        )

            self.new_occurrence.save()
            self.clear_form()

        except Exception as e:
            raise e
    
    def alter_form(self, event):
        self.is_vehicle = not self.is_vehicle

        if event == 2:
            self.form_box_3.hide()
            self.input_vehicle_occupants.hide()
        else:
            self.form_box_3.show()
            self.input_vehicle_occupants.show()

    def confirm_save_form(self):
        message = CMessageBox(self,title="Confirmação",text="Deseja realmente salvar?", buttons=CMessageBox.double_choice(), icon_type=CMessageBox.Icon.information)
        response = message.show()
        if response == "Yes":
            self.save_form()
    
    def confirm_clear_form(self):
        message = CMessageBox(self,title="Confirmação",text="Deseja realmente limpar os campos?", buttons=CMessageBox.double_choice(), icon_type=CMessageBox.Icon.warning)
        response = message.show()
        if response == "Yes":
            self.clear_form()

    def ui_boxes(self):
        self.form_box_1 = CFrame(bg_color=Colors.transparent,border_radius=BorderRadius(top_left=20,top_right=20))
        self.form_box_2 = CFrame(bg_color=Colors.transparent)
        self.form_box_3 = CFrame(bg_color=Colors.transparent)
        self.form_box_4 = CFrame(bg_color=Colors.transparent)
        self.form_box_5 = CFrame(bg_color=Colors.transparent)
        self.form_box_6 = CFrame(bg_color=Colors.transparent)
        self.form_box_7 = CFrame(bg_color=Colors.transparent,border_radius=BorderRadius(bottom_left=20,bottom_right=20))

        # Criando layouts separados para cada box
        self.form_layout_1 = CLayout(self.form_box_1).horizontal()
        self.form_layout_2 = CLayout(self.form_box_2).horizontal()
        self.form_layout_3 = CLayout(self.form_box_3).horizontal()
        self.form_layout_4 = CLayout(self.form_box_4).horizontal()
        self.form_layout_5 = CLayout(self.form_box_5).horizontal()
        self.form_layout_6 = CLayout(self.form_box_6).horizontal()
        self.form_layout_7 = CLayout(self.form_box_7).horizontal(spacing=10, margins=(10,10,10,10))

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

        self.form_layout_6.addWidget(self.input_description)

        self.form_layout_7.addWidget(self.btn_save)
        self.form_layout_7.addWidget(self.btn_clear)
        self.form_layout_7.addWidget(self.btn_alter)

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
            self.input_description,
        ]

        for input_field in inputs:
            input_field._text_color = self._text_color
            input_field._bg_color = self._input_bg_color
            input_field.update_styles()

        self.update()
