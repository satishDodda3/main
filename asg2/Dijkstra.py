#Name: Satish Dodda
#ULID: 809961786
#Pledge : This entire code was developed by my self 
#copyright: without authorization copying or modifying the code is not allowed


#importing the sys package to handel the command line arguments 
import sys
#importing the heapq package for priority queue 
import heapq
#Accepting the file name as argument and opening the file 

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
            print('*** There is no path.\n')
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
            print((i[1],i[0],round(i[-1]-track,3)),'-->' ,round(i[-1],3))
            track=i[-1]
        # for i in stack[::-1]:
        #     for j in adjList[i[1]]:
        #         if(j[-1]==i[1] and j[1]==i[0]):
        #             print(j[::-1],'-->',round(i[-1],3))
        #             break
        print()
c=0
shortestPath={}
adjList={}
visited={}
last_vertex=0
count=0

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
        # a=i.strip().split(',')  
        # e=(int(a[0][1::].strip()),int(a[1].strip()),float(a[2][0:-1].strip()))
        e=eval(i)    
        #print(e)
        shortestPath[e[0]]=["",0]
        visited[e[0]]=0
        if e[0] not in adjList:
            adjList[e[0]]=[e[::-1]]
            
        else:
            adjList[e[0]].append(e[::-1])
    #if '--' is encounterd in line that means end of graph 
    elif '--' in i:
        # calling method and priting shortest path and clearing data form shortestPath and adjList 
        c=0
        count+=1
        print(f"G{count}’s shortest path from 0 to {last_vertex-1}:")
        computeDijkstra(shortestPath,adjList,visited,last_vertex-1)
        shortestPath.clear()
        adjList.clear()
        visited.clear()
#closing file       
file.close()