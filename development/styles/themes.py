from development.styles.colors import Colors
from development.styles.border import Border


class WindowStyle:
    def __init__(self, bg_color = None, fg_color = None, text_color = None, border = None):
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.text_color = text_color
        self.border = border


class Themes:
    class light:
        window = WindowStyle(bg_color=Colors.gray.adjust_tonality(100))
        toggle_theme = WindowStyle(bg_color=Colors.blue)
        occurrenceForm = WindowStyle(bg_color=Colors.white, fg_color=Colors.white.adjust_tonality(40), text_color=Colors.black.adjust_tonality(80), border=Border(color=Colors.gray.adjust_tonality(85)))
        occurrenceTable = WindowStyle(bg_color=Colors.white, fg_color=Colors.gray.adjust_tonality(70), text_color=Colors.black.adjust_tonality(80))

    class dark:
        window = WindowStyle(bg_color=Colors.black.adjust_tonality(65))
        toggle_theme = WindowStyle(bg_color=Colors.black.adjust_tonality(60))
        occurrenceForm = WindowStyle(bg_color=Colors.black.adjust_tonality(60), fg_color=Colors.black.adjust_tonality(70), text_color=Colors.white, border=Border(color=Colors.gray.adjust_tonality(25)))
        occurrenceTable = WindowStyle(bg_color=Colors.black.adjust_tonality(60), fg_color=Colors.gray.adjust_tonality(50), text_color=Colors.white)
