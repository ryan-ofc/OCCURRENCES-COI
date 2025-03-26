from PySide6.QtWidgets import QLineEdit, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QCompleter
from PySide6.QtGui import QPixmap, QPainter, QFont
from PySide6.QtCore import Qt
from PySide6.QtSvg import QSvgRenderer
from development.styles import Colors, Border, type_border, Padding, BorderRadius
from development.elements import CTooltip
from development.model import Instances
import re


class CInput(QWidget, Instances):
    def __init__(
        self,
        label: str = "",
        icon_path: str = None,
        objectName: str = "CInput",
        placeholder: str = None,
        width: int = None,
        height: int = None,
        minimumWidth: int = None,
        minimumHeight: int = None,
        maximumWidth: int = 4096,
        maximumHeight: int = 2160,
        bg_color: Colors = Colors.white,
        text_color: Colors = Colors.black.adjust_tonality(75),
        border: Border = None,
        border_radius: BorderRadius = BorderRadius(all=5),
        hover_bg_color: Colors = None,
        hover_border: Border = None,
        padding: Padding = Padding(all=8),
        suggestions: list = None,
        only_numbers: bool = False,
        no_special_chars: bool = False,
        only_uppercase: bool = False,
        value: str = None,
        font_size: int = 10,
    ):
        super().__init__()
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
            text_color=text_color,
            padding=padding,
            border_radius=border_radius,
            font_size=font_size,
        )

        self._placeholder = placeholder
        self.label = QLabel(label)
        self.icon_label = QLabel()
        self.input_field = QLineEdit()
        self.input_field.setObjectName(objectName)
        self.icon_path = icon_path
        self.suggestions = suggestions if suggestions else []
        self.only_numbers = only_numbers
        self.no_special_chars = no_special_chars
        self.only_uppercase = only_uppercase
        self.value = value

        self.completer = QCompleter(self.suggestions, self)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer.setFilterMode(Qt.MatchContains)
        self.input_field.setCompleter(self.completer)

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

        if self.value is not None:
            self.input_field.setText(str(self.value))
    
        self.input_field.textChanged.connect(self.__on_text_changed)
        self.input_field.setFont(QFont("Arial", self._font_size))

    def __setup__(self):
        self.__config__()
        self.__style__()
        self.__layout__()

    def __config__(self):
        if self._width is not None and self._height is not None:
            self.resize(self._width, self._height)

        if self._minimumWidth is not None and self._minimumHeight is not None:
            self.setMinimumSize(self._minimumWidth, self._minimumHeight)

        if self._maximumWidth is not None and self._maximumHeight is not None:
            self.setMaximumSize(self._maximumWidth, self._maximumHeight)

        if self._placeholder is not None:
            self.input_field.setPlaceholderText(self._placeholder)

        if self.icon_path:
            self.setIcon(self.icon_path)
  
    def __style__(self):
        self.update_styles()

    def __layout__(self):
        main_layout = QVBoxLayout()
        label_layout = QHBoxLayout()

        if self.icon_path:
            label_layout.addWidget(self.icon_label)

        label_layout.addWidget(self.label)
        label_layout.addStretch()

        main_layout.setSpacing(4)
        main_layout.addLayout(label_layout)
        main_layout.addWidget(self.input_field)

        self.setLayout(main_layout)

    def __on_text_changed(self, text: str):
        cursor_pos = self.input_field.cursorPosition()
        filtered_text = self.apply_filters(text)
        
        if filtered_text != text:
            self.input_field.setText(filtered_text)
            self.input_field.setCursorPosition(cursor_pos - (len(text) - len(filtered_text)))

    def apply_filters(self, text: str) -> str:
        if self.only_numbers:
            text = re.sub(r'\D', '', text)
        if self.no_special_chars:
            text = re.sub(r'[^a-zA-Z0-9 ]', '', text)
        if self.only_uppercase:
            text = text.upper()
        return text
    
    def clear(self):
        self.input_field.clear()

    def text(self):
        return self.input_field.text()

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
            QLabel {{
                font-size: 11px;
                padding-left: 0px;
                color: {self._text_color};
            }}
            #{self._objectName}:focus {{
                border: 1px solid gray;
            }}
            {hover_style}
            {border}
            {border_radius}
            {padding}
            {hover_border}
            {self._toolTip.styleSheet()}
        """
        self.setStyleSheet(style_sheet)
        self.input_field.setStyleSheet(style_sheet)
        self.label.setStyleSheet(style_sheet)
        self.update()

    def setIcon(self, icon_path):
            if icon_path.lower().endswith(".svg"):
                # Renderiza SVG com alta qualidade
                svg_renderer = QSvgRenderer(icon_path)
                pixmap = QPixmap(20, 20)  # Aumenta o tamanho para melhor resolução
                pixmap.fill(Qt.transparent)  # Fundo transparente
                
                painter = QPainter(pixmap)
                svg_renderer.render(painter)
                painter.end()
            else:
                # Renderiza imagens comuns com suavização
                pixmap = QPixmap(icon_path).scaled(
                    20, 20, mode=Qt.SmoothTransformation
                )
            
            pixmap.setDevicePixelRatio(self.devicePixelRatioF())  # Ajusta para telas de alta DPI
            self.icon_label.setPixmap(pixmap)

    def setOnlyNumbers(self, role: bool):
        self.only_numbers = role

    def setNoSpecialChars(self, role: bool):
        self.no_special_chars = role

    def setOnlyUppercase(self, role: bool):
        self.only_uppercase = role
