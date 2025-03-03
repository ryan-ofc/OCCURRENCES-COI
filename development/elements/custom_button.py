from PySide6.QtWidgets import QPushButton
from development.styles import Colors, Border, type_border, Padding, BorderRadius
from development.model import Instances

class CButton(QPushButton, Instances):
    def __init__(
        self,
        text: str = "CButton",
        objectName: str = "CButton",
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
        onClick=None,
    ):
        super().__init__(text)
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
        
        self.setObjectName(objectName)
        
        if onClick:
            self.clicked.connect(onClick)

        self.__setup__()

    def __setup__(self):
        self.__config__()
        self.__style__()

    def __config__(self):
        if self._width is not None and self._height is not None:
            self.resize(self._width, self._height)
        
        if self._minimumWidth is not None and self._minimumHeight is not None:
            self.setMinimumSize(self._minimumWidth, self._minimumHeight)
        
        if self._maximumWidth is not None and self._maximumHeight is not None:
            self.setMaximumSize(self._maximumWidth, self._maximumHeight)

    def __style__(self):
        self.update_styles()

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
            QPushButton {{
                font-size: 12px;
                font-weight: bold;
                text-align: center;
            }}
            {hover_style}
            {border}
            {border_radius}
            {padding}
            {hover_border}
        """
        self.setStyleSheet(style_sheet)
        self.update()
