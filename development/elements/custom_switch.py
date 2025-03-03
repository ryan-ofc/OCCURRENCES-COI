from PySide6.QtWidgets import QCheckBox, QWidget, QVBoxLayout, QApplication, QFrame
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QPoint
from development.styles import Colors, Border, type_border
from development.elements import CTooltip


class CSwitch(QCheckBox):
    def __init__(self, on_switch=None, bg_color: Colors = Colors.gray, text_color: Colors = Colors.white, parent=None):
        super().__init__(parent)
        self.on_switch = on_switch
        self._bg_color = bg_color
        self._text_color = text_color
        self.stateChanged.connect(self.switch)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        # Configurações iniciais
        self.setFixedSize(70, 30)

        # Criando o QFrame para a bolinha
        self._circle = QFrame(self)
        self._circle.setFixedSize(24, 24)
        self._circle.setStyleSheet("background-color: white; border-radius: 12px;")

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

        # Estilo personalizado
        self.setStyleSheet(
            F"""
            CSwitch {{
                background-color: {self._bg_color};
                border-radius: 15px;
                border: 2px solid #ccc;
                padding: 0px;
            }}
            CSwitch:checked {{
                background-color: #4CAF50;
            }}
            CSwitch::indicator {{
                width: 0px;
                height: 0px;
                border: none;
                padding: 0px;
                margin: 0px;
            }}
            {self._toolTip.styleSheet()}
        """
        )

        # Definindo a animação como um atributo de classe
        self._animation = QPropertyAnimation(self._circle, b"pos")
        self._animation.setDuration(300)
        self._animation.setEasingCurve(QEasingCurve.InOutQuad)

        # Conectar a animação ao método que reativa o switch
        self._animation.finished.connect(self.enableSwitch)

        # Definir posição inicial correta da bolinha
        self.updatePosition()

    def updatePosition(self):
        """Atualiza a posição da bolinha com base no estado atual do switch"""
        end_x = (
            self.rect().width() - self._circle.width() - 3 if self.isChecked() else 3
        )
        self._circle.move(end_x, 3)  # Posiciona corretamente sem animação

    def switch(self, state):
        """Chama a função de troca de estado e inicia a animação."""
        if self.on_switch:
            self.on_switch(state)

        # Desabilita temporariamente para evitar múltiplos cliques
        self.setEnabled(False)

        # Atualiza a posição final da animação com base no estado
        end_x = (
            self.rect().width() - self._circle.width() - 3 if self.isChecked() else 3
        )

        self._animation.setStartValue(self._circle.pos())
        self._animation.setEndValue(QPoint(end_x, self._circle.y()))
        self._animation.start()

    def enableSwitch(self):
        """Reativa o switch após a animação terminar."""
        self.setEnabled(True)

    def mousePressEvent(self, event):
        """Intercepta o clique e alterna o estado manualmente, mas só permite se estiver habilitado."""
        if self.isEnabled():
            self.setChecked(not self.isChecked())  # Alterna o estado ao clicar
            super().mousePressEvent(event)  # Chama o evento original


# Código para inicializar a aplicação
if __name__ == "__main__":
    app = QApplication([])

    window = QWidget()
    layout = QVBoxLayout()

    switch = CSwitch()
    layout.addWidget(switch)

    window.setLayout(layout)
    window.setWindowTitle("Custom Switch")
    window.show()

    app.exec()
