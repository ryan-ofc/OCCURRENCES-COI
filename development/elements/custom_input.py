from PySide6.QtWidgets import QLineEdit, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QCompleter
from PySide6.QtGui import QPixmap, QPainter
from PySide6.QtCore import Qt
from PySide6.QtSvg import QSvgRenderer
from development.styles import Colors, Border, type_border, Padding, BorderRadius
from development.elements import CTooltip
from development.model import Instances

class CInput(QWidget, Instances):
    def __init__(
        self,
        label: str = "",
        icon_path: str = None,  # Ícone
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
        )

        self._placeholder = placeholder
        self.label = QLabel(label)
        self.icon_label = QLabel()
        self.input_field = QLineEdit()
        self.input_field.setObjectName(objectName)
        self.icon_path = icon_path
        self.suggestions = suggestions if suggestions else []

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
