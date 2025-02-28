from development.styles.colors import Colors


class WindowStyle:
    def __init__(self, bg_color):
        self.bg_color = bg_color


class Themes:
    class light:
        window = WindowStyle(bg_color=Colors.gray.adjust_tonality(100))

    class dark:
        window = WindowStyle(bg_color=Colors.black.adjust_tonality(65))
