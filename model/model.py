from database.dao import DAO
import networkx as nx

class Model:
    def __init__(self):
        self.lista_categorie = []
        self.grafo = None


    def get_date_range(self):
        return DAO.get_date_range()


    def getRangeFiltrato(self, category_id):
        return DAO.leggiDateFiltrate(category_id)


    def getCategorie(self):
        self.lista_categorie = DAO.leggiCategorie()


    def creaGrafo(self, category_id, data_inizio, data_fine):
        prodotti_data_la_categoria = DAO.cercaProdotti(category_id)         # lista di id prodotti [4, 54, 55, 114, ...]
        self.grafo = None
        self.grafo = nx.DiGraph()
        self.grafo.add_nodes_from(prodotti_data_la_categoria)
        for p1 in prodotti_data_la_categoria:
            for p2 in prodotti_data_la_categoria:
                if p1 != p2:
                    ordini_p1 = DAO.cercaOrdini(p1)
                    ordini_p2 = DAO.cercaOrdini(p2)
                    vendite_p1 = 0
                    vendite_p2 = 0
                    for o1 in ordini_p1:
                        vendite_p1 += DAO.cercaVendita(o1, data_inizio, data_fine)
                    for o2 in ordini_p2:
                        vendite_p2 += DAO.cercaVendita(o2, data_inizio, data_fine)
                    if vendite_p1 != 0 and vendite_p2 != 0:
                        peso = vendite_p1 + vendite_p2
                        if vendite_p1 > vendite_p2:
                            self.grafo.add_edge(p1, p2, weight = peso)
                        elif vendite_p2 > vendite_p1:
                            self.grafo.add_edge(p2, p1, weight = peso)
                        elif vendite_p1 == vendite_p2:
                            self.grafo.add_edge(p1, p2, weight = peso)
                            self.grafo.add_edge(p2, p1, weight = peso)