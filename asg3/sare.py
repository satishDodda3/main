import sys
import time

class Graph:
    def __init__(self, num_nodes, edges=[]):
        self.num_nodes = num_nodes
        self.edges = edges

def read_file(file_path):
    print(f'Minimum Arborescences in {file_path}\n')
    f = open(file_path, 'r')
    line = f.readline()

    while line:
        line = line.strip()

        if line.startswith('**'):
            num_nodes = int(line.split('=')[1])
            g = Graph(num_nodes, [])
            val = line[3:].split(':')
            print(f"{val[0]}:\t{val[1].replace(' ','')} -----------------------")
            print('\tArborescence --')

        elif line.startswith('(u'):
            pass

        elif line.startswith('('):
            edge = line.replace('(', '').replace(')', '').replace('}', '').split(',')
            start, end, weight = int(edge[0]), int(edge[1]), float(edge[2])
            g.edges.append((start, end, weight))

        elif line.startswith('-'):
            start_time = time.time()
            arb = min_cost_arb(g)
            end_time = time.time()

            for i, edge in enumerate(sorted(arb)):
                print(f'\t\t{i+1}:\t({edge[0]}, {edge[1]}, {edge[2]:.5f})')

            print(f'\tTotal weight: {sum([i[2] for i in arb])} ({round((end_time - start_time) * 1000)} ms)')

        line = f.readline()

    f.close()
    print('Anuhya Yamparala')


def find_min_incoming_edges(graph, root=0):
    """
    Find the minimum incoming edge for each node.
    """

    min_weight = [float('inf')] * graph.num_nodes

    f_star = [None] * graph.num_nodes

    # Iterate through all edges to find the minimum incoming edge for each node.
    for u, v, weight in graph.edges:
        if v != root and (min_weight[v] > weight):
            min_weight[v] = weight
            f_star[v] = (u, v, weight)

    # Create a new graph with reduced weights
    new_edges = []

    for u, v, w in graph.edges:
        new_edges.append((u, v, w - min_weight[v]))

    reduced_graph = Graph(graph.num_nodes, new_edges)

    return reduced_graph, f_star

def find_cycles(f_star):
    """
    Find the first cycle in the graph induced by the minimum incoming edges.
    Returns the first cycle found as a list of nodes.
    The cycle should not have another cycle in it.
    """
    visited = [False] * len(f_star)
    
    # dfs like cycle detection
    for i in range(len(f_star)):

        # If the vertex is visited or has no incoming edge, skip it
        if visited[i] or f_star[i] is None:
            continue
        
        cycle = []
        current = i
        
        # Mark all nodes in this path as visited
        while not visited[current] and f_star[current] is not None:
            visited[current] = True
            cycle.append(current)
            incoming_edge = f_star[current]
            # Move to the next node
            current = incoming_edge[0]
            
        # Check if a cycle is found
        if current in cycle:
            cycle_start_index = cycle.index(current)
            return [cycle[cycle_start_index:]]  # Return the first cycle found
            
    # No cycle found
    return None

def contract_cycle(graph, cycle, f_star):
    """
    Contract a cycle into a single node and adjust the graph accordingly.
    """
    cycle_set = set(cycle)
    # New node to represent the contracted cycle
    cycle_index = graph.num_nodes
    
    # store the edges by transforming the cycle nodes to the new node
    new_edges = []
    cycle_edges = {}
    # store the old edges by transforming the cycle nodes to the new node
    old_edges = []

    # Iterate through the edges to contract the cycle
    for u, v, weight in graph.edges:
        if u in cycle_set and v in cycle_set:
            # This edge is within the cycle, we only keep the minimum weight edge between nodes
            if (u, v) not in cycle_edges or cycle_edges[(u, v)] > weight:
                cycle_edges[(u, v)] = weight
        else:
            # Contract nodes involved in the cycle into the cycle_index
            u_new = cycle_index if u in cycle_set else u
            
            v_new = cycle_index if v in cycle_set else v
            new_edges.append((u_new, v_new, weight))
            old_edges.append((u, v, weight))

    new_to_old_map = {new_edge: old_edge for new_edge, old_edge in zip(new_edges, old_edges)}

    # Return the new graph with the contracted cycle and the relevant edges
    return Graph(graph.num_nodes + 1, new_edges), cycle_edges, new_to_old_map


def min_cost_arb(g, root=0):
    
    reduced_graph, f_star = find_min_incoming_edges(g)

    # maps to be used to reconstruct the graph
    reduced_to_original_map = {reduced_edge: original_edge for reduced_edge, original_edge in zip(reduced_graph.edges, g.edges)}

    cycles = find_cycles(f_star)

    if cycles:
        contracted_graph, cycle_edges, contracted_to_old_map = contract_cycle(reduced_graph, cycles[0], f_star)

        arb = min_cost_arb(contracted_graph)
        
        # Restore original edges from the contracted arborescence
        arb = [reduced_to_original_map[contracted_to_old_map[edge]] for edge in arb if edge]
            
        # add cycle edges
        # nodes with incoming edge in arb
        visited_nodes = {v for _, v, _ in arb}

        # edges to add from all the cycle edges
        cycle_visited = {}

        for key in cycle_edges.keys():
            u, v, w = key[0], key[1], cycle_edges[key]

            # exclude edges that already has incoming edge in the contracted graph
            if v not in visited_nodes:
                # if any cycle node is visited, then dont add it, add it only if the weight is less than prev edge
                if v not in cycle_visited or w < cycle_visited[v][1]:
                    cycle_visited[v] = (u, w)

        for v in cycle_visited:
            old_edge = (cycle_visited[v][0], v, cycle_visited[v][1])
            arb.append(reduced_to_original_map[old_edge])

        return arb
    else:
        return [edge for edge in f_star if edge]

if __name__=='__main__':
    file_path = sys.argv[1]
    read_file(file_path)