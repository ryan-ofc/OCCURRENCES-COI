from PySide6.QtWidgets import QLabel, QHBoxLayout, QWidget
from PySide6.QtGui import QPixmap, QPainter
from PySide6.QtCore import Qt
from PySide6.QtSvg import QSvgRenderer
from development.styles import Colors, Border, type_border, Padding, BorderRadius
from development.elements import CTooltip
from development.model import Instances


class CLabel(QWidget, Instances):
    def __init__(
        self,
        text: str = "",
        icon_path: str = None,
        objectName: str = "CLabel",
        width: int = None,
        height: int = None,
        minimumWidth: int = None,
        minimumHeight: int = None,
        maximumWidth: int = 4096,
        maximumHeight: int = 2160,
        bg_color: Colors = Colors.transparent,
        text_color: Colors = Colors.black.adjust_tonality(75),
        border: Border = None,
        border_radius: BorderRadius = BorderRadius(all=5),
        padding: Padding = Padding(all=8),
        icon_size: list[int] = [20,20],
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
            border=border,
            text_color=text_color,
            padding=padding,
            border_radius=border_radius,
        )

        self.label = QLabel(text)
        self.icon_label = QLabel()
        self.icon_path = icon_path
        self._icon_size = icon_size

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
        if self.icon_path:
            self.setIcon(self.icon_path)

        if self._width is not None and self._height is not None:
            self.resize(self._width, self._height)

        if self._minimumWidth is not None and self._minimumHeight is not None:
            self.setMinimumSize(self._minimumWidth, self._minimumHeight)

        if self._maximumWidth is not None and self._maximumHeight is not None:
            self.setMaximumSize(self._maximumWidth, self._maximumHeight)

    def setIcon(self, icon_path):
        if icon_path.lower().endswith(".svg"):
            svg_renderer = QSvgRenderer(icon_path)
            pixmap = QPixmap(self._icon_size[0], self._icon_size[1])
            pixmap.fill(Qt.transparent)

            painter = QPainter(pixmap)
            svg_renderer.render(painter)
            painter.end()
        else:
            pixmap = QPixmap(icon_path).scaled(self._icon_size[0], self._icon_size[1], mode=Qt.SmoothTransformation)

        pixmap.setDevicePixelRatio(self.devicePixelRatioF())
        self.icon_label.setPixmap(pixmap)

    def __style__(self):
        self.update_styles()

    def __layout__(self):
        main_layout = QHBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if self.icon_path:
            main_layout.addWidget(self.icon_label)
        main_layout.addWidget(self.label)
        self.setLayout(main_layout)

    def setText(self, text: str):
        self.label.setText(text)

    def text(self):
        return self.label.text()

    def update_styles(self):
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

        style_sheet = f"""
            #{self._objectName} {{
                color: {self._text_color};
                background-color: {self._bg_color};
            }}
            QLabel {{
                font-size: 16px;
                font-weight: bold;
                color: {self._text_color};
            }}
            {border_radius}
            {self._toolTip.styleSheet()}
        """
        self.setStyleSheet(style_sheet)
        self.label.setStyleSheet(style_sheet)
        self.update()
