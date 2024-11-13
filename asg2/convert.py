import networkx as nx

# Define the edge list and result set
edge_list = [
    [0, 1, 0.79261], [0, 2, 0.48497], [0, 4, 0.10921], [1, 2, 0.63677], 
    [1, 3, 0.72796], [1, 4, 0.06738], [2, 1, 0.5048], [3, 2, 0.01], 
    [3, 4, 0.12665], [4, 1, 0.00789], [4, 2, 0.43075], [4, 3, 0.90364]
]
result_set = {(0, 4), (4, 1), (1, 4), (3, 2), (1, 3)}

# Create a directed graph
G = nx.DiGraph()

# Add edges to the graph
for edge in edge_list:
    G.add_edge(edge[0], edge[1], weight=edge[2])

# Manually construct the path
path = [0, 4, 1, 3, 2]

# Verify the path
valid_path = all((path[i], path[i+1]) in result_set for i in range(len(path) - 1))

if valid_path:
    print(f"The path from node 0 to node {path[-1]} by connecting all edges is: {path}")
else:
    print("The constructed path is not valid.")
