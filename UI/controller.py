from ast import operator
from operator import itemgetter
import operator as operator
from UI.view import View
from model.model import Model
import flet as ft
import datetime

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model
        self.categoria_scelta = None        # viene salvata la key, ovvero l'id della categoria
        self.data_inizio = None             # datetime yyyy:mm:dd hh:mm:ss
        self.data_fine = None               # datetime yyyy:mm:dd hh:mm:ss


    def set_dates(self):
        first, last = self._model.get_date_range()

        self._view.dp1.first_date = datetime.date(first.year, first.month, first.day)
        self._view.dp1.last_date = datetime.date(last.year, last.month, last.day)
        self._view.dp1.current_date = datetime.date(first.year, first.month, first.day)

        self._view.dp2.first_date = datetime.date(first.year, first.month, first.day)
        self._view.dp2.last_date = datetime.date(last.year, last.month, last.day)
        self._view.dp2.current_date = datetime.date(last.year, last.month, last.day)


    def handleChangeCategoria(self, e):
        self.categoria_scelta = e.control.value
        if self.categoria_scelta is None:
            return
        first, last = self._model.getRangeFiltrato(self.categoria_scelta)

        self._view.dp1.first_date = datetime.date(first.year, first.month, first.day)
        self._view.dp1.last_date = datetime.date(last.year, last.month, last.day)
        self._view.dp1.current_date = datetime.date(first.year, first.month, first.day)

        self._view.dp2.first_date = datetime.date(first.year, first.month, first.day)
        self._view.dp2.last_date = datetime.date(last.year, last.month, last.day)
        self._view.dp2.current_date = datetime.date(last.year, last.month, last.day)


    def popolaDropdown(self, dd):
        dd.options.clear()
        self._model.getCategorie()
        for c in self._model.lista_categorie:
            dd.options.append(ft.dropdown.Option(key = c.id, text=c.category_name))


    def handleChangeDate(self, e):
        self.data_inizio = self._view.dp1.value
        self.data_fine = self._view.dp2.value
        if self.data_inizio is None or self.data_fine is None:
            return
        print(self.data_inizio, self.data_fine)


    def handle_crea_grafo(self, e):
        """ Handler per gestire creazione del grafo """
        if (self.categoria_scelta is not None) and (self.data_inizio is not None) and (self.data_fine is not None):
            self._model.creaGrafo(self.categoria_scelta, self.data_inizio, self.data_fine)
            self._view.txt_risultato.controls.clear()
            self._view.txt_risultato.controls.append(ft.Text(f"Categoria scelta: {self.categoria_scelta}"))
            self._view.txt_risultato.controls.append(ft.Text(f"Data di inizio: {self.data_inizio}"))
            self._view.txt_risultato.controls.append(ft.Text(f"Data di finne: {self.data_fine}"))
            self._view.txt_risultato.controls.append(ft.Text(""))
            self._view.txt_risultato.controls.append(ft.Text("Dettagli del grafo creato: "))
            self._view.txt_risultato.controls.append(ft.Text(f"Numero di nodi: {self._model.grafo.number_of_nodes()}"))
            self._view.txt_risultato.controls.append(ft.Text(f"Numero di archi: {self._model.grafo.number_of_edges()}"))
            self._view.page.update()

    def handle_best_prodotti(self, e):
        """ Handler per gestire la ricerca dei prodotti migliori """
        punteggi = {}
        for nodo in self._model.grafo.nodes:
            pesi_uscenti = sum(self._model.grafo[nodo][v]["weight"] for v in self._model.grafo.successors(nodo))
            pesi_entranti = sum(self._model.grafo[v][nodo]["weight"] for v in self._model.grafo.predecessors(nodo))
            score = pesi_uscenti - pesi_entranti
            punteggi[nodo] = score
        ordine_decrescente = sorted(punteggi.items(), key=operator.itemgetter(1), reverse=True)
        self._view.txt_risultato.controls.clear()
        self._view.txt_risultato.controls.append(ft.Text("TOP 5 prodotti più venduti: "))
        for nodo, score in ordine_decrescente[:5]:
            self._view.txt_risultato.controls.append(ft.Text(f"Nodo {nodo} con archi uscenti - archi entranti pari a {score}"))
            self._view.page.update()


    def handle_cerca_cammino(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del cammino """
        # TODO
