from PySide6.QtWidgets import QDialog, QSpacerItem, QSizePolicy
from PySide6.QtGui import QIcon, QPixmap, QPainter, QColor, QFont, QStandardItem
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtCore import QByteArray, Qt
from development.styles import (
    Colors,
    Border,
    type_border,
    Border,
    BorderRadius,
    Padding,
)
from development.elements import (
    CTooltip,
    CLayout,
    CFrame,
    CInput,
    CButton,
    CTextArea,
    CSwitch,
    CMessageBox,
    CLabel,
    CSelect,
)
from development.model import Instances
from development.constants import *
from ..utils import Occurrence
import base64
import os


class OccurrenceEditForm(QDialog, Instances):
    def __init__(
        self,
        occurrence: Occurrence,
        objectName: str = "OccurrenceEditForm",
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
        input_bg_color: Colors = Colors.white.adjust_tonality(40),
        input_border: Border = Border(color=Colors.gray.adjust_tonality(85)),
        padding: Padding = None,
        update_table: callable = None,
    ):
        QDialog.__init__(self)
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
        self.occurrence = occurrence
        self.is_vehicle = True
        self.update_table = update_table
        self._input_bg_color = input_bg_color
        self._input_border = input_border

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

        self.main_layout.addWidget(self.title_label)
        self.main_layout.addWidget(self.form_box_1)
        self.main_layout.addWidget(self.form_box_2)
        self.main_layout.addWidget(self.form_box_3)
        self.main_layout.addWidget(self.form_box_4)
        self.main_layout.addWidget(self.form_box_5)
        self.main_layout.addItem(spacer)
        self.main_layout.addWidget(self.form_box_6)
        self.main_layout.addWidget(self.form_box_7)

    def __ui__(self):
        self.title_label = CLabel(
            text="Formulário completo", text_color=self._text_color
        )
        self.ui_inputs()
        self.ui_boxes()

    def setIcon(self, source: str | bytes):
        """Define um ícone para a janela a partir de um arquivo ou Base64 (suporte para PNG, JPG e SVG)."""
        if os.path.exists(source):
            icon = QIcon(source)  # Arquivo de imagem ou SVG
        else:
            icon = self.__load_icon_from_base64(source)

        self.setWindowIcon(icon)

    def __load_icon_from_base64(self, base64_str):
        """Converte uma string Base64 em um QIcon, suportando PNG, JPG e SVG."""
        try:
            image_data = base64.b64decode(base64_str)

            # Verifica se o dado é um SVG
            if b"<svg" in image_data:
                return self.__convert_svg_to_icon(image_data)

            # Caso contrário, assume que é PNG/JPG
            pixmap = QPixmap()
            pixmap.loadFromData(image_data)
            return QIcon(pixmap)
        except Exception:
            return QIcon()

    def __convert_svg_to_icon(self, svg_data):
        """Converte um arquivo SVG Base64 em um QIcon."""
        try:
            renderer = QSvgRenderer(QByteArray(svg_data))
            pixmap = QPixmap(128, 128)
            pixmap.fill(Qt.transparent)

            # Renderiza o SVG no pixmap
            painter = QPainter(pixmap)
            renderer.render(painter)
            painter.end()

            return QIcon(pixmap)
        except Exception:
            return QIcon()

    def ui_inputs(self):
        self.input_name = CSelect(
            label="Nome",
            bg_color=self._input_bg_color,
            icon_path="app/icons/svg/user.svg",
            is_editable=True,
            items=["Usuário"],
            only_numbers=False,
            only_uppercase=True,
            no_special_chars=False,
            value=self.occurrence.name,
            default_value=True,
        )
        self.input_phone = CInput(
            label="Telefone",
            bg_color=self._input_bg_color,
            icon_path="app/icons/svg/phone.svg",
            only_numbers=True,
            only_uppercase=True,
            no_special_chars=False,
            value=self.occurrence.phone,
        )
        self.input_highway = CInput(
            label="Rodovia",
            bg_color=self._input_bg_color,
            icon_path="app/icons/svg/highway.svg",
            suggestions=HIGHWAYS,
            only_numbers=False,
            only_uppercase=True,
            no_special_chars=False,
            value=self.occurrence.highway,
        )
        self.input_km = CInput(
            label="Km",
            bg_color=self._input_bg_color,
            icon_path="app/icons/svg/km.svg",
            only_numbers=True,
            only_uppercase=False,
            no_special_chars=False,
            value=self.occurrence.km,
        )
        self.input_direction = CSelect(
            label="Sentido",
            bg_color=self._input_bg_color,
            icon_path="app/icons/svg/sentido.svg",
            items=DIRECTIONS,
            only_numbers=False,
            only_uppercase=True,
            no_special_chars=False,
            value=self.occurrence.direction,
            default_value=True,
        )
        self.input_vehicle_model = CSelect(
            label="Veículo",
            bg_color=self._input_bg_color,
            icon_path="app/icons/svg/carro.svg",
            items=VEHICLES_MODELS,
            is_editable=True,
            only_numbers=False,
            only_uppercase=True,
            no_special_chars=False,
            value=self.occurrence.vehicle,
            default_value=True,
        )
        self.input_vehicle_color = CInput(
            label="Cor",
            bg_color=self._input_bg_color,
            icon_path="app/icons/svg/cor.svg",
            suggestions=COLORS,
            only_numbers=False,
            only_uppercase=True,
            no_special_chars=False,
            value=self.occurrence.color,
        )
        self.input_vehicle_license_plate = CInput(
            label="Placa",
            bg_color=self._input_bg_color,
            icon_path="app/icons/svg/placa.svg",
            only_numbers=False,
            only_uppercase=True,
            no_special_chars=False,
            value=self.occurrence.license_plate,
        )
        self.input_problem = CSelect(
            label="Problema",
            bg_color=self._input_bg_color,
            icon_path="app/icons/svg/sirene.svg",
            only_numbers=False,
            only_uppercase=True,
            no_special_chars=False,
            is_editable=True,
            default_value=False,
            items=[],
        )
        self.input_vehicle_occupants = CInput(
            label="Ocupantes",
            bg_color=self._input_bg_color,
            icon_path="app/icons/svg/ocupantes.svg",
            only_numbers=False,
            only_uppercase=True,
            no_special_chars=False,
            value=self.occurrence.occupantes,
        )
        self.input_local = CSelect(
            label="Encontra-se",
            bg_color=self._input_bg_color,
            icon_path="app/icons/svg/local.svg",
            items=LOCALS,
            is_editable=True,
            only_numbers=False,
            only_uppercase=True,
            no_special_chars=False,
            value=self.occurrence.local,
            default_value=True,
        )
        self.input_reference_point = CInput(
            label="Ponto de referência",
            bg_color=self._input_bg_color,
            icon_path="app/icons/svg/mapa.svg",
            only_numbers=False,
            only_uppercase=True,
            no_special_chars=False,
            value=self.occurrence.reference_point,
        )
        self.input_description = CTextArea(
            label="Observações",
            bg_color=self._input_bg_color,
            only_numbers=False,
            only_uppercase=True,
            no_special_chars=False,
            value=self.occurrence.observations,
        )

        self.btn_save = CButton(
            text="Salvar",
            bg_color=Colors.blue,
            hover_bg_color=Colors.blue.adjust_tonality(60),
            text_color=Colors.white,
            onClick=self.confirm_save_form,
        )
        self.btn_clipboard = CButton(
            text="Copiar",
            bg_color=Colors.gray,
            hover_bg_color=Colors.gray.adjust_tonality(60),
            text_color=Colors.white,
            onClick=self.clipboard_form,
        )
        self.btn_alter = CSwitch(on_switch=self.alter_form)

        self.btn_save.setToolTip("CTRL + ENTER")
        self.btn_clipboard.setToolTip("Copiar")
        self.btn_alter.setToolTip("Alterar Formulário")

        self.problems()

    def clipboard_form(self):
        self.form_occurrence = {
            "is_vehicle": self.is_vehicle,
            "name": self.input_name.currentText() or "Usuário",
            "number_phone": self.input_phone.text() or "N/A",
            "highway": self.input_highway.text() or "",
            "km": self.input_km.text() or "",
            "direction": self.input_direction.currentText() or "",
            "vehicle_model": "N/A",
            "vehicle_color": "N/A",
            "vehicle_license_plate": "N/A",
            "vehicle_occupants": "N/A",
            "problem": self.input_problem.currentText() or "",
            "local": self.input_local.currentText() or "N/A",
            "reference_point": self.input_reference_point.text() or "N/A",
            "description": self.input_description.text() or "",
        }
        if self.is_vehicle:
            self.form_occurrence["vehicle_model"] = (
                self.input_vehicle_model.currentText()
                if self.input_vehicle_model.currentText()
                else "N/A"
            )
            self.form_occurrence["vehicle_color"] = (
                self.input_vehicle_color.text()
                if self.input_vehicle_color.text()
                else "N/A"
            )
            self.form_occurrence["vehicle_license_plate"] = (
                self.input_vehicle_license_plate.text()
                if self.input_vehicle_license_plate.text()
                else "N/A"
            )
            self.form_occurrence["vehicle_occupants"] = (
                self.input_vehicle_occupants.text()
                if self.input_vehicle_occupants.text()
                else "N/A"
            )

        try:
            from development.modules import Occurrence

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

            self.new_occurrence.clipboard()
            self.destroy(True)

        except Exception as e:
            message = CMessageBox(
                self, title="Atenção", text=str(e), icon_type=CMessageBox.Icon.critical
            )
            message.show()

    def save_form(self):
        self.form_occurrence = {
            "id": self.occurrence.id,
            "is_vehicle": self.is_vehicle,
            "name": self.input_name.currentText() or "Usuário",
            "number_phone": self.input_phone.text() or "N/A",
            "highway": self.input_highway.text() or "",
            "km": self.input_km.text() or 0,
            "direction": self.input_direction.currentText() or "",
            "vehicle_model": self.input_vehicle_model.currentText() or "",
            "vehicle_color": self.input_vehicle_color.text() or "N/A",
            "vehicle_license_plate": self.input_vehicle_license_plate.text() or "N/A",
            "vehicle_occupants": self.input_vehicle_occupants.text() or "N/A",
            "problem": self.input_problem.currentText() or "",
            "local": self.input_local.currentText() or "N/A",
            "reference_point": self.input_reference_point.text() or "N/A",
            "description": self.input_description.text() or "",
        }

        try:
            from development.modules import Occurrence

            self.new_occurrence = Occurrence(
                id=self.form_occurrence.get("id"),
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

            self.new_occurrence.update()
            self.new_occurrence.clipboard()
            message = CMessageBox(
                self, title="Notificação", text="Ocorrência atualizada!"
            )
            message.show()
            self.destroy(True)

        except Exception as e:
            message = CMessageBox(
                self, title="Atenção", text=str(e), icon_type=CMessageBox.Icon.critical
            )
            message.show()

    def alter_form(self, event):
        self.is_vehicle = not self.is_vehicle

        if event == 2:
            self.form_box_3.hide()
            self.input_vehicle_occupants.hide()
            self.input_problem.combo_box.clear()
            self.other_problems()
            self.title_label.setText("Formulário simples")
        else:
            self.form_box_3.show()
            self.input_vehicle_occupants.show()
            self.input_problem.combo_box.clear()
            self.problems()
            self.title_label.setText("Formulário completo")

    def other_problems(self):
        self.add_title("─── Animais Soltos ───", "#00AC0B")
        self.input_problem.combo_box.addItems(
            [
                "Equino solto na via",
                "Bovino solto na via",
                "Suíno solto na via",
                "Canino solto na via",
            ]
        )

        self.add_title("─── Animais Mortos ───", "#C41111")
        self.input_problem.combo_box.addItems(
            [
                "Equino morto na via",
                "Bovino morto na via",
                "Suíno morto na via",
                "Canino morto na via",
            ]
        )
        if self.occurrence.problem:
            self.input_problem.combo_box.insertItem(0, self.occurrence.problem)
            self.input_problem.combo_box.setCurrentText(self.occurrence.problem)
        else:
            self.input_problem.combo_box.setCurrentIndex(-1)

    def problems(self):
        self.add_title("─── Mecânicos ───", "darkgreen")
        self.input_problem.combo_box.addItems(["Pane Mecânica", "Pane Elétrica"])

        self.add_title("─── Acidentes ───", "#C41111")
        self.input_problem.combo_box.addItems(
            [
                "Sinistro / Saída de pista",
                "Sinistro / Capotamento",
                "Sinistro / Tombamento",
            ]
        )

        self.add_title("─── Pneus ───", "darkorange")
        self.input_problem.combo_box.addItems(
            [
                "Pneu furado / Danificado, possui estepe: Sim",
                "Pneu furado / Danificado, possui estepe: Não",
            ]
        )
 
        if self.occurrence.problem:
            self.input_problem.combo_box.insertItem(0, self.occurrence.problem)
            self.input_problem.combo_box.setCurrentText(self.occurrence.problem)
        else:
            self.input_problem.combo_box.setCurrentIndex(-1)

    def add_title(self, title, color):
        """Adiciona um título desabilitado e colorido no QComboBox"""
        self.input_problem.combo_box.addItem(title)
        item: QStandardItem = self.input_problem.combo_box.model().item(
            self.input_problem.combo_box.count() - 1
        )
        item.setEnabled(False)
        item.setForeground(QColor(color))
        font = QFont()
        font.setBold(True)
        item.setFont(font)

    def confirm_save_form(self):
        message = CMessageBox(
            self,
            title="Confirmação",
            text="Salvar alterações e copiar?",
            buttons=CMessageBox.double_choice(),
            icon_type=CMessageBox.Icon.information,
        )
        response = message.show()
        if response == "Yes":
            self.save_form()

    def confirm_clear_form(self):
        message = CMessageBox(
            self,
            title="Confirmação",
            text="Deseja realmente limpar os campos?",
            buttons=CMessageBox.double_choice(),
            icon_type=CMessageBox.Icon.warning,
        )
        response = message.show()
        if response == "Yes":
            self.clear_form()

    def ui_boxes(self):
        self.form_box_1 = CFrame(
            bg_color=Colors.transparent,
            border_radius=BorderRadius(top_left=20, top_right=20),
        )
        self.form_box_2 = CFrame(bg_color=Colors.transparent)
        self.form_box_3 = CFrame(bg_color=Colors.transparent)
        self.form_box_4 = CFrame(bg_color=Colors.transparent)
        self.form_box_5 = CFrame(bg_color=Colors.transparent)
        self.form_box_6 = CFrame(bg_color=Colors.transparent)
        self.form_box_7 = CFrame(
            bg_color=Colors.transparent,
            border_radius=BorderRadius(bottom_left=20, bottom_right=20),
        )

        # Criando layouts separados para cada box
        self.form_layout_1 = CLayout(self.form_box_1).horizontal()
        self.form_layout_2 = CLayout(self.form_box_2).horizontal()
        self.form_layout_3 = CLayout(self.form_box_3).horizontal()
        self.form_layout_4 = CLayout(self.form_box_4).horizontal()
        self.form_layout_5 = CLayout(self.form_box_5).horizontal()
        self.form_layout_6 = CLayout(self.form_box_6).horizontal()
        self.form_layout_7 = CLayout(self.form_box_7).horizontal(
            spacing=10, margins=(10, 10, 10, 10)
        )

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
        self.form_layout_7.addWidget(self.btn_clipboard)
        self.form_layout_7.addWidget(self.btn_alter)

        self.btn_alter.setChecked(not self.occurrence.is_vehicle)

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

        inputs: list[CInput] = [
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
            input_field._border = self._input_border
            input_field.update_styles()

        self.title_label._text_color = self._text_color
        self.title_label.update_styles()
        self.update()
