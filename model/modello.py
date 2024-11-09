import copy

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
        self.path = []
        self.punteggio = 0

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

    def getPath(self):
        self.path = []
        self.punteggio = 0
        parziale = []
        contatoriMese = {}
        for i in range(1, 13):
            contatoriMese[i] = 0
        for node in self.grafo.nodes():
            parziale.append(node)
            contatoriMese[node.mese] += 1
            self.ricorsione(parziale, contatoriMese)
            parziale.remove(node)
            contatoriMese[node.mese] -= 1
        return self.path, self.punteggio

    def ricorsione(self, parziale, contatoriMese):
        vicini = list(self.grafo.neighbors(parziale[-1]))
        #TERMINAZIONE
        viciniMax = []
        for i in vicini:
            if i.duration > parziale[-1].duration:
                viciniMax.append(i)
        if len(viciniMax) == 0:
            if self.getPuntCam(parziale) > self.punteggio:
                self.punteggio = self.getPuntCam(parziale)
                self.path = copy.deepcopy(parziale)
        else:
            for n in vicini:
                if n.duration > parziale[-1].duration:
                    if contatoriMese[n.mese] < 3:
                        parziale.append(n)
                        contatoriMese[n.mese] += 1
                        self.ricorsione(parziale, contatoriMese)
                        parziale.pop()
                        contatoriMese[n.mese] -= 1

    def getPuntCam(self, parziale):
        punteggio = 0
        for i in range(len(parziale)):
            if i == 0:
                punteggio += 100
            else:
                if parziale[i].mese == parziale[i-1].mese:
                    punteggio += 200
                else:
                    punteggio += 100
        return punteggio



