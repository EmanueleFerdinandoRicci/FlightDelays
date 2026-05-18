import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._airports = DAO.getAllAirports()
        self._idMapAirports = {}
        for a in self._airports:
            self._idMapAirports[a.ID] = a
        self._bestCammino = []
        self._bestScore = 0

    def buildGraph(self,nMin):
        nodes = DAO.getAllNodes(nMin, self._idMapAirports)
        self._graph.add_nodes_from(nodes)
        print(f"N nodi: {len(self._graph.nodes)}, n archi: {len(self._graph.edges)}")
        self.getAllEdges()
        print(f"N nodi: {len(self._graph.nodes)}, n archi: {len(self._graph.edges)}")
        self._graph.clear_edges()
        self.getAllEdgesV2()
        print(f"N nodi: {len(self._graph.nodes)}, n archi: {len(self._graph.edges)}")

    def getAllEdges(self):
        allTratte = DAO.getAllEdgesV1(self._idMapAirports)
        #queste tratte hanno 2 problemi:
        # 1 ho archi diretti e inversi e quindi dovrò sommarli
        # 2 ho archi fra aereoporti che avevo filtrato

        for t in allTratte:
            if t.airportP in self._graph and t.airportA in self._graph:
                #allora posso aggiungerlo
                if self._graph.has_edge(t.airportP, t.airportA):
                    self._graph[t.airportP][t.airportA]['weight'] += t.peso
                else:
                    self._graph.add_edge(t.airportP, t.airportA, weight=t.peso)

    def getAllEdgesV2(self):
        allTratte = DAO.getAllEdgesV2(self._idMapAirports)

        for t in allTratte:
            if t.airportP in self._graph and t.airportA in self._graph:
                self._graph.add_edge(t.airportP, t.airportA, weight=t.peso)

    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def getAllNodes(self):
        nodes = list(self._graph.nodes)
        nodes.sort(key = lambda x: x.IATA_CODE)
        return nodes

    def getViciniOrdinati(self,source):
        #restituisce tutti i vicini di source, ordinati per peso dell'arco
        vicini = self._graph.neighbors(source)
        viciniT = []
        for v in vicini:
            viciniT.append((v, self._graph[source][v]["weight"]))
        viciniT.sort(key = lambda x:x[1],reverse=True)
        return viciniT

    def hasPath(self,v0,v1):
        #restituisce true se un qualche cammino fra v0 e v1 esiste
        return v1 in nx.node_connected_component(self._graph, v0)

    def getPath(self,v0,v1):
        #v1
        #dictOfPredecessors = dict(nx.bfs_predecessors(self._graph,v0))
        #path = [v1]
        #while path[0] != v[0]:
        #    path.insert(0,dictOfPredecessors[path[0]])

        #v2
        #dictOfPredecessors = dict(nx.dfs_predecessors(self._graph, v0))
        #path = [v1]
        #while path[0] != v[0]:
        #    path.insert(0, dictOfPredecessors[path[0]])

        #v3
        #path = nx.shortest_path(v0,v1)

        #v4
        path = nx.dijkstra_path(self._graph,v0,v1, weight = None)
        return path

    def getCamminoOttimo(self,v0,v1,t):
        self._bestCammino = []
        self._bestScore = 0

        parziale = [v0]

        self._ricorsione(parziale,v1,t)

    def _ricorsione(self,parziale,v1,t):
        #verifico se parziale è soluzione valid, in caso salvo
        if parziale[-1] == v1: #potenzialmente buona
            if self._getScore(parziale) > self._bestScore:
                self._bestCammino = copy.deepcopy(parziale)
                self._bestScore = self._getScore(parziale)
        #verifico se ha senso continuare ad aggiungere elementi in parziale o esco
        if len(parziale) == t+1: #allora parziale ha già raggiunto il numero max di tratte
            return
        #espando parziale e facciamo tentativi in backtracking
        for n in self._graph.neighbors(parziale[-1]):
            if n not in parziale:
                parziale.append(n)
                self._ricorsione(parziale,v1,t)
                parziale.pop()

        return self._bestCammino,self._bestScore

    def _getScore(self, parziale):
        sumPesi = 0
        for i in range(0,len(parziale)-1):
            sumPesi += self._graph[parziale[i]][parziale[i+1]]["weight"]

        return sumPesi