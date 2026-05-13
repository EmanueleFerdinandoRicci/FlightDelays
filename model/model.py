import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._airports = DAO.getAllAirports()
        self._idMapAirports = {}
        for a in self._airports:
            self._idMapAirports[a.ID] = a

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