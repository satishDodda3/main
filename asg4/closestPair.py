#Name: Satish Dodda
#uild: 809961786
#pledge: This entire code was written by Satish Dodda 
#copyright: 2024 satish Dodda, unauthorized copying or modiying the code is not allowed 
import time 
import sys 
from decimal import Decimal
file=open(sys.argv[1])

# find distance method will find euclidean distance and return it 
# @ x and y are points 
# Satish Dodda , 15-oct-2024 started at 2:55pm finsihed at 3pm 
def find_distance(x,y):
    return (((x[0]-y[0])**2+(x[1]-y[1])**2)**0.5)
#find_closest_pair_using_brute_force method it will find closest pair and it's distance in a list of points using brute_force method 
# @x is a list of points 
# @strip is a boolean value 
# if strip is true  then it will update m value with 7 because for each value, compare it with the next 7 closest values
#Satish Dodda, 15-oct-2024, started at 2:40pm finished at 2:55pm
def find_closest_pair_using_brute_force(x,strip):
    min_distance=float('inf')
    pair=None
    m=len(x)
    if strip:
        m=7
    for i in range(len(x)):
        for j in range(i+1,min(i+m,len(x))):
            distance=find_distance(x[i],x[j])
            min_distance=min(min_distance,distance)
            if min_distance==distance:
                pair=(x[i],x[j])
    return (pair,min_distance)

# recursively_find_closest_pair method will recursively find the closest pairs and it's distance
#@ x is list of point which is sorted based on x coordinate 
#@ y is a list of point which is sorted based on y coordinate 
#Satish Dodda, 15-oct-2024, started at 2:10pm finished at 2:40pm
def recursively_find_closest_pair(x,y):
    n=len(x)
    # if len(x) is less than 4 it will find closest pair using brute force method and it will return it 
    if n<4: return find_closest_pair_using_brute_force(x,False)
    
    #finding the mid 
    mid=n//2
    #finding the mid point line 
    mid_point=x[mid][0]

    #dividing the points into two halfs 
    x_left=x[:mid]
    x_right=x[mid:]

    #seperating the values which is less than mid_point and greater than mid point 
    y_left=list(filter(lambda p:p[0]<=mid_point,y))
    y_right=list(filter(lambda p:p[0]>mid_point,y))
    
    #recursively calling the method it will find closest pairs in both left half and right half 
    l_pair,l_min_distance=recursively_find_closest_pair(x_left,y_left)
    r_pair,r_min_distance=recursively_find_closest_pair(x_right,y_right)

    # finding the minimum among the both left half and right half 
    min_distance=min(l_min_distance,r_min_distance)
    #if min_distance is equal to left half min distance then it update pair with l_pair otherwise r_pair 
    pair=l_pair  if min_distance==l_min_distance else r_pair 

    #creating the strip values 
    strip =[i for i in y if abs(i[0]-mid_point)<min_distance]
    #finding the cloest pair in strip and it's distance 
    s_pair,s_min_distance=find_closest_pair_using_brute_force(strip,True)
    # finding the minimum value  among the min_distance and strip distance 
    min_distance=min(min_distance,s_min_distance)
    # if min value is in strip then return the strip pair and strip distance otherwise min values among left or right halfs 
    return (s_pair,min_distance) if min_distance==s_min_distance else (pair,min_distance)

#method find_closest_pair will sort the data using x and y coordinates and find closest pair and it distance by calling recursively_find_closest_pair method 
# @l is list of points 
#Satish Dodda, 15-oct-2024, started at 2pm finished at 2:10pm
def find_closest_pair(l):
    sort_by_x=sorted(l,key=lambda x: x[0])
    sort_by_y=sorted(l,key=lambda y: y[0])
    #recursively calling the method 
    return recursively_find_closest_pair(sort_by_x,sort_by_y)
#list to store the points 
l=[]
#count is variable to count number of testcases 
count=1
# iterating over the list 
for i in file: 
    # if '(' in i then adding the tuple values to list 
    if '(' in i: 
        h=list(eval(i))
        x=round(float(h[0]),5)
        y=round(float(h[1]),5)
        l.append((x,y))
    # '--' is line that means test is ended calling the find_closest_pair method by passing l and printing it 
    elif '--' in i:
        #calculating the time 
        start=time.time()
        pair, distance = find_closest_pair(l)
        end=time.time()
        print(f"Set No {count}: {len(l)} points \n ({pair[0][0]:10.5f} ,{pair[0][1]:10.5f})-({pair[1][0]:10.5f} ,{pair[1][1]:10.5f})\n Distance = {"{:11.6f}".format(distance)} ({round((end-start)*1000,2)} ms)\n")
        count+=1
        l.clear()
print("By Satish Dodda")
file.close()    