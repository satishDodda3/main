import math
import sys

def cross_product(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

def is_convex(polygon):
    n = len(polygon)
    if n < 3:
        return False 
    direction = 0
    for i in range(n):
        cross = cross_product(polygon[i], polygon[(i + 1) % n], polygon[(i + 2) % n])
        if cross != 0:
            if direction == 0:
                direction = 1 if cross > 0 else -1 
            elif (cross > 0 and direction < 0) or (cross < 0 and direction > 0):
                return False        
    return True

def distance(v1, v2):
    return math.sqrt((v1[0] - v2[0])**2 + (v1[1] - v2[1])**2)

def q(i, k, j, vertices):
    return distance(vertices[i], vertices[k]) + distance(vertices[k], vertices[j]) + distance(vertices[j], vertices[i])

def minimum_cost_triangulation(vertices):
    if not is_convex(vertices):
        return None, None, None

    n = len(vertices)
    V = [[float('inf')] * n for _ in range(n)]  
    split = [[None] * n for _ in range(n)]     

    for i in range(n):
        V[i][i] = 0  
        if i + 1 < n:
            V[i][i + 1] = 0  

    for gap in range(2, n):  
        for i in range(n - gap):
            j = i + gap
            
            for k in range(i + 1, j):
               
                cost = q(i, k, j, vertices) + V[i][k] + V[k][j]
                if cost < V[i][j]:
                    V[i][j] = cost
                    split[i][j] = k  

    def construct_triangulation(i, j):
        if j <= i + 1:
            return []
        k = split[i][j]
        return [(i, k, j)] + construct_triangulation(i, k) + construct_triangulation(k, j)

    min_cost = V[0][n - 1]
    triangulation = construct_triangulation(0, n - 1)
    
    edges = set()
    for (i, k, j) in triangulation:
        edges.add((i, k))
        edges.add((k, j))
        edges.add((i, j))

    boundary_edges = {(i, (i + 1) % n) for i in range(n)}
    triangulation_edges = {edge for edge in edges if edge not in boundary_edges and (edge[1], edge[0]) not in boundary_edges}
    all_edges = triangulation_edges.union(boundary_edges) 
    min_cost = sum(distance(vertices[start], vertices[end]) for start, end in all_edges)
    
    triangulation_edge_coords = [((vertices[start], vertices[end])) for start, end in triangulation_edges]
    return min_cost, triangulation_edge_coords, len(triangulation_edges)

def printOuput(min_cost,triangulation_edges,edge_count,n):
    if min_cost is not None:
            print(f'**Polygon no.{n} is convex.')
            print(f"{edge_count} chords: (xi, yi)-(xj, yj)")
            print(f'Optimal Triangulation: minimum weight = {round(min_cost, 6)}')
            for edge in triangulation_edges:
                print(f"({round(edge[0][0], 6)}, {round(edge[0][1], 6)}) - ({round(edge[1][0], 6)}, {round(edge[1][1], 6)})")
            print()
    else:
        print(f'**Polygon no.{n} is not convex.\n')
file = open(sys.argv[1])
vertex = []
n = 0
for line in file:

    if line.strip() and '--' not in line:
        vertex.append(tuple(map(float, line.split())))
    elif '--'  in line and vertex:
        n += 1
        min_cost, triangulation_edges, edge_count = minimum_cost_triangulation(vertex)
        printOuput(min_cost,triangulation_edges,edge_count,n)
        
        vertex.clear()
if vertex: 
    min_cost,triangulation_edges,edge_count=minimum_cost_triangulation(vertex)
    printOuput(min_cost,triangulation_edges,edge_count,n+1)
    vertex.clear()
        
    