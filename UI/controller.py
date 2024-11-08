import flet as ft
from UI.view import View
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self.stato = None

    def fillDDyear(self):
        avvistamenti = self._model.listaSighting
        listaAnni = []
        for a in avvistamenti:
            if a.datetime.year not in listaAnni:
                listaAnni.append(a.datetime.year)
        for i in listaAnni:
            self._view.ddyear.options.append(ft.dropdown.Option(i))
        self._view.update_page()

    def fillDDstate(self, e):
        self._view.ddstate.options.clear()
        self._view.ddstate.value = None
        anno = int(self._view.ddyear.value)
        stati = self._model.getStatiAnno(anno)
        for s in stati:
            self._view.ddstate.options.append(ft.dropdown.Option(text=s.name,
                                                                 data=s,
                                                                 on_click=self.readStato))
        self._view.update_page()

    def readStato(self, e):
        if e.control.data is None:
            self._view.create_alert(("Popolare menù a tendina"))
            return
        else:
            self.stato = e.control.data

    def handle_graph(self, e):
        anno = self._view.ddyear.value
        self._model.creaGrafo(anno, self.stato)
        nNodes = self._model.getNumNodes()
        nEdges = self._model.getNumEdges()
        numCompCon = self._model.getNumCompConn()
        compCon = self._model.getCompConMax()
        lunghezza = len(compCon)
        self._view.txt_result1.controls.clear()
        self._view.txt_result1.controls.append(ft.Text(f"Numero di vertici: {nNodes}"))
        self._view.txt_result1.controls.append(ft.Text(f"Numero di archi: {nEdges}"))
        self._view.txt_result1.controls.append(ft.Text(f"Numero di componenti connesse: {numCompCon}"))
        self._view.txt_result1.controls.append(ft.Text(f"Componente connessa maggiore ha {lunghezza} nodi:"))
        for c in compCon:
            self._view.txt_result1.controls.append(ft.Text(f"{c}"))
        self._view.update_page()

    def handle_path(self, e):
        pass

