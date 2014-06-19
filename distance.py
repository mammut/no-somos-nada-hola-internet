#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Enrutamiento de Vector-Distancia con el algoritmo de Bellman-Ford
"""


class Node(object):
    """
    Representa un nodo dentro del grafo
    """
    def __init__(self, name):
        self.distance = {}
        self.next = {}
        self.name = name

    def to_string(self):
        response = "Nodo {}:[ ".format(self.name)
        for key in sorted(self.distance):
            distance = self.distance[key]
            next = self.next[key]
            response += "{}: {}, {};\t".format(
                key,
                "∞" if distance == float('inf') else distance,
                "∅" if next is None else next)
        response += "]"
        return response


class Graph(object):
    """
    Reprentación del Grafo.

    El API del grafo con que se inicializa tiene que ser la siguiente:
    iter(graph) itera sobre cada nodo del grafo
    iter(graph[u]) itera sobre cada vecino del nodo u
    graph[u][v] entrega la distancia entre el nodo u y v
    """
    def __init__(self, graph):
        self.graph = graph
        self.nodes = {}
        for node in self.graph:
            self.nodes[node] = Node(node)
            for other in self.graph:
                self.nodes[node].distance[other] = float('inf')
                self.nodes[node].next[other] = None
            self.nodes[node].distance[self.nodes[node].name] = 0

    def measure(self, node, neighbour, obj):
        """
        Mide la distancia entre nodo y su vecino y
        la almacena en la representación del nodo
        """
        new_distance = obj.distance[node] + self.graph[node][neighbour]
        if obj.distance[neighbour] > new_distance:
            obj.distance[neighbour] = new_distance
            obj.next[neighbour] = node if node != obj.name else None

    def step(self):
        """
        Itera sobre todos los nodos del grafo y hace un
        intercambio de mediciones entre los nodos una vez
        """
        for node in self.nodes:
            for u in self.graph:
                for v in self.graph[u]:
                    self.measure(u, v, self.nodes[node])

    def node_string(self):
        """
        Devuelve una cadena con la representación en pantalla
        de cada nodo. Se usa para comparar.
        """
        response = ""
        for node in sorted(self.nodes):
            response += self.nodes[node].to_string() + "\n"
        return response

    def break_link(self, one, two):
        if one in self.graph:
            if two in self.graph[one]:
                del self.graph[one][two]
        if two in self.graph:
            if one in self.graph[two]:
                del self.graph[two][one]
        if one in self.nodes:
            if two in self.nodes[one].distance:
                self.nodes[one].distance[two] = float('inf')
                self.nodes[one].next[two] = None
        if two in self.nodes:
            if one in self.nodes[two].distance:
                self.nodes[two].distance[one] = float('inf')
                self.nodes[two].next[one] = None
        for node in self.nodes:
            if self.nodes[node].next[one] == two:
                self.nodes[node].distance[one] = float('inf')
                self.nodes[node].next[one] = None
            elif self.nodes[node].next[two] == one:
                self.nodes[node].distance[two] = float('inf')
                self.nodes[node].next[two] = None

if __name__ == "__main__":
    graph = {
        'A': {'B': 1, 'G': 4, 'I': 10},
        'B': {'A': 1, 'C': 9, 'E': 8},
        'C': {'B': 9, 'D': 2},
        'D': {'C': 2, 'E': 9, 'F': 4, 'I': 2},
        'E': {'B': 8, 'D': 9, 'F': 2, 'I': 1},
        'F': {'D': 4, 'E': 2, 'H': 6},
        'G': {'A': 4, 'H': 7},
        'H': {'F': 6, 'G': 7, 'I': 3},
        'I': {'A': 10, 'D': 2, 'E': 1, 'H': 3},
    }

    g = Graph(graph)

    print "Estado Inicial"
    last = g.node_string()
    print last
    print "Comenzando Enrutamiento..."
    breaking = False
    i = 0
    while True:
        g.step()
        now = g.node_string()
        if last == now:
            if not breaking:
                print "Primera convergencia"
                g.break_link('H', 'I')
                now = g.node_string()
                print "Nos acaban de informar que un transatlántico cortó el enlace H-I, recalculando..."
                breaking = True
            else:
                break
        last = now
        print last
    print "Convergencia final"