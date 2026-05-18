import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        # page stuff
        self._page = page
        self._page.title = "Template application using MVC and DAO"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.DARK
        self._page.window_width = 700
        # controller (it is not initialized. Must be initialized in the main, after the controller is created)
        self._controller = None
        # graphical elements
        self._title = None
        self.txt_name = None
        self.btn_hello = None
        self.txt_result = None
        self.txt_container = None

    def load_interface(self):
        #ROW1
        self._txtInCmin = ft.TextField(label="N min compagnie")
        self._btnAnalizzaAereoporti = ft.ElevatedButton(text="Analizza Aereoporti", on_click=self._controller.handleAnalizza)
        row1 = ft.Row([ft.Container(self._txtInCmin,width=250),ft.Container(self._btnAnalizzaAereoporti,width=250)],alignment=ft.MainAxisAlignment.CENTER)

        #ROW2
        self._ddAereoportoP = ft.Dropdown(label="Aereoporto di Partenza")
        self._btnAereoportiConnessi = ft.ElevatedButton(text="Aereoporti Connessi", on_click = self._controller.handleConnessi)
        self._ddAereoportoA = ft.Dropdown(label="Aereoporto di Arrivo")
        self._btnTestConnessione = ft.ElevatedButton(text="Test Connessione", on_click=self._controller.handleTestConnessione)
        row2 = ft.Row([ft.Container( self._ddAereoportoP,width=150),ft.Container(self._btnAereoportiConnessi,width=150),ft.Container(self._ddAereoportoA, width=150), ft.Container(self._btnTestConnessione,width=150)],alignment=ft.MainAxisAlignment.CENTER)

        #ROW3
        self._txtInTratteMax =ft.TextField(label="N max tratte")
        self._btnCercaItinerario = ft.ElevatedButton(text="Cerca Itinerario", on_click=self._controller.handleCercaItinerario)

        row3 = ft.Row([ ft.Container(self._txtInTratteMax, width=250),
                       ft.Container(self._btnCercaItinerario, width=250)], alignment=ft.MainAxisAlignment.CENTER)

        self._txtResults = ft.ListView(expand = 1,
                                       spacing=10,
                                       padding=20,
                                       auto_scroll=True)

        self._page.add(row1,row2,row3,self._txtResults)
        self._page.update()



    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    def create_alert(self, message):
        dlg = ft.AlertDialog(title=ft.Text(message))
        self._page.dialog = dlg
        dlg.open = True
        self._page.update()

    def update_page(self):
        self._page.update()
