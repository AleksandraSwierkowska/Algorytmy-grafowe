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

    def euler(self, v):
        v = int(v)
        vert = []
        length = len(self.edges)
        for i in range(length):
            if self.edges[v][i] == 1:
                self.edges[v][i] = -1
                self.edges[i][v] = -1
                self._euler(i, vert)
        vert.append(v)
        return vert

    def _euler(self, v, vert):
        length = len(self.edges)
        for i in range(length):
            if self.edges[v][i] == 1:
                self.edges[v][i] = -1
                self.edges[i][v] = -1
                self._euler(i, vert)
        vert.append(v)

    def _hamilton(self, out, start, v):
        for i in range(len(self.edges)):
            if len(out) == len(self.edges) + 1:
                break
            elif self.edges[v][i] != 0 and not (i in out):
                out.append(i)
                out = self._hamilton(out, start, i)
        print(v)
        print(out)
        if len(out) >= len(self.edges):
            print("wie:" +str(v))
            if len(out) == len(self.edges) and self.edges[v][start] == 1:
                print(str(v)+' '+str(start))
                out.append(start)
        else:
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

tries_number = 3
start_int = 30
euler30 = np.array([0.0] * 15)
euler70 = np.array([0.0] * 15)
hamilton30 = np.array([0.0] * 15)
hamilton70 = np.array([0.0] * 15)

for j in range(tries_number):
    nmb = start_int
    for i in range(15):
        g30 = create_euler(nmb, 0.3)
        g70 = create_euler(nmb, 0.7)
        
        start = time.time()
        g30.euler('0')
        stop = time.time()
        euler30[i] += stop - start
        
        start = time.time()
        g30.hamilton(0)
        stop = time.time()
        hamilton30[i] += stop - start
        
        start = time.time()
        g70.euler('0')
        stop = time.time()
        euler70[i] += stop - start
        
        start = time.time()
        g70.hamilton(0)
        stop = time.time()
        hamilton70[i] += stop - start
        nmb += 20
        
euler70/=tries_number
euler30/=tries_number
hamilton70/=tries_number
hamilton30/=tries_number

print(list(euler30))
print(list(hamilton30))
print(list(euler70))
print(list(hamilton70))