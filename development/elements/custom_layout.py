from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QFormLayout, QGridLayout, QWidget
from typing import Literal


class CLayout:
    def __init__(self, parent: QWidget = None):
        self._parent = parent
        self._current_layout = None

    def horizontal(self, margins: tuple = (0, 0, 0, 0), spacing: int = 0) -> QHBoxLayout:
        """Retorna um layout horizontal (QHBoxLayout) com margens e espaçamento configuráveis."""
        layout = QHBoxLayout(self._parent)
        layout.setContentsMargins(*margins)
        layout.setSpacing(spacing)
        return layout

    def vertical(self, margins: tuple = (0, 0, 0, 0), spacing: int = 0) -> QVBoxLayout:
        """Retorna um layout vertical (QVBoxLayout) com margens e espaçamento configuráveis."""
        layout = QVBoxLayout(self._parent)
        layout.setContentsMargins(*margins)
        layout.setSpacing(spacing)
        return layout

    def form(self, margins: tuple = (0, 0, 0, 0), spacing: int = 0) -> QFormLayout:
        """Retorna um layout de formulário (QFormLayout) com margens e espaçamento configuráveis."""
        layout = QFormLayout(self._parent)
        layout.setContentsMargins(*margins)
        layout.setSpacing(spacing)
        return layout

    def grid(self, margins: tuple = (0, 0, 0, 0), spacing: int = 0) -> QGridLayout:
        """Retorna um layout de grade (QGridLayout) com margens e espaçamento configuráveis."""
        layout = QGridLayout(self._parent)
        layout.setContentsMargins(*margins)
        layout.setSpacing(spacing)
        return layout

    def setLayout(self, layout):
        """Define o layout no widget pai."""
        if self._parent:
            self._parent.setLayout(layout)

    def change_layout(self, layout_type: Literal['h', 'v', 'f', 'g', 'horizontal', 'vertical', 'form', 'grid'], margins: tuple = (0, 0, 0, 0), spacing: int = 0):
        """Altera o layout dinamicamente de acordo com o tipo desejado."""
        if layout_type in ['horizontal', 'h']:
            layout = self.horizontal(margins, spacing)
        elif layout_type in ['vertical', 'v']:
            layout = self.vertical(margins, spacing)
        elif layout_type in ['form', 'f']:
            layout = self.form(margins, spacing)
        elif layout_type in ['grid', 'g']:
            layout = self.grid(margins, spacing)
        else:
            raise ValueError("Tipo de layout desconhecido")

        self.setLayout(layout)