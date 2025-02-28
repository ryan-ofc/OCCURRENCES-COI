from development import (
    CMainWindow,
    Colors,
    QApplication,
    rgba,
    CLayout,
    CFrame,
    Navbar,
    ToggleTheme,
    Themes,
    time,
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
        bg_color: rgba = Colors.gray.adjust_tonality(55),
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
        self.theme: Themes = Themes.light
        self.theme_light = Themes.light
        self.theme_dark = Themes.dark
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
        self.ui_toggle_theme()

    def __layout__(self):
        layout = CLayout(self.central_widget)
        self.main_layout = layout.vertical()

        # add to layout
        self.main_layout.addWidget(self.navbar)
        self.main_layout.addWidget(self.content)

    def ui_toggle_theme(self):
        self.btn_toggle_theme = ToggleTheme(self, icon_light="sun.svg", icon_dark="moon.svg")
        self.btn_toggle_theme.clicked.connect(self.toggle_theme)

    def ui_navbar(self):
        self.navbar = Navbar(maximumHeight=30,bg_color=Colors.blue.adjust_tonality(80))
    
    def ui_content(self):
        self.content = CFrame(bg_color=self._bg_color)
        
        layout = CLayout(self.content)
        self.content_layout = layout.horizontal(spacing=10)

    def setThemeLight(self):
        # window
        self.content._bg_color = self.theme_light.window.bg_color
    
    def setThemeDark(self):
        # window
        self.content._bg_color = self.theme_dark.window.bg_color

    def setTheme(self, theme: Themes):
        if theme == Themes.light:
            self.setThemeLight()
        elif theme == Themes.dark:
            self.setThemeDark()
        else:
            raise ValueError

    def toggle_theme(self):
        self.hide()

        self.theme: Themes = (
            self.theme_light if self.theme == self.theme_dark else self.theme_dark
        )
        self.setTheme(self.theme)
        self.update_styles()
        self.content.update_styles()

        self.btn_toggle_theme.switch_theme()

        time.sleep(1)
        self.show()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.btn_toggle_theme.move(self.width() - 80, self.height() - 58)

        # print(self.width(), self.height())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec())
