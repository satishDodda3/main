# # Re-defining the msa_adjusted function and rerunning the adjusted input as requested.

def msa_adjusted(V, E, r, w):
    """
    Recursive Edmond's algorithm adjusted for string-based vertices.
    Returns a set of all the edges of the minimum spanning arborescence.
    V := set( Vertex(v) )
    E := set( Edge(u,v) )
    r := Root(v)
    w := dict( Edge(u,v) : cost)
    """

    """
    Step 1 : Removing all edges that lead back to the root
    """
    for (u,v) in E.copy():
        if v == r:
            E.remove((u,v))
            w.pop((u,v))

    """
    Step 2 : Finding the minimum incoming edge for every vertex.
    """
    pi = dict()
    for v in V:
        edges = [edge[0] for edge in E if edge[1] == v]
        if not len(edges):
            continue
        costs = [w[(u,v)] for u in edges]
        pi[v] = edges[costs.index(min(costs))]
    
    
    """
    Step 3 : Finding cycles in the graph
    """
    # print(V)
    cycle_vertex = None
    for v in V:
        if cycle_vertex is not None:
            break
        visited = set()
        next_v = pi.get(v)
        while next_v:
            if next_v in visited:
                cycle_vertex = next_v
                break
            visited.add(next_v)
            next_v = pi.get(next_v)
    """
    Step 4 : If there is no cycle, return all the minimum edges pi(v)
    """
    if cycle_vertex is None:
        return set([(pi[v],v) for v in pi.keys()])
    
    """
    Step 5 : Otherwise, all the vertices in the cycle must be identified
    """
    C = set()
    C.add(cycle_vertex)
    next_v = pi.get(cycle_vertex)
    while next_v != cycle_vertex:
        C.add(next_v)
        next_v = pi.get(next_v)
    # print(C)
    """
    Step 6 : Contracting the cycle C into a new node v_c (string-based ID to avoid conflicts)
    """
    v_c = 'cycle_' + cycle_vertex
    V_prime = set([v for v in V if v not in C] + [v_c])
    print(V_prime)
    E_prime = set()
    w_prime = dict()
    correspondance = dict()
    for (u,v) in E:
        if u not in C and v in C:
            e = (u,v_c)
            if e in E_prime:
                if w_prime[e] < w[(u,v)] - w[(pi[v],v)]:
                    continue
            w_prime[e] = w[(u,v)] - w[(pi[v],v)]
            correspondance[e] = (u,v)
            E_prime.add(e)
            
        elif u in C and v not in C:
            e = (v_c,v)
           
            if e in E_prime:
                old_u = correspondance[e][0]
                if w[(old_u,v)] < w[(u,v)]:
                    continue
            E_prime.add(e)
            w_prime[e] = w[(u,v)]
            correspondance[e] = (u,v)
        elif u not in C and v not in C:
            e = (u,v)
            E_prime.add(e)
            w_prime[e] = w[(u,v)]
            correspondance[e] = (u,v)
    
    # print(E_prime)
    print(w_prime)
    # print(correspondance)
    print()

    """
    Step 7 : Recursively calling the algorithm again until no cycles are found
    """
    tree = msa_adjusted(V_prime, E_prime, r, w_prime)
    """
    Step 8 : Find the cycle edge and finalize the result
    """
    # print(tree)
    cycle_edge = None
    for (u,v) in tree:
        if v == v_c:
            
            old_v = correspondance[(u,v_c)][1]
            
            cycle_edge = (pi[old_v],old_v)
            # print((u,v_c),correspondance[(u,v_c)],cycle_edge)
            break
    
    ret = set([correspondance[(u,v)] for (u,v) in tree])
    # print(C)
    for v in C:
        u = pi[v]
        ret.add((u,v))

    # print(ret,cycle_edge)

    ret.remove(cycle_edge)
    return ret

