from PySide6.QtWidgets import QTextEdit, QLabel, QVBoxLayout, QWidget
from development.styles import Colors, Border, type_border, Border, Padding, BorderRadius
from development.elements import CTooltip
from development.model import Instances
import re


class CTextArea(QWidget, Instances):
    def __init__(
        self,
        label: str = "",
        placeholder: str = "",
        objectName: str = "CTextArea",
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
        only_numbers: bool = False,
        no_special_chars: bool = False,
        only_uppercase: bool = False,
        value: str = None,
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
        )

        self.only_numbers = only_numbers
        self.no_special_chars = no_special_chars
        self.only_uppercase = only_uppercase
        self.value = value

        self.label = QLabel(label)
        self.text_area = QTextEdit()
        self.text_area.setObjectName(objectName)
        self.text_area.setPlaceholderText(placeholder)

        if self.value:
            self.text_area.setText(str(self.value))

        self.text_area.textChanged.connect(self.__on_text_changed)
        
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
    
    def __style__(self):
        self.update_styles()
    
    def __layout__(self):
        layout = QVBoxLayout()
        layout.setSpacing(4)
        layout.addWidget(self.label)
        layout.addWidget(self.text_area)
        self.setLayout(layout)
    
    def clear(self):
        self.text_area.clear()

    def text(self):
        return self.text_area.toPlainText()
    
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
            QLabel {{
                font-size: 11px;
                padding-left: 5px;
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
        self.text_area.setStyleSheet(style_sheet)
        self.label.setStyleSheet(style_sheet)
        self.update()

    def apply_filters(self, text: str) -> str:
        if self.only_numbers:
            text = re.sub(r'\D', '', text)
        if self.no_special_chars:
            text = re.sub(r'[^a-zA-Z0-9 ]', '', text)
        if self.only_uppercase:
            text = text.upper()
        return text
    
    def __on_text_changed(self):
        text = self.text_area.toPlainText()
        filtered_text = self.apply_filters(text)

        # Armazena a posição do cursor antes da alteração
        cursor_position = self.text_area.textCursor().position()

        self.text_area.blockSignals(True)

        # Só altera o texto após salvar a posição do cursor
        self.text_area.setPlainText(filtered_text)

        # Restaura a posição do cursor para onde estava antes da alteração
        cursor = self.text_area.textCursor()
        cursor.setPosition(cursor_position if cursor_position <= len(filtered_text) else len(filtered_text))
        self.text_area.setTextCursor(cursor)

        self.text_area.blockSignals(False)

    def setOnlyNumbers(self, role: bool):
        self.only_numbers = role

    def setNoSpecialChars(self, role: bool):
        self.no_special_chars = role

    def setOnlyUppercase(self, role: bool):
        self.only_uppercase = role