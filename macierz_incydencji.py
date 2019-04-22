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
			self.edges.append([0] * (len(self.edges)+1))
			self.edge_indices[vertex.name] = len(self.edge_indices)
			return True
		else:
			return False
    
    def add_edge(self, u, v, weight=1):
		if u in self.vertices and v in self.vertices:
			self.edges[self.edge_indices[u]][self.edge_indices[v]] = weight
			self.edges[self.edge_indices[v]][self.edge_indices[u]] = -weight
			#if there's an arc to a vertex we can be sure that there won't be one back since it's DAG
			return True
		else:
			return False
			
    def print_graph(self):
		for v, i in sorted(self.edge_indices.items()):
			print(v + ' ')
			for j in range(len(self.edges)):
				print(self.edges[i][j])
			print(' ')    

def create_dag(n, c):
	#n - liczba wierzcholkow
	#c - nasycenie
	g = Graph()
	edges = []
	for i in range(n):
		g.add_vertex(Vertex(chr(97+i)))
	c = int((n*(n-1)/2)*c)
	created_edges = 0
	while created_edges < c:
		x = random.randrange(97, 97+n)
		y = random.randrange(x, 97+n)
		if not chr(x) == chr(y) and not (chr(x),chr(y)) in edges:
			g.add_edge(chr(x),chr(y))
			edges.append((chr(x),chr(y)))
			created_edges += 1
	print(edges)
	g.print_graph()
	return g


create_dag(5,0.6)
#np dla n = 5 i c = 0.6
