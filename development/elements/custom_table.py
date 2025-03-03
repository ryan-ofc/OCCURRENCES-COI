from PySide6.QtWidgets import QTableWidget, QTableWidgetItem
from development.styles import Colors, Border, BorderRadius, type_border
from development.elements import CTooltip
from development.model import Instances

class CTable(QTableWidget, Instances):
    def __init__(
        self,
        objectName: str = "CTable",
        rows: int = 0,
        columns: int = 0,
        width: int = None,
        height: int = None,
        minimumWidth: int = None,
        minimumHeight: int = None,
        maximumWidth: int = 4096,
        maximumHeight: int = 2160,
        bg_color: Colors = Colors.white,
        border: Border = None,
        border_radius: BorderRadius = None,
        hover_bg_color: Colors = None,
        hover_border: Border = None,
        text_color: Colors = Colors.black.adjust_tonality(75),
    ):
        QTableWidget.__init__(self, rows, columns)
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
            border_radius=border_radius,
            text_color=text_color,
        )

        self._toolTip = CTooltip(
            bg_color=self._bg_color,
            color=self._text_color,
            border=Border(pixel=1, type_border=type_border.solid, color=self._text_color),
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
        style_sheet = f"""
            #{self._objectName} {{
                color: {self._text_color};
                background-color: {self._bg_color};
                border: {self._border if self._border else 'none'};
                border-radius: {self._border_radius if self._border_radius else '0px'};
            }}
            {self._toolTip.styleSheet()}
        """
        self.setStyleSheet(style_sheet)

    def set_headers(self, headers: list[str]):
        self.setColumnCount(len(headers))
        self.setHorizontalHeaderLabels(headers)

    def add_row(self, row_data: list[str]):
        row_position = self.rowCount()
        self.insertRow(row_position)
        for col, data in enumerate(row_data):
            self.setItem(row_position, col, QTableWidgetItem(data))
