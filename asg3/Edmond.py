#Name: Satish Dodda
#uild: 809961786
#pledge: This entire code was written by Satish Dodda 
#copyright: 2024 satish Dodda, unauthorized copying or modifying of this code is not allowed
import time

import sys
file=open(sys.argv[1])

# Satish dodda ,7-oct-2024, started at 10am and finished 10:20 am
# @min_indegree map it will store the min_indegree values for every vertix expect root 
# @edge is a list it will store  list of edges
# @weight is a map which will store the weights of the edge 
#find_indegree method  finds the min_indegree for every vertex in the edge list ,except root 
def find_Indegree(min_indegree,edge,weight):
    #finding the min_indegree values for every vertix 
    for i in edge:
        if i[1]!=0 and i[1] not in min_indegree:
            min_indegree[i[1]]=i.copy()
          
        elif min_indegree[i[1]][2]>i[2]:
            min_indegree[i[1]]=i.copy()
#after identifying the minimum incoming edge for each vertex, subtract the weight of the minimum incoming edge from every other incoming edge to that vertex 
    for i in range(len(edge)):
        if edge[i][1] in min_indegree:
            edge[i][2]-=min_indegree[edge[i][1]][2]
            weight[(edge[i][0],edge[i][1])]-=min_indegree[edge[i][1]][2]

    return min_indegree

#Satish dodda ,7-oct-2024, started at 10:30am and finished 11 am
# @min_indegree is map it will store the min_indegree weight for every vertix
# @vertex it is set which will store the set of vertex
# is_cycle method  find cycle if any cycle is found in min_indegree map 

def is_cycle(min_indegree,vertex):
    #checking for cycle in min_indegree map if cylce present then storing it into cycle list 
    cycle=[]
    n=None
    for i in vertex: 
        if i==0:
            continue
        visited=set()
        n=i
        #checking for the cylce in min_indegree map 
        while n!=0 and  n not in visited and n in min_indegree:
            visited.add(n)
            n=min_indegree[n][0]
        #if cycle present in min_indegree map then storing the vertex's of cycle in in cycle list 
        if n!=0 and n in visited: 
            cycle=[]
            while n not in cycle: 
                cycle.append(n)
                n=min_indegree[n][0]
            break
    return cycle
#Satish dodda ,7-oct-2024, started at 10am and finished 5 pm
# @ edge is a list which contains list of edges 
# @ vertex is a set which contains set of vertex
# @ weight is map which contains weight of edge
# @ count is a number to uniquely name the cycles 
#find_arboresence method will accept edge, vertex, weight as pararamter and will return the minimum cost arboresence 
def find_arboresence(edge,vertex,weight,count):
    #min_indegree map to store the min_indegree values for each vertex 
    min_indegree={}
    #calling find_Indegree 
    find_Indegree(min_indegree,edge,weight)
    #calling is_cycle method and storing it into cycle 
    cycle=is_cycle(min_indegree,vertex)

        
    # if not cycle is present then returning the min_indegree values 
    if not cycle:return list(min_indegree.values())
   
    track={} 
    # removing all cycle vertex's for the vertex list 
    non_cycle_vertex=set(i for i in vertex if i not in cycle )
    #naming the cycle with s+cycle number 
    super_node='s'+str(count)
    #adding super_Node to non_cycle_vertex list 
    non_cycle_vertex.add(super_node)
    new_weight={}

   
    c=cycle
    edge1=[]    



    for i in range(len(edge)):
        # if edge[i][0] in cycle and edge[i][1] not in cycle 
        if edge[i][0] in c and edge[i][1] not in c: 
            #replacing the edge[i][0] vertex with cycle_node 
            e=(super_node,edge[i][1])
             #if more than one edge is from  supernode to somevertix then storing the minimum weighted edge only 
            if e in new_weight and new_weight[e]<weight[(edge[i][0],edge[i][1])]:
                continue
            h=edge[i].copy()
            #track map is used to track the original values of edge[i][0] and edge[i][1]
            track[e]=(h[0],h[1])
            new_weight[e]=weight[(h[0],h[1])]
            h[0]=super_node
            #adding the edge to new edge list 
            edge1.append(h)
                
        elif edge[i][0] not in c and edge[i][1]  in c: 
            e=(edge[i][0],super_node)
            if e in new_weight and new_weight[e]<weight[(edge[i][0],edge[i][1])]:
                continue
            h=edge[i].copy()
            track[e]=(h[0],h[1])
            new_weight[e]=weight[(h[0],h[1])]
            h[1]=super_node
            edge1.append(h)
        # if edge[i][0] and edge[i][1] is not in cycle 
        elif edge[i][0] not in c and edge[i][1] not in c:
            e=(edge[i][0],edge[i][1])
            h=edge[i].copy()
            track[e]=(h[0],h[1])
            new_weight[e]=weight[(h[0],h[1])]
            edge1.append(h)
        
    #calling the recursive function 
    graph=find_arboresence(edge1,non_cycle_vertex ,new_weight,count+1)
    #expanding the graph 

    c=None
    for i in  graph:
        #finding the cycle forming edge 
        if i[1]==super_node:
           h= track[(i[0],i[1])][1]
           c=(min_indegree[h][0],h)
           break
    #extracting the original values from the graph using track map 
    expand=[list(track[(i[0],i[1])])for i in graph]
    #removing the cycle edge and adding non cycle edges to the expand list and returning it 
    for v in cycle:
        k=min_indegree[v][0]
        if c[0]==k and c[1]==v:
            continue
        expand.append([k,v])
    return expand
     

c=0
edge=[]
totalVertex=0
vertex=set()
get_edgeNumber={}
weight={}

#reading the data from the file 
edge_number=1
print(f"Minimum Arboresence in {sys.argv[1]}\n")
graph=1
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
        # get_edgeNumber[edge_number]=(e[0],e[1])
       
        edge.append(e)
        vertex.add(e[0])
        vertex.add(e[1])
        weight[(e[0],e[1])]=float(e[2])
        edge_number+=1 
    #if '--' is encounterd in line that means end of graph 
    elif '--' in i:
        c=0
        weight1=weight.copy()

        print(f"G{graph}: |V|= {totalVertex} -------------------------")
        print("   Arborescence --")
        s=time.time()
        res=find_arboresence(edge,vertex,weight,1)
        e=time.time()
        res.sort()
        total=0
        for i in range(len(res)):
            print(f'{i+1}: {(res[i][0],res[i][1],round(weight1[(res[i][0],res[i][1])],5))}')
            total+=weight1[(res[i][0],res[i][1])]
        print(f'Total weight: {total} ({(round((e-s)*1000))} ms)\n')
   
        edge_number=1
        
        edge.clear()
        vertex.clear()
        # get_edgeNumber.clear()
        weight.clear()
        graph+=1
print("Satish Dodda")
