import random

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
            print(v + ' ')
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
                self._euler(i, vert)
        return vert

    def _euler(self, v, vert):
        length = len(self.edges)
        for i in range(length):
            if self.edges[v][i] == 1:
                self.edges[v][i] = -1
                self._euler(i, vert)
        vert.append(v)


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
        edges.append((str(vertex[i]), str(vertex[i+1])))

    c = (n * (n - 1) / 2) * c
    created_edges = n-1
    while created_edges < c:
        x = str(random.randrange(n))
        y = str(random.randrange(int(x), n))
        z = str(random.randrange(int(x), n))
        if not x == y == z and not (x, y) in edges and not (x,z) in edges:
            g.add_edge(x, y)
            g.add_edge(x, z)
            edges.append((x, y))
            edges.append((x,z))
            created_edges += 2
    return g

g = create_euler(10, 0.5)
#g.print_graph()
print(g.euler('0'))
