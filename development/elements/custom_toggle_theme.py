from PySide6.QtWidgets import (
    QWidget,
    QPushButton,
)
from PySide6.QtGui import QIcon, QImage, QPainter, Qt
from PySide6.QtCore import QSize
from PySide6.QtSvg import QSvgRenderer
import os


class ToggleTheme(QPushButton):
    def __init__(
        self,
        parent: QWidget,
        icon_light: str,
        icon_dark: str,
        iconSize: list = (42, 42),
    ):
        super().__init__(parent=parent)
        self._parent = parent
        self._icon_light = icon_light
        self._icon_dark = icon_dark
        self._iconSize = [iconSize[0], iconSize[1]]
        self.default_theme = True
        self.bg_light = "#0082D8"
        self.bg_dark = "#005892"
        self.border_radius = (self._iconSize[0] // 2) + 2

        self.setToolTip("Dark ativo")

        self.setFixedSize(self._iconSize[0] + 5, self._iconSize[1] + 5)
        self.setStyleSheet(
            f"""
                QPushButton {{
                    background-color: {self.bg_dark}; 
                    border-radius: {self.border_radius}px;
                    color: white; font-size: 30px;
            }}
                QToolTip {{
                    background-color: #0097D8;
                    color: #ffffff;
                    border: 1px solid #007AAF;
                    padding: 5px;
                    border-radius: 3px;
                    font-size: 12px;
            }}
            """
        )

        self.set_icon(self._icon_light)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self.set_icon(self._icon_light)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def set_icon(self, icon_name: str):
        """Sets the button icon from an SVG."""
        base_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "app", "icons", "svg")
        )
        full_path = os.path.join(base_path, icon_name)
        renderer = QSvgRenderer(full_path)
        image = QImage(self._iconSize[0], self._iconSize[1], QImage.Format_ARGB32)
        image.fill(0)
        painter = QPainter(image)
        renderer.render(painter)
        painter.end()

        self.setIcon(QIcon(full_path))
        self.setIconSize(QSize(self._iconSize[0] - 10, self._iconSize[1] - 10))

    def switch_theme(self):
        """Switches the theme and updates the icon."""
        self.default_theme = not self.default_theme

        self.setStyleSheet(
            f"background-color: {self.bg_dark}; border-radius: {self.border_radius}; color: white; font-size: 30px;"
            if self.default_theme
            else f"background-color: {self.bg_light}; border-radius: {self.border_radius}; color: white; font-size: 30px;"
        )

        self.setToolTip("Dark ativo" if self.default_theme else "Light ativo")
        self.set_icon(self._icon_light if self.default_theme else self._icon_dark)
