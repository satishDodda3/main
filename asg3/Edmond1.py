import sys
file=open(sys.argv[1])
test_map={}


def find_min_indegree(edge,weight,min_indegree):
    for i in edge:
        if i[1] not in min_indegree:
            min_indegree[i[1]]=[i[0],weight[(i[0],i[1])]]
        elif i[1] in min_indegree and min_indegree[i[1]][1]>weight[(i[0],i[1])]:
            min_indegree[i[1]]=[i[0],weight[(i[0],i[1])]]

    for i in range(len(edge)):
        edge=list(edge)
        if edge[i][1] in min_indegree:
            weight[(edge[i][0],edge[i][1])]-=min_indegree[edge[i][1]][1]

def expand_graph(graph,c_node,track,min_indegree,cycle):
    c_e=None 
    for i, j in graph:
        if j==c_node:
            
            o_v=track[(i,j)][1]
            c_e=(min_indegree[o_v][0],o_v)
            break

    expand=set([track[(i,j)] for i, j in graph])
    for v in cycle:
        k=min_indegree[v][0]
        if c_e[0]!=k and c_e[1]!=v:
            expand.add((k,v))
    return expand 


def detect_cycle(vertex, min_indegree):
    cycle=[]
    n=None
    for i in vertex: 
        if i==0:
            continue
        visited=set()
        n=i
        while n!=0 and  n not in visited and n in min_indegree:
            visited.add(n)
            n=min_indegree[n][0]

        if n!=0 and n in visited: 
            cycle=[]
            while n not in cycle: 
                cycle.append(n)
                n=min_indegree[n][0]
            break
    return (cycle,n)

def find_arboresence(edge,vertex,weight):

    min_indegree={}
    find_min_indegree(edge,weight,min_indegree)
    


    cycle,n=detect_cycle(vertex,min_indegree)
    
    if not cycle: 
        return [(min_indegree[i][0],i) for i in min_indegree.keys()]
    
  

    c_node='s'+str(n)

    no_cycle_vertix=list([i for i in vertex if i not in cycle])
    no_cycle_vertix.append(c_node)
    no_cycle_edge=set()
    no_cycle_weight={}
    track={}

    def update(i,j, e):
        no_cycle_weight[e]=weight[(i,j)]
        track[e]=(i,j)
        no_cycle_edge.add(e)

    for i,j in edge: 
        if i not in cycle and j in cycle:
            edge=(i,c_node)
            if edge in no_cycle_edge and no_cycle_weight[edge]<weight[(i,j)]:
                continue
            update(i,j,edge)

        elif i in cycle and j not in cycle: 
            edge=(c_node,j)
            if edge in no_cycle_edge and no_cycle_weight[edge]<weight[(i,j)]:
                continue
            update(i,j,edge)
            
        elif i not in cycle and j not in cycle:
            edge=(i,j)
            update(i,j,edge)
    
    graph=find_arboresence(no_cycle_edge,no_cycle_vertix,no_cycle_weight)
   
    return expand_graph(graph,c_node,track,min_indegree,cycle)
    


    
    

c=0
edge=set()
totalVertex=0
vertex=set()
graph=1

#reading the data from the file 
print(f"Minimum Arboresence in {sys.argv[1]}\n")
for i in file:
    #if encounter ** in line then , taking total vertex number from line
    if '**' in i:
        k=i.split('=')[1]
        totalVertex=int(k[0::])
    #if E and { is encounterd then it means edge tuple is started so updating c with 1 
    elif 'E' in i and '{' in i: 
        c=1 
    #if '--' and '=' not in line that means those are tuple of edges and weights processing it and updating the adjList 
    elif c and '--' not in i and '=' not in i:
        if '}' in i:
            i=i[0:i.index('}')]
        e=list(eval(i))
       
        edge.add((e[0],e[1]))
        vertex.add(e[0])
        vertex.add(e[1])
        test_map[(e[0],e[1])]=e[2]

    #if '--' is encounterd in line that means end of graph 
    elif '--' in i:
        weight=test_map.copy()
        c=0
        print(f"G{graph}: |V|= {totalVertex} -------------------------")
        print("   Arborescence --")

        res=find_arboresence(edge,vertex,test_map)
        res=list(res)
        l=[]
        for i in range(len(res)):
            l.append([res[i][0],res[i][1],weight[res[i]]])
        l.sort()
        
        total=0
        for i in range(len(l)):
            print(f'{i+1}: {(l[i][0],l[i][1],l[i][2])}')
            total+=weight[res[i]]
        print(f'Total weight: {total} (0 ms)\n')
        
        
        graph+=1 
        edge.clear()
        vertex.clear()
        test_map.clear()
       

