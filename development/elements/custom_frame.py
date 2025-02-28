from PySide6.QtWidgets import QFrame
from development.styles import Colors, Border, type_border, Border
from development.elements import CTooltip
from development.model import Instances

class CFrame(QFrame, Instances):
    def __init__(
        self,
        objectName: str = "CFrame",
        width: int = None,
        height: int = None,
        minimumWidth: int = None,
        minimumHeight: int = None,
        maximumWidth: int = 4096,
        maximumHeight: int = 2160,
        bg_color: Colors = Colors.white,
        hover_bg_color: Colors = None,
        hover_border: Border = None,
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

        if self._width is not None and self._height is not None:
            self.resize(self._width, self._height)

        if self._minimumWidth is not None and self._minimumHeight is not None:
            self.setMinimumSize(self._minimumWidth, self._minimumHeight)

        if self._maximumWidth is not None and self._maximumHeight is not None:
            self.setMaximumSize(self._maximumWidth, self._maximumHeight)

    def __style__(self):
        self.update_styles()

    def update_styles(self):
        hover_style = f"""
            #{self._objectName}:hover {{
                background-color: {self._hover_bg_color};
            }}
        """ if self._hover_bg_color else ""

        hover_border = f"""
            #{self._objectName}:hover {{
                border: {self._hover_border};
            }}
        """ if self._hover_border else ""

        style_sheet = f"""
            #{self._objectName} {{
                background-color: {self._bg_color};
            }}
            {hover_style}
            {hover_border}
            {self._toolTip.styleSheet()}
        """
        self.setStyleSheet(style_sheet)
        self.update()

