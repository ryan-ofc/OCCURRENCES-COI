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
    OccurrenceForm,
    BorderRadius,
    Border,
    type_border,
    Qt,
    SQLiteManager,
    CTable,
    os,
    time,
    sys,
)


class App(CMainWindow):
    def __init__(
        self,
        title="Cadastro de ocorrências",
        width=500,
        height=600,
        minimumWidth=500,
        minimumHeight=600,
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
        self.theme: Themes = Themes.light
        self.theme_light = Themes.light
        self.theme_dark = Themes.dark
        self.search = None
        self.page = 1
        self.rows = 17
        self.total_pages = None
        self.total_rows = None
        self.central_widget = CFrame(
            maximumWidth=4096,
            maximumHeight=2160,
            bg_color=self._bg_color,
        )
        self.setCentralWidget(self.central_widget)
        self.create_db()
        self.__ui__()
        self.__layout__()

    def __ui__(self):
        self.ui_navbar()
        self.ui_content()
        self.ui_toggle_theme()
        self.ui_occurrence_form()
        self.ui_table_occurrences()

    def __layout__(self):
        layout = CLayout(self.central_widget)
        self.main_layout = layout.vertical(spacing=0)

        # add to layout
        self.main_layout.addWidget(self.navbar)
        self.main_layout.addWidget(self.content)

        self.content_layout.addWidget(self.occurrence_form)
        self.content_layout.addWidget(self.table_occurrences)

    def ui_toggle_theme(self):
        self.btn_toggle_theme = ToggleTheme(
            self,
            icon_light="sun.svg",
            icon_dark="moon.svg",
            bg_light=self.theme_light.toggle_theme.bg_color,
            bg_dark=self.theme_dark.toggle_theme.bg_color,
        )
        self.btn_toggle_theme.clicked.connect(self.toggle_theme)

    def ui_navbar(self):
        self.navbar = Navbar(maximumHeight=30, bg_color=Colors.blue.adjust_tonality(90))

    def ui_content(self):
        self.content = CFrame(bg_color=self._bg_color)

        layout = CLayout(self.content)
        self.content_layout = layout.horizontal(spacing=10, margins=(5, 5, 5, 5))

    def ui_occurrence_form(self):
        self.occurrence_form = OccurrenceForm(
            bg_color=self.theme_light.occurrenceForm.bg_color,
            text_color=self.theme_light.occurrenceForm.text_color,
            minimumWidth=485,
            minimumHeight=585,
            maximumWidth=485,
            maximumHeight=585,
            border_radius=BorderRadius(all=8),
            border=Border(
                pixel=1,
                type_border=type_border.solid,
                color=Colors.gray.adjust_tonality(80),
            ),
        )

    def ui_table_occurrences(self):
        self.table_occurrences = CTable(
            columns=9,
            rows=0,
            vertical=False,
            bg_color=self.theme_light.occurrenceForm.bg_color,
            text_color=self.theme_light.occurrenceForm.text_color,
            maximumHeight=585,
            maximumWidth=1200,
            next_action=self.next_page,
            previous_action=self.previous_page,
            border_radius=BorderRadius(bottom_left=8,bottom_right=8),
            border=Border(
                pixel=1,
                type_border=type_border.solid,
                color=Colors.gray.adjust_tonality(80),
            ),
        )
        self.table_occurrences.set_headers(["ID","Nome","Telefone","Rodovia","Km","Sentido","Problema","Encontra-se","Ponto de referência", "Ações"])
        for oc in self.responseSearch.data:
            self.table_occurrences.add_row([str(oc.id), oc.name, oc.phone, oc.highway, oc.km or "", oc.direction, oc.problem, oc.local, oc.reference_point])

        self.occurrence_form.update_table = self.load_page

    def setThemeLight(self):
        light = self.theme_light

        self.content._bg_color = light.window.bg_color
        self.btn_toggle_theme.bg_light = light.toggle_theme.bg_color
        self.occurrence_form._bg_color = light.occurrenceForm.bg_color
        self.occurrence_form._text_color = light.occurrenceForm.text_color
        self.occurrence_form._input_bg_color = light.occurrenceForm.fg_color
        self.occurrence_form._input_border = light.occurrenceForm.border
        self.table_occurrences._bg_color = light.occurrenceTable.bg_color
        self.table_occurrences._text_color = light.occurrenceTable.text_color
        self.table_occurrences._fg_color = light.occurrenceTable.fg_color

    def setThemeDark(self):
        dark = self.theme_dark

        self.content._bg_color = dark.window.bg_color
        self.btn_toggle_theme.bg_dark = dark.toggle_theme.bg_color
        self.occurrence_form._bg_color = dark.occurrenceForm.bg_color
        self.occurrence_form._text_color = dark.occurrenceForm.text_color
        self.occurrence_form._input_bg_color = dark.occurrenceForm.fg_color
        self.occurrence_form._input_border = dark.occurrenceForm.border
        self.table_occurrences._bg_color = dark.occurrenceTable.bg_color
        self.table_occurrences._text_color = dark.occurrenceTable.text_color
        self.table_occurrences._fg_color = dark.occurrenceTable.fg_color

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
        self.occurrence_form.update_styles()
        self.table_occurrences.update_styles()

        self.btn_toggle_theme.switch_theme()

        time.sleep(1)
        self.show()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.btn_toggle_theme.move(self.width() - 80, self.height() - 58)
        if self.width() < 700 and self.height() < 700:
            self.btn_toggle_theme.hide()
        else:
            self.btn_toggle_theme.show()

        if self.width() <= 1000 and self.height() >= 600:
            self.table_occurrences.hide()
        else:
            self.table_occurrences.show()

        # print(self.width(), self.height())

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return and event.modifiers() & Qt.ControlModifier:
            # Ação para Ctrl + Enter
            self.occurrence_form.save_form()

        elif event.key() == Qt.Key_Backspace and event.modifiers() & Qt.ControlModifier:
            # Ação para Ctrl + Backspace
            self.occurrence_form.clear_form()

        else:
            pass

    def create_db(self):
        db_path = "app/database/database.db"
        db_dir = os.path.dirname(db_path)

        if not os.path.exists(db_dir):
            os.makedirs(db_dir)

        with SQLiteManager(db_name=db_path) as db:
            db.execute(
                """
                CREATE TABLE IF NOT EXISTS occurrences (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    phone TEXT,
                    highway TEXT,
                    km INTEGER,
                    direction TEXT,
                    vehicle TEXT,
                    color TEXT,
                    license_plate TEXT,
                    problem TEXT,
                    occupantes TEXT,
                    local TEXT,
                    reference_point TEXT,
                    observations TEXT,
                    is_vehicle BOOLEAN
                );
            """
            )

            self.responseSearch = db.searchPagination(search=self.search,page=self.page,rows=self.rows)
            self.total_pages = self.responseSearch.total_pages
            self.total_rows = self.responseSearch.total_rows

    def next_page(self):
        if self.page < self.total_pages:
            self.page += 1
            self.load_page()

    def previous_page(self):
        if self.page > 1:
            self.page -= 1
            self.load_page()

    def load_page(self):
        self.table_occurrences.setRowCount(0)

        db_path = "app/database/database.db"

        with SQLiteManager(db_name=db_path) as db:
            response = db.searchPagination(search=self.search, page=self.page, rows=self.rows)
            self.page, self.total_pages, self.total_rows, data = response.page, response.total_pages, response.total_rows, response.data

            for oc in data:
                self.table_occurrences.add_row([str(oc.id), oc.name, oc.phone, oc.highway, oc.km or "", oc.direction, oc.problem, oc.local, oc.reference_point])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec())
