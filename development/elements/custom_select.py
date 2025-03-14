from PySide6.QtWidgets import QComboBox, QLabel, QVBoxLayout, QHBoxLayout, QWidget
from PySide6.QtGui import QPixmap, QPainter, QFont
from PySide6.QtCore import Qt
from PySide6.QtSvg import QSvgRenderer
from development.styles import Colors, Border, type_border, Padding, BorderRadius
from development.elements import CTooltip
from development.model import Instances
import re


class CSelect(QWidget, Instances):
    def __init__(
        self,
        label: str = "",
        icon_path: str = None,
        objectName: str = "CSelect",
        items: list = None,
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
        is_editable: bool = False,
        icon_down_arrow: str = "app/icons/svg/seta.svg",
        icon_down_arrow_size: list = [14,32],
        only_numbers: bool = False,
        no_special_chars: bool = False,
        only_uppercase: bool = False,
        default_value: bool = False,
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

        self._icon_down_arrow = icon_down_arrow
        self._icon_down_arrow_size = icon_down_arrow_size
        self.label = QLabel(label)
        self.icon_label = QLabel()
        self.combo_box = QComboBox()
        self.combo_box.setObjectName(objectName)
        self.combo_box.setEditable(is_editable)
        self.icon_path = icon_path
        self.default_value = default_value
        self.value = value

        self.only_numbers = only_numbers
        self.no_special_chars = no_special_chars
        self.only_uppercase = only_uppercase

        if items:
            self.combo_box.addItems([self.apply_filters(item) for item in items])

        if self.value is not None:
            if self.value in [self.combo_box.itemText(i) for i in range(self.combo_box.count())]:
                self.combo_box.setCurrentText(self.value)
            else:
                self.combo_box.addItem(self.value)
                self.combo_box.setCurrentText(str(self.value))

        if not (self.default_value):
            self.combo_box.setCurrentIndex(-1)

        self.combo_box.editTextChanged.connect(self.on_text_changed)
        self.combo_box.setFont(QFont("Arial", self._font_size))

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
        main_layout.addWidget(self.combo_box)

        self.setLayout(main_layout)

    def setSelectionValue(self, value: str):
        if value in [self.combo_box.itemText(i) for i in range(self.combo_box.count())]:
            self.combo_box.setCurrentText(value)
        else:
            self.combo_box.addItem(value)
            self.combo_box.setCurrentText(str(value))

    def setValue(self, value: str):
        self.value = value

    def currentText(self):
        return self.combo_box.currentText()

    def addItem(self, text):
        self.combo_box.addItem(text)

    def addItems(self, items):
        self.combo_box.addItems(items)

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
            #{self._objectName}::drop-down {{
                padding-right: 4px;
                border-top-right-radius: {self._border_radius.top_right};
                border-bottom-right-radius: {self._border_radius.bottom_right};
                background-color: transparent;
            }}
            #{self._objectName}::down-arrow {{
                padding-left: 3px;
                padding-right: 5px;
                border-left: {self._border if self._border else 'transparent'};
                image: url({self._icon_down_arrow});
                width: {self._icon_down_arrow_size[0]};
                height: {self._icon_down_arrow_size[1]};
            }}
            #{self._objectName}::down-arrow:hover {{
                border-left: {self._border if self._border else 'transparent'};
            }}
            #{self._objectName} QAbstractItemView {{
                border: 1px solid #ccc;
                background-color: {self._bg_color};
                selection-background-color: #0078D7;
                selection-color: {self._text_color};
                color: {self._text_color};
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
        self.combo_box.setStyleSheet(style_sheet)
        self.label.setStyleSheet(style_sheet)
        self.update()

    def setIcon(self, icon_path):
        if icon_path.lower().endswith(".svg"):
            svg_renderer = QSvgRenderer(icon_path)
            pixmap = QPixmap(20, 20)
            pixmap.fill(Qt.transparent)

            painter = QPainter(pixmap)
            svg_renderer.render(painter)
            painter.end()
        else:
            pixmap = QPixmap(icon_path).scaled(20, 20, mode=Qt.SmoothTransformation)

        pixmap.setDevicePixelRatio(self.devicePixelRatioF())
        self.icon_label.setPixmap(pixmap)

    def clearText(self):
        self.combo_box.setCurrentIndex(-1)

    def apply_filters(self, text: str) -> str:
        if self.only_numbers:
            text = re.sub(r'\D', '', text)
        if self.no_special_chars:
            text = re.sub(r'[^a-zA-Z0-9 ]', '', text)
        if self.only_uppercase:
            text = text.upper()
        return text

    def setOnlyNumbers(self, role: bool):
        self.only_numbers = role

    def setNoSpecialChars(self, role: bool):
        self.no_special_chars = role

    def setOnlyUppercase(self, role: bool):
        self.only_uppercase = role

    def on_text_changed(self, text: str):
        self.combo_box.blockSignals(True)
        self.combo_box.setEditText(self.apply_filters(text))
        self.combo_box.blockSignals(False)      