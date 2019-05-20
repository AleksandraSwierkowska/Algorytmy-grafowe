import random
import numpy as np
import time

class Vertex:
    def __init__(self, n):
        self.name = n

class Graph:
    vertices = {}
    edges = []
    edge_indices = {}

    def add_vertex(self, vertex):
        if isinstance(vertex, Vertex) and vertex.name not in self.vertices:
            self.vertices[vertex.name] = vertex
            for row in self.edges:
                row.append(0)
            self.edges.append([0] * (len(self.edges) + 1))
            self.edge_indices[vertex.name] = len(self.edge_indices)
            return True
        else:
            return False

    def add_edge(self, u, v, weight=1):
        if u in self.vertices and v in self.vertices:
            self.edges[self.edge_indices[u]][self.edge_indices[v]] = weight
            self.edges[self.edge_indices[v]][self.edge_indices[u]] = weight
            # if there's an arc to a vertex we can be sure that there won't be one back since it's DAG
            return True
        else:
            return False

    def print_graph(self):
        for v, i in sorted(self.edge_indices.items()):
            #print(v + ' ')
            edges = []
            for j in range(len(self.edges)):
                edges.append(self.edges[i][j])
            print(edges)

    def _hamilton(self, out, start, v):
        for i in range(len(self.edges)):
            if len(out) == len(self.edges) + 1:
                break
            elif self.edges[v][i] != 0 and not (i in out):
                out.append(i)
                out = self._hamilton(out, start, i)
        out.pop()
        return out

    def hamilton(self, v):
        out = [v]
        start = v
        return self._hamilton(out, start, v)

def create_euler(n, c):
    # n - liczba wierzcholkow
    # c - nasycenie
    g = Graph()
    edges = []
    for i in range(n):
        g.add_vertex(Vertex(str(i)))
    vertex = list(range(n))
    random.shuffle(vertex)
    for i in range(n-1):
        g.add_edge(str(vertex[i]), str(vertex[i+1]))
    g.add_edge(str(vertex[-1]), str(vertex[0]))
    c = (n * (n - 1) / 2) * c
    created_edges = n-1
    while created_edges < c:
        x = random.randrange(n)
        y = random.randrange(n)
        z = random.randrange(n)
        if x!=y and y!=z and z!=x and g.edges[x][y]!=1 and g.edges[y][z]!=1 and g.edges[x][z]!=1:
            g.add_edge(str(x), str(y))
            g.add_edge(str(x), str(z))
            g.add_edge(str(y),str(z))
            created_edges += 3

    return g

g = create_euler(15, 0.5)
g.hamilton(0)

tries_number = 3
start_int = 5
hamilton = np.array([0.0] * 15)
for j in range(tries_number):
    nmb = start_int
    for i in range(10):
        g = create_euler(nmb, 0.5)
        start = time.time()
        g.hamilton(0)
        stop = time.time()
        hamilton[i] += stop - start
        nmb+=1

hamilton/=tries_number
print(list(hamilton))