# # Re-running the input based on the provided graph data
V_passed = {'r', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i'}  # Vertex set
E_passed = {('r', 'a'), ('r', 'c'), ('a', 'c'), ('r', 'e'), ('c', 'e'), ('b', 'a'), 
           ('d', 'b'), ('c', 'd'), ('f', 'd'), ('f', 'e'), ('h', 'b'), ('h', 'd'),
           ('g', 'h'), ('d', 'g'), ('g', 'f'), ('h', 'i'), ('g', 'i'), ('f', 'i'), ('b', 'i')}  # Edge set
r_passed = 'r'  # Root node
w_passed = {('r', 'a'): 8, ('r', 'c'): 6, ('a', 'c'): 1, ('r', 'e'): 3, ('c', 'e'): 1, 
           ('b', 'a'): 2, ('d', 'b'): 2, ('c', 'd'): 5, ('f', 'd'): 3, ('f', 'e'): 2,
           ('h', 'b'): 5, ('h', 'd'): 2, ('g', 'h'): 8, ('d', 'g'): 6, ('g', 'f'): 6, 
           ('h', 'i'): 2, ('g', 'i'): 4, ('f', 'i'): 3, ('b', 'i'): 3}  # Weights for edges

# V_passed = {'0','1','2','3','4','5','6','7','8','9'}  # Vertex set
# E_passed = {('7', '6'), ('3', '9'), ('9', '1'), ('0', '3'), ('9', '7'), ('6', '4'), ('2', '7'), ('4', '6'), ('6', '3'), ('5', '3'), ('8', '2'), ('8', '5'), ('4', '9'), ('5', '2'), ('1', '4'), ('2', '4'), ('9', '4'), ('1', '3'), ('5', '8'), ('8', '6'), ('1', '2'), ('4', '7'), ('2', '3'), ('3', '4'), ('7', '4'), ('8', '9'), ('6', '9'), ('3', '2'), ('0', '1'), ('3', '5'), ('8', '1'), ('7', '2'), ('2', '8'), ('0', '7'), ('3', '8'), ('9', '6'), ('6', '1'), ('7', '8'), ('4', '3'), ('2', '6'), ('6', '7'), ('3', '6'), ('2', '9')}
# r_passed = '0'  # Root node
# w_passed = {('0', '1'): 0.85058, ('0', '3'): 0.95819, ('0', '7'): 0.34803, ('1', '2'): 0.33826, ('1', '3'): 0.71177, ('1', '4'): 0.55209, ('2', '3'): 0.85744, ('2', '4'): 0.79246, ('2', '6'): 0.91747, ('2', '7'): 0.49254, ('2', '8'): 0.10176, ('2', '9'): 0.91594, ('3', '2'): 0.30029, ('3', '4'): 0.52212, ('3', '5'): 0.59355, ('3', '6'): 0.20255, ('3', '8'): 0.0219, ('3', '9'): 0.43642, ('4', '3'): 0.34498, ('4', '6'): 0.17412, ('4', '7'): 0.01052, ('4', '9'): 0.63069, ('5', '2'): 0.43382, ('5', '3'): 0.89637, ('5', '8'): 0.35259, ('6', '1'): 0.16157, ('6', '3'): 0.41769, ('6', '4'): 0.42906, ('6', '7'): 0.64465, ('6', '9'): 0.41599, ('7', '2'): 0.55818, ('7', '4'): 0.361, ('7', '6'): 0.79847, ('7', '8'): 0.12842, ('8', '1'): 0.66204, ('8', '2'): 0.26611, ('8', '5'): 0.67824, ('8', '6'): 0.99243, ('8', '9'): 0.87777, ('9', '1'): 0.6507, ('9', '4'): 0.53703, ('9', '6'): 0.80471, ('9', '7'): 0.11021}
# # Running the algorithm on this input
msa_output_passed = msa_adjusted(V_passed, E_passed, r_passed, w_passed)
print(msa_output_passed)


