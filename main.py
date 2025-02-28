from development import (
    CMainWindow,
    Colors,
    QApplication,
    rgba,
    CLayout,
    CFrame,
    Navbar,
    sys,
)


class App(CMainWindow):
    def __init__(
        self,
        title="Cadastro de ocorrências",
        width=720,
        height=500,
        minimumWidth=None,
        minimumHeight=None,
        maximumWidth=None,
        maximumHeight=None,
        bg_color: rgba = Colors.gray.adjust_tonality(100),
        text_color: rgba = Colors.black,
        icon: str | bytes = "app/icons/svg/icon.svg",
    ):

        super().__init__(
            title=title,
            width=width,
            height=height,
            minimumWidth=minimumWidth,
            minimumHeight=minimumHeight,
            maximumWidth=maximumWidth,
            maximumHeight=maximumHeight,
            bg_color=bg_color,
            text_color=text_color,
            icon=icon,
        )
        self.central_widget = CFrame(
            maximumWidth=4096,
            maximumHeight=2160,
            bg_color=self._bg_color,
        )
        self.setCentralWidget(self.central_widget)
        self.__ui__()
        self.__layout__()
    
    def __ui__(self):
        self.ui_navbar()
        self.ui_content()

    def __layout__(self):
        layout = CLayout(self.central_widget)
        self.main_layout = layout.vertical()

        # add to layout
        self.main_layout.addWidget(self.navbar)
        self.main_layout.addWidget(self.content)

    def ui_navbar(self):
        self.navbar = Navbar(maximumHeight=30,bg_color=Colors.blue.adjust_tonality(80))
    
    def ui_content(self):
        self.content = CFrame(bg_color=self._bg_color)
        
        layout = CLayout(self.content)
        self.content_layout = layout.horizontal(spacing=10)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec())
