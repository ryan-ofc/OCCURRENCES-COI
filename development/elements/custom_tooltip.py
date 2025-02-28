from development.styles import Colors, Border


class CTooltip:
    def __init__(
        self,
        bg_color: Colors,
        color: Colors,
        border: Border,
        border_radius: int,
        padding: int,
        font_size: int,
    ):
        self.bg_color = bg_color
        self.color = color
        self.border = border
        self.border_radius = border_radius
        self.padding = padding
        self.font_size = font_size

    def styleSheet(self) -> str:
        style = f"""            
            QToolTip {{
                background-color: {self.bg_color};
                color: {self.color};
                border: {self.border};
                padding: {self.padding}px;
                border-radius: {self.border_radius}px;
                font-size: {self.font_size}px;
            }}"""
        return str(style)

    def setStyleSheet(
        self,
        bg_color: Colors = None,
        color: Colors = None,
        border: Border = None,
        border_radius: int = None,
        padding: int = None,
        font_size: int = None,
    ):
        if bg_color is not None:
            self.bg_color = bg_color
        if color is not None:
            self.color = color
        if border is not None:
            self.border = border
        if border_radius is not None:
            self.border_radius = border_radius
        if padding is not None:
            self.padding = padding
        if font_size is not None:
            self.font_size = font_size
