from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self.listaStati = DAO.get_all_states()
        self.mapStati = {}
        for s in self.listaStati:
            self.mapStati[s.id] = s
        self.listaSighting = DAO.get_all_sightings()
        self.mapSighting = {}
        for a in self.listaSighting:
            self.mapSighting[a.id] = a
        self.grafo = nx.Graph()

    def getStatiAnno(self, anno):
        return DAO.getStatiAnno(anno)

    def creaGrafo(self, anno, stato):
        self.grafo.clear()
        idStato = stato.id
        listaNodi = DAO.getNodi(anno, idStato)
        self.grafo.add_nodes_from(listaNodi)
        listArchi = DAO.getSightingShape(self.mapSighting, anno, idStato)
        for t in listArchi:
            sigh1 = t[0]
            sigh2 = t[1]
            if sigh1.distance_HV(sigh2) < 100:
                self.grafo.add_edge(sigh1, sigh2)

    def getNumCompConn(self):
        numero = nx.number_connected_components(self.grafo)
        return numero

    def getCompConMax(self):
        largest_cc = max(nx.connected_components(self.grafo), key=len)
        return largest_cc

    def getNumNodes(self):
        return len(self.grafo.nodes())

    def getNumEdges(self):
        return len(self.grafo.edges())


