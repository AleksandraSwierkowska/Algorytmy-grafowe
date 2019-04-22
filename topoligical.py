import random
class NodeList:
    def __init__(self, name):
        self.name = name
        self.next = None

class SLinkedList:
    def __init__(self):
        self.head = None

    def add(self, name):
        current = self.head
        if current == None:
            self.head = NodeList(name)
        else:
            while current.next != None:
                current = current.next
            current.next = NodeList(name)
    
    def print_list(self):
        printval = self.head.next
        while printval:
            print(printval.name + " " + str(printval.val))
            printval = printval.next
                
class Incidence_list:
    def __init__(self):
        self.vertices = {}
        
    def add_vertex(self, v):
        temp = SLinkedList()
        temp.add(v)
        self.vertices[v] = temp
    
    def add_edge(self, u, v):
        if u in self.vertices and v in self.vertices:
            self.vertices[u].add(v)
            self.vertices[v].add(u)
            
    def add_directed_edge(self, u, v):
        if u in self.vertices and v in self.vertices:
            self.vertices[u].add(v)
            
    def print_graph(self):
        for key in sorted(list(self.vertices.keys())):
            print("klucz: ", key)
            self.vertices[key].print_list()

    def topological_sort(self):
        key = list(self.vertices.keys())
        visited = [False] * len(key)
        stack = []
        
        for i in range(len(key)):
            if visited[i] == False:
                self._topological_sort(i, visited, stack)
                
        return stack
                
    def _topological_sort(self, v, visited, stack):
        key = list(self.vertices.keys())
        visited[v] = True
        current = self.vertices[key[v]].head
        while current.next != None:
            current = current.next
            idx = key.index(current.name)
            if visited[idx] == False:
                self._topological_sort(idx, visited, stack)
        stack.insert(0,key[v]) 
        
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
        g.add_vertex(Vertex(str(i)))
    c = int((n*(n-1)/2)*c)
    created_edges = 0
    while created_edges < c:
        x = str(random.randrange(n))
        y = str(random.randrange(int(x), n))
        if not x == y and not (x,y) in edges:
            g.add_edge(x,y)
            edges.append((x,y))
            created_edges += 1
    print(edges)
    g.print_graph()
    return g

def create_list(g):
    print(g.edges)
    
g =create_dag(8,0.6)
   
create_list(g)     


"""
g = Incidence_list()
for i in range(20):
    g.add_vertex(str(i))
    
rand = list(range(20))
random.shuffle(rand)

for i in range(19):
    g.add_edge(str(rand[i]), str(rand[i+1]))
g.add_edge('1', '8')
g.add_edge('2', '13')
g.add_edge('2', '19')
g.add_edge('13', '15')

print(g.topological_sort())
"""
