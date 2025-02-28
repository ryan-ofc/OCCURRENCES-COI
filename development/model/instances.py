from development.styles.colors import Colors
from development.styles.border import Border


class Instances:
    def __init__(
        self,
        objectName: str = None,
        spacing: int = None,
        title: str = None,
        width: int = None,
        height: int = None,
        minimumWidth: int = 0,
        minimumHeight: int = 0,
        maximumWidth: int = 4096,
        maximumHeight: int = 2160,
        bg_color: Colors = None,
        text_color: Colors = None,
        icon: str | bytes = None,
        hover_bg_color: Colors = None,
        hover_text_color: Colors = None,
        hover_border: Border = None,
    ):
        self._objectName = objectName
        self._spacing = spacing
        self._title = title
        self._width = width
        self._height = height
        self._minimumWidth = minimumWidth
        self._minimumHeight = minimumHeight
        self._maximumWidth = maximumWidth
        self._maximumHeight = maximumHeight
        self._bg_color = bg_color
        self._text_color = text_color
        self._hover_text_color = hover_text_color
        self._icon = icon
        self._hover_bg_color = hover_bg_color
        self._hover_border = hover_border
