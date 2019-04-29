import random
import numpy as np
import time

class NodeList:
    def __init__(self, name, val = None):
        self.name = name
        self.val = val
        self.next = None

class SLinkedList:
    def __init__(self):
        self.head = None

    def add(self, name, item = None):
        current = self.head
        if current == None:
            self.head = NodeList(name,item)
        else:
            while current.next != None:
                current = current.next
            current.next = NodeList(name, item)
    
    def print_list(self):
        printval = self.head.next
        while printval:
            print(printval.name + " " + str(printval.val))
            printval = printval.next
            
    def find_min(self, tab):
        current = self.head.next
        minimum = 100000000000
        v = current.name
        while current != None:
            if current.val < minimum and current.name not in tab:
                minimum = current.val
                v = current.name
            current = current.next
        return v
    
    def finding(self, item):
        first = self.head
        while True:
            if item == first.name:
                return first
            else:
                if first.next == None:
                    return False
                else:
                    first = first.next
    
class Incidence_list:
    def __init__(self):
        self.vertices = {}
        
    def add_vertex(self, v):
        temp = SLinkedList()
        temp.add(v)
        self.vertices[v] = temp
    
    def add_edge(self, u, v, nmb):
        if u in self.vertices and v in self.vertices:
            self.vertices[u].add(v,nmb)
            self.vertices[v].add(u,nmb)
            
            
    def print_graph(self):
        for key in sorted(list(self.vertices.keys())):
            print("klucz: ", key)
            self.vertices[key].print_list()
 
    def prim(self):
        self.mst = {}
        ans = []
        v_list = sorted(list(self.vertices.keys()))
        el = v_list[0]
        tab = [el]
        while len(self.mst) < len(self.vertices) - 1:
            link = self.vertices[el].find_min(tab)
            self.mst[el] = link
            tab.append(link)
            el = link  
        for i in self.mst.keys():
            ans.append((i, self.mst[i]))
        return ans
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
            self.edges[self.edge_indices[v]][self.edge_indices[u]] = weight
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
            
    def prim(self):
        ans = []
        start = 0
        el = self.edges[start]
        visited = []
        visited.append(start)
        while len(ans) < len(self.edges) - 1:
            link = find_min(el, visited)
            idx = link[1]
            ans.append((start, idx))
            visited.append(link[0])
            el = self.edges[idx]  
            start = idx
        return ans
        
def find_min(lst, tab):
    minimum = 100000
    for j in range(len(lst)):
        if 0<lst[j]<minimum and lst[j] not in tab:
            minimum = lst[j]
            idx = j
    return minimum, idx

def create_dag(n, c):
    #n - liczba wierzcholkow
    #c - nasycenie
    g = Graph()
    edges = []
    choose = [] #lista wierzcholkow
    for i in range(n):
        g.add_vertex(Vertex(str(i)))
        choose.append(i)
    c = int((n*(n-1)/2)*c)
    created_edges = 0
    while created_edges < c:
        if len(choose) == 0: #gdy lista sie konczy, jest odnawiana
            for i in range(n):
                choose.append(i)
        x = (random.choice(choose)) #wybor losowego wierzcholka z listy, kazdy bedzie wybrany min 1 raz
        choose.remove(x) #usuniecie uzytego z listy, aby dac innym szanse
        y = str(random.randrange(x, n))
        x = str(x)
        nmb = random.randrange(1000)
        if not x == y and not (x,y) in edges:
            g.add_edge(x,y, nmb)
            edges.append((x,y))
            created_edges += 1
    return g
         
def create_list(g):
    l = Incidence_list()
    for k in range(len(g.edges)):
        l.add_vertex(str(k))
    for i in range(len(g.edges)):
        for j in range(len(g.edges)):
             if g.edges[i][j] != 0 and l.vertices[list(l.vertices.keys())[i]].finding(str(j)) == False:
                 l.add_edge(str(i),str(j), g.edges[i][j])
    return l
 
           
start_int = 10
nmb_of_tries = 3
list_time1 = np.array([0.0]*15)
matrix_time1 = np.array([0.0]*15)
list_time2 = np.array([0.0]*15)
matrix_time2 = np.array([0.0]*15) 

for j in range(nmb_of_tries):
    nmb = start_int
    for i in range(15):
        g = create_dag(nmb, 0.3)
        l = create_list(g)
        
        start = time.time()
        g.prim()
        stop = time.time()
        matrix_time1[i]+= stop-start
        
        start = time.time()
        l.prim()
        stop = time.time()
        list_time1[i] += stop-start
        
        b = create_dag(nmb, 0.7)
        m = create_list(b)
        
        start = time.time()
        b.prim()
        stop = time.time()
        matrix_time2[i]+= stop-start
        
        start = time.time()
        m.prim()
        stop = time.time()
        list_time2[i] += stop - start
        
        nmb+=10

list_time1/=nmb_of_tries
matrix_time1/=nmb_of_tries
list_time2/=nmb_of_tries
list_time2/= nmb_of_tries

print(list(list_time1))      
print(list(matrix_time1))
print(list(list_time2))
print(list(matrix_time2))

