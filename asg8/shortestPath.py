#Name: Satish Dodda
#ULID: 809961786
#Pledge : This entire code was developed by my self 
#copyright: without authorization copying or modifying the code is not allowed

from collections import defaultdict,deque
#importing the sys package to handel the command line arguments 
import sys
#importing the heapq package for priority queue 
import heapq
#Accepting the file name as argument and opening the file 
import math
file=open(sys.argv[1])
print(f'Shortest Paths from vertex 0 to vertex n-1 in {sys.argv[1]}, |V|=n\n')

#Name: Satish Dodda 
#Date: 17-sep 2024
#Time: 2pm-5pm

# @shortestPath is a map, the key represents the starting vertex and value is the list of two items indicates the target vertex and second value indicates the min cost to visit  edge
# @adiList is a map , the key represents the vertex and value  is a tuple of three values edge and weight of the edge 
# @visited is a map , the key represent the vertex and value is either (0 or 1) if it is one then it is already visited , other wise not visited 
# @last_vertex ,which hold the value of last vertex 
def computeDijkstra(shortestPath,adjList,visited,last_vertex):
    #stack is a list to store the shortest path values from 0 to n-1 
    stack=[]
    #pq is the list to store the priority queue values 
    pq=[]
    # This is the edge case , if 0 is not in adiList than means is no edge from 0 that means no path 
    if 0 not in adjList:
        print('*** There is no path.\n')
        return ()
    
    #First i am placing the all edges from vertix 0 in priority queue 
    for i in adjList[0]:
        heapq.heappush(pq,i)
    #marking vertex 0 is visited 
    visited[0]=1
    
    #if pq list is not empty then it will enter into loop 
    while(len(pq)):
        # headpq. heappop() method will remove and return the top element from the priority queue
        top=heapq.heappop(pq)

        #taking the second element from the tuple and marking as visited ,example (10.34, 1,0 ) there is a edge from 0 to 1 with weight 10.34 so marking 1 as visited 
        visited[top[1]]=1
        #if element already present in shortestPath map and values is 0 ,not at visited that edge , adding the edge weight to the shortestPath map  
        if top[1] in shortestPath and shortestPath[top[1]][1]==0:
            shortestPath[top[1]]=[top[2],top[0]]
        # if vertex is present in adjList 
        if top[1] in adjList:
            # Then traversing through  all the adjacen vertices connected to the current vertex top[1]
            for i in adjList[top[1]]:
                 # if adjacent vertex i[1] is not visited 
                 if i[1] in visited and visited[i[1]]==0:
                    #updating the cost of to reach  vertex i[1] by adding the min cost to travel the vertex top[1] because there is edge between top[1] and i[1]
                    heapq.heappush(pq,(i[0]+shortestPath[i[-1]][-1],i[1],i[2]))
    # a flag to check weather vertex present in shortestPath or not 
    flag=1
    while(1):
        # if last_vertex is not in shortestPath that means there is not path between 0 to n-1
        if last_vertex not in shortestPath:
            flag=0
            print('     *** There is no path.\n')
            break
        #if last_vertex is 0 that means we have reach from n-1 to 0 and have a shortest path
        if last_vertex==0:
            break
        # if last_vertex is shortestpath we are pushing edge to stack to print 
        elif last_vertex in shortestPath:
            stack.append((last_vertex,*shortestPath[last_vertex]))
            # updating the last_vertex to get next edge from shortestPath
            last_vertex=shortestPath[last_vertex][0]

    #if flag is 1 then it will print the shortest path 
    if(flag):
        track=0
        for i in stack[::-1]:
            print(f"    ( {i[1]}, {i[0]}, {(i[-1]-track):.3f}) -->  {i[-1]:.3f}")
            track=i[-1]
        
        print()

#Name: Satish Dodda Date: 11-nov 2024 Time: 2pm-2:20pm
# update_dp_table method will check weather the current weight of  v is greather than weight  u+(u,v) if greater then
# we will check for any negative cycle in the graph by calling detect_negative_cycle method , if any negative cycle is found then it will print the negative cycle and stops the program , 
# other wise  we will update weight of v with u+weight(u,v)               
# @ weight it will store the weights of the edges 
# @ track is a map it will store the min in comming vertex u for every v 
# @ edges is the list which contains list of edges (u,v)
# @ weight_by_edges is a dict which will store key as (u,v) and values as weight associate with edge (u,v)
# @ total_vertices is the total count of unique vertices in the graph 

def update_dp_table(weight,track,edges,weight_by_edges,total_vertices):
    i=0
    while i<total_vertices-1:
        for u, v in edges:
            if weight[u] != math.inf and weight[u] +weight_by_edges[(u,v)]  < weight[v]:
                if detect_negative_cycle(edge_weight,v,track,total_vertices):
                    return True
                weight[v] ,track[v] = weight[u] + weight_by_edges[(u,v)],u
        i+=1

