#!/usr/bin/python
# -*- coding: utf-8 -*-


class Node(object):
    def __init__(self, name):
        self.distance = {}
        self.next = {}
        self.name = name


class Graph(object):
    def __init__(self, graph):
        self.graph = graph
        self.nodes = {}
        for node in self.graph:
            self.nodes[node] = Node(node)
            for other in self.graph:
                self.nodes[node].distance[other] = float('inf')
                self.nodes[node].next[other] = None
            self.nodes[node].distance[self.nodes[node].name] = 0

    def relax(self, node, neighbour, obj):
        new_distance = obj.distance[node] + self.graph[node][neighbour]
        if obj.distance[neighbour] > new_distance:
            obj.distance[neighbour] = new_distance
            obj.next[neighbour] = node if node != obj.name else None

    def step(self):
        for node in self.nodes:
            for u in self.graph:
                for v in self.graph[u]:
                    self.relax(u, v, self.nodes[node])

    def node_string(self):
        response = ""
        for node in self.nodes:
            response += "Nodo {}:[ ".format(node)
            for key in self.graph:
                distance = self.nodes[node].distance[key]
                next = self.nodes[node].next[key]
                response += "{}: {}, {};\t".format(
                    key,
                    "∞" if distance == float('inf') else distance,
                    "∅" if next is None else next)
            response += "]\n"
        return response

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
    for i in range(len(g.graph)-1):
        g.step()
        if last == g.node_string():
            print "Convergencia completa"
            exit()
        else:
            last = g.node_string()
        print "Paso", i+1
        print last
