from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView, QApplication
from development.styles import Colors, Border, BorderRadius, type_border
from development.elements import CTooltip
from development.model import Instances
from .custom_button import CButton
from .custom_messagebox import CMessageBox


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
        vertical: bool = True,
        horizontal: bool = True,
        fg_color: Colors = Colors.gray.adjust_tonality(70)
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
        self._fg_color = fg_color
        self._toolTip = CTooltip(
            bg_color=self._bg_color,
            color=self._text_color,
            border=Border(
                pixel=1, type_border=type_border.solid, color=self._text_color
            ),
            border_radius=3,
            padding=5,
            font_size=12,
        )

        self.header = self.horizontalHeader()
        self.header.setHidden(not horizontal)
        self.header.setStyleSheet(
            f"background-color: {self._bg_color}; color: {self._text_color};"
        )

        self.header_vertical = self.verticalHeader()
        self.header_vertical.setStyleSheet(
            f"background-color: {self._bg_color}; color: {self._text_color};"
        )
        self.header_vertical.setHidden(not vertical)

        for i in range(self.columnCount()):
            self.header.setSectionResizeMode(i, QHeaderView.Stretch)

        self.header.setStretchLastSection(True)
        self.setEditTriggers(QTableWidget.NoEditTriggers)

        self.itemDoubleClicked.connect(self.clipboard_row)

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

    def clipboard_row(self, item):
        row_index = item.row()
        column_index = item.column()
        cell_value = item.text()

        if cell_value is not None and cell_value != "N/A" and cell_value != "":
            clipboard = QApplication.clipboard()
            clipboard.setText(cell_value)

            message = CMessageBox(self,title="Notificação",text=f"Valor: [{cell_value}] copiado para área de transferência.")
            message.show()

    def get_row_values(self, row_index: int):
        row_values = []
        for column in range(self.columnCount()):
            item = self.item(row_index, column)
            row_values.append(item.text() if item else "")
        return row_values

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
                border: {self._border if self._border else 'none'};
            }}
            QTableWidget::item:selected {{
                background-color: {self._fg_color};
            }}
            {border_radius}
            {self._toolTip.styleSheet()}
        """
        self.setStyleSheet(style_sheet)
        self.header.setStyleSheet(
            f"background-color: {self._bg_color}; color: {self._text_color};"
        )
        self.header_vertical.setStyleSheet(
            f"background-color: {self._bg_color}; color: {self._text_color};"
        )
        for row in range(self.rowCount()):
            cell_widget = self.cellWidget(row, self.columnCount() - 1)
            if isinstance(cell_widget, CButton):
                cell_widget._bg_color = self._bg_color
                cell_widget.update_styles()

    def set_headers(self, headers: list[str]):
        self.setColumnCount(len(headers))
        self.setHorizontalHeaderLabels(headers)

    def add_row(self, row_data: list[str]):
        row_position = self.rowCount()
        self.insertRow(row_position)
        
        # Adicionar os dados da linha
        for col, data in enumerate(row_data):
            self.setItem(row_position, col, QTableWidgetItem(data))
        
        # Adicionar o botão de lápis na última coluna
        edit_button = CButton(text="✏️", bg_color=self._bg_color, border_radius=BorderRadius(all=0))
        edit_button.clicked.connect(lambda: self.edit_row(row_position))
        self.setCellWidget(row_position, len(row_data), edit_button)

    def edit_row(self, row_index: int):
        data = self.get_row_values(row_index)
        print(data)