#Name: Satish Dodda Date: 11-nov 2024 Time: 2:40pm-2:50pm 
#getCycleVertexs method will detect the cycle if any cycle is found it will store cycle vertices in cycle list 
# @ cycle is a list is to store the list of cycle vertices 
# @ current is the varible which contains starting node to find the cycle 
# @ track is a map it will store the min in comming vertex u for every v 

def getCycleVertexs(cycle,current,track):
    dq=deque()
    cycle_start = current
    while current != cycle_start or not dq: 
        dq.appendleft(current)
        current = track[current]
    dq.appendleft(cycle_start)
    if None in dq:
        dq.clear()
    cycle.extend(dq)
    
#Name: Satish Dodda Date: 11-nov 2024 Time: 2:20pm-2:40pm 
# @ detect_negative_cycle method will check for negative cycle in the graph if it found any negative cycle in the graph will print the negative cycle edges and break the program
# @ track is a map it will store the min in comming vertex u for every v 
# @ weight_by_edges is a dict which will store key as (u,v) and values as weight associate with edge (u,v)
# @ total_vertices is the total count of unique vertices in the graph 
# @ v is vertex v 
def detect_negative_cycle(edge_weight,v,track,total_vertices):
            cycle_sum,cycle,current,i=0,[],v,0
            find_cycle_entry=set()
            #from vertex v checking any cycle is present in track map 
            while i<total_vertices and current not in find_cycle_entry :
                find_cycle_entry.add(current)
                current = track[current]
                if current==None:
                    break
                i+=1

            if current in find_cycle_entry and current is not None:
                getCycleVertexs(cycle,current,track)

            elif  not cycle or None in cycle:
                return
            
            for i in range(len(cycle)-1):
                    cycle_sum+=edge_weight[(cycle[i],cycle[i+1])]
                    print(f'    ( {cycle[i]}, {cycle[i+1]}, {edge_weight[(cycle[i],cycle[i+1])]:.3f}) --> {cycle_sum:.3f}')
            print(f'    ** {cycle[i]} ==> {cycle[i+1]} Enter a negative cycle.')
            print()

            return True
#Name: Satish Dodda Date: 11-nov 2024 Time: 2pm-3pm 
#method bellam_ford  method will call the update_dp_table method , it will update the dp table if it found a path in a  graph with no negative cycle in it 
# after updating the table we are just extracting the path using track table from last_vertex to 0 that is source and printing it 
# @ edges is the list which contains list of edges (u,v)
# @ weight_by_edges is a dict which will store key as (u,v) and values as weight associate with edge (u,v)
# @ total_vertices is the total count of unique vertices in the graph 
# @ source starting point which is 0 
def bellman_ford(edges,total_vertices, source,edge_weight):

    weight = defaultdict(lambda: math.inf)
    track = defaultdict(lambda: None)
    weight[source] = 0

    if update_dp_table(weight,track,edges,edge_weight,total_vertices):
        return 

    
    dq=deque()

    current = last_vertex-1
    while current is not None:
        dq.appendleft(current)
        current = track[current]
    if 0 not in dq:
        print("     *** There is no path.\n")
    else:        
        for i in range(len(dq)-1):
            print(f'    ( {dq[i]}, {dq[i+1]}, {edge_weight[(dq[i],dq[i+1])]:.3f}) --> {weight[dq[i+1]]:.3f}')
    print()

    
    


c=0
shortestPath={}
adjList={}
visited={}
last_vertex=0
count=0
is_negative=False
edges=[]
edge_weight={}
#reading the data from the file 
for i in file:
    #if encounter ** in line then , taking total vertex number from line
    if '**' in i:
        k=i.split('=')[1]
        k=k[0:k.index(',')]
        last_vertex=int(k)
    #if E and { is encounterd then it means edge tuple is started so updating c with 1 
    elif 'E' in i and '{' in i: 
        c=1 
    #if '--' and '=' not in line that means those are tuple of edges and weights processing it and updating the adjList 
    elif c and '--' not in i and '=' not in i:
        if '}' in i:
            i=i[0:i.index('}')]
        
        e=eval(i)  
        if e[-1]<0:
            is_negative=True  
        shortestPath[e[0]]=["",0]
        shortestPath[e[1]]=["",0]
        visited[e[0]]=0
        visited[e[1]]=0
        if e[0] not in adjList:
            adjList[e[0]]=[e[::-1]]
            
        else:
            adjList[e[0]].append(e[::-1])
        edges.append(e[0:-1])
        
        edge_weight[(e[0],e[1])]=e[2]
        # print(adjList)
    #if '--' is encounterd in line that means end of graph 
    elif '--' in i:
        # calling method and priting shortest path and clearing data form shortestPath and adjList 
        c=0
        count+=1
        print(f"G{count}’s shortest path from 0 to {last_vertex-1}:")
        if not is_negative:
            print("     Dijkstra’s Algorithm")
            computeDijkstra(shortestPath,adjList,visited,last_vertex-1)
        else:
            print("     Dynamic Programming")
            bellman_ford(edges, last_vertex, 0,edge_weight)
            
        edges.clear()
        shortestPath.clear()
        edge_weight.clear()
        adjList.clear()
        visited.clear()
        is_negative=False
#closing file       
file.close()