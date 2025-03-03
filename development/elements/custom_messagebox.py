from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QMessageBox, QWidget
from PySide6.QtCore import Qt
from typing import Literal


class ButtonRole:
    def __init__(
        self,
        title: str,
        name: Literal["Yes", "No", "Cancel"],
        role: QMessageBox.ButtonRole,
    ):
        self.title = title
        self.name = name
        self.role = role


class CMessageBox(QDialog):
    def __init__(
        self,
        parent: QWidget,
        title: str,
        text: str,
        buttons: list[ButtonRole] = [
            ButtonRole(
                title="Entendido",
                name="Yes",
                role=QMessageBox.ButtonRole.YesRole,
            )
        ],
        icon_type: QMessageBox.Icon = QMessageBox.Icon.Information,
    ):
        super().__init__(parent)
        self.title = title
        self.text = text
        self.buttons = buttons
        self.icon_type = icon_type

        self.setWindowTitle(self.title)
        self.setWindowModality(Qt.ApplicationModal)

        layout = QVBoxLayout(self)

        icon_label = QLabel()
        icon_label.setPixmap(QMessageBox.standardIcon(self.icon_type))
        layout.addWidget(icon_label, alignment=Qt.AlignCenter)

        text_label = QLabel(self.text)
        layout.addWidget(text_label, alignment=Qt.AlignCenter)

        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignCenter)

        for button in self.buttons:
            btn = QPushButton(button.title)
            btn.setDefault(True if button.name == "Yes" else False)
            button_layout.addWidget(btn)

            btn.clicked.connect(lambda _, b=button: self.done_with_button(b.name))

        layout.addLayout(button_layout)

    def done_with_button(self, button_name: str):
        self.button_name = button_name
        self.accept()

    def show(self)-> Literal["Yes","No","Cancel"]:
        if self.exec() == QDialog.Accepted:
            return self.button_name
        return None

    @staticmethod
    def double_choice():
        return [
            ButtonRole(
                title="Sim",
                name="Yes",
                role=QMessageBox.ButtonRole.YesRole,
            ),
            ButtonRole(
                title="Não",
                name="No",
                role=QMessageBox.ButtonRole.YesRole,
            )
        ]
    
    class Icon:
        information = QMessageBox.Icon.Information
        critical = QMessageBox.Icon.Critical
        noIcon = QMessageBox.Icon.NoIcon
        question = QMessageBox.Icon.Question
        warning = QMessageBox.Icon.Warning