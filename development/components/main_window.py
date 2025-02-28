from PySide6.QtWidgets import QMainWindow
from PySide6.QtGui import QIcon, QPixmap, QPainter
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtCore import QByteArray, Qt
from development.styles import Colors, Border, type_border
from development.elements import CTooltip
from development.model import Instances
import base64
import os


class CMainWindow(QMainWindow, Instances):
    def __init__(
        self,
        objectName: str = "CMainWindow",
        title: str = "CMainWindow",
        width: int = None,
        height: int = None,
        minimumWidth: int = None,
        minimumHeight: int = None,
        maximumWidth: int = 4096,
        maximumHeight: int = 2160,
        bg_color: Colors = Colors.gray,
        text_color: Colors = Colors.black,
        icon: str | bytes = None,
    ):
        QMainWindow.__init__(self)
        Instances.__init__(
            self,
            objectName=objectName,
            title=title,
            width=width,
            height=height,
            minimumWidth=minimumWidth,
            minimumHeight=minimumHeight,
            maximumWidth=maximumWidth,
            maximumHeight=maximumHeight,
            bg_color=bg_color,
            text_color=text_color,
            icon=icon,
        )

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

    def __config__(self):
        self.setObjectName(self._objectName)

        if self._title is not None:
            self.setWindowTitle(self._title)

        if self._width is not None and self._height is not None:
            self.resize(self._width, self._height)

        if self._minimumWidth is not None and self._minimumHeight is not None:
            self.setMinimumSize(self._minimumWidth, self._minimumHeight)

        if self._maximumWidth is not None and self._maximumHeight is not None:
            self.setMaximumSize(self._maximumWidth, self._maximumHeight)

        if self._icon is not None:
            self.setIcon(self._icon)

    def __style__(self):
        label = f"""
            QLabel {{
                color: {self._text_color};
            }}
        """ if self._text_color else ""

        style_sheet = f"""
            #{self._objectName} {{
                color: {self._text_color};
                background-color: {self._bg_color};
            }}
            {label}
            {self._toolTip.styleSheet()}
        """

    def update_styles(self):
        label = f"""
            QLabel {{
                color: {self._text_color};
            }}
        """ if self._text_color else ""

        style_sheet = f"""
            #{self._objectName} {{
                color: {self._text_color};
                background-color: {self._bg_color};
            }}
            {label}
            {self._toolTip.styleSheet()}
        """
        self.setStyleSheet(style_sheet)
        self.update()

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
