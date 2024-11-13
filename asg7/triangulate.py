#Name: Satish Dodda
#uild: sdodda1
#pledge: This entire code was written by Satish Dodda 
#copyright: 2024 satish Dodda, unauthorized copying or modiying the code is not allowed

import sys
#method distance will calculate the euclidean distance between two points
# Satish Dodda , 5-nov-2024 started at 2:50pm finsihed at 3pm
def distance(point1, point2):
    return ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)**0.5

# polygon_perimeter will find the entire polygon perimeter by sum the distance between consecutive vertices 
# Satish Dodda , 5-nov-2024 started at 3pm finsihed at 3:10pm
def polygonPerimeter(polygon_vertices):
    perimeter = 0
    for i in range(len(polygon_vertices)):
        next_vertex_index = (i + 1) % len(polygon_vertices)
        edge_length = distance(polygon_vertices[i], polygon_vertices[next_vertex_index])
        perimeter += edge_length
    return perimeter

#cross_product method  will accepts there pairs of points and convert it into vectors and find the cross product 
# Satish Dodda , 5-nov-2024 started at 2:15pm finsihed at 2:20pm
def cross_product(origin, point_a, point_b):
    return (point_a[0] - origin[0]) * (point_b[1] - origin[1]) - (point_a[1] - origin[1]) * (point_b[0] - origin[0])

# is_conver_polygon is a method will call the cross_product method if cross_product is greater than 0  then direction is in anticlock wise if less than 0 then clock wise if it is zero then it is colinear 
# Satish Dodda , 5-nov-2024 started at 2:20pm finsihed at 2:50pm
def is_convex_polygon(polygon_vertices):
    num_vertices = len(polygon_vertices)
    if num_vertices < 3:
        #polygon with less than 3 vertices is not valid 
        return False  
    direction = 0
    for i in range(num_vertices):
        point_a, point_b, point_c = polygon_vertices[i], polygon_vertices[(i + 1) % num_vertices], polygon_vertices[(i + 2) % num_vertices]
        cross = cross_product(point_a, point_b, point_c)
        if cross != 0:
            if direction == 0:
                direction = 1 if cross > 0 else -1
            elif (cross > 0 and direction < 0) or (cross < 0 and direction > 0):
                # if not convex polygon it will return false
                return False 
    #if convex polygon then it will return true
    return True



#compute_triangle_perimeter will find the perimeter of the triangle formed by three points
# Satish Dodda , 5-nov-2024 started at 3:10pm finsihed at 3:20pm
def compute_triangle_perimeter(polygon_vertices, index_i, index_j, index_k):
    return distance(polygon_vertices[index_i], polygon_vertices[index_j]) + distance(polygon_vertices[index_j], polygon_vertices[index_k]) + distance(polygon_vertices[index_k], polygon_vertices[index_i])

# compute_chord_sum method will find the  chords of the minimum triangulation and their total length
# Satish Dodda , 5-nov-2024 started at 4pm finsihed at 4:30pm
def compute_chord_sum(polygon_vertices, track):
    chords = []
    distinct_chords = set()  # track unique chords
    chord_length_sum = 0
    #add_chords method will recurrsively add the chords for the optimal triangulation
    #satish dodda ,5-nov-2024 started at 4:5pm finished at 4:30pm
    def add_chords(si, ei):
        nonlocal chord_length_sum
        if ei - si < 2:
            return  # no valid chords in a segment with less than 2 points
        k = track[si][ei]
        if k != -1:
            #addes the chords  to chords list if it is not already added to the chords 
            if abs(si - ei) > 1 and (si == 0 and ei == len(polygon_vertices) - 1)==False:
                chord = (min(si, ei), max(si, ei))
                if chord not in distinct_chords:
                    distinct_chords.add(chord)
                    chords.append((polygon_vertices[si], polygon_vertices[ei]))
                    chord_length_sum += distance(polygon_vertices[si], polygon_vertices[ei])
            add_chords(si, k)  # recursively add chords on left segment
            add_chords(k, ei)  # recursively add chords on right segment

    add_chords(0, len(polygon_vertices) - 1)
    return chords, chord_length_sum
#compute_minimum_triangulation method will  find the minimum triangulation cost and chords for a convex polygon 
# Satish Dodda , 5-nov-2024 started at 3:20pm finsihed at 4pm
def compute_minimum_triangulation(polygon_vertices):
    num_vertices = len(polygon_vertices)
    dp = [[float('inf')] * num_vertices for _ in range(num_vertices)]
    track = [[-1] * num_vertices for _ in range(num_vertices)]

    for i in range(num_vertices - 1):
        #for adjacent vertices there will be no triangulation
        dp[i][i + 1] = 0  
    #start will start with small gap that is 2 and we will keep expand it will till num_vertices
    for gap in range(2, num_vertices): 
        for i in range(num_vertices - gap):
            j = i + gap
            for k in range(i + 1, j):
                #finding the triangulation cost with k as as dividing point 
                cost = dp[i][k] + dp[k][j] + compute_triangle_perimeter(polygon_vertices, i, k, j)
                if cost < dp[i][j]:
                    dp[i][j] = cost
                    #storing the diving point
                    track[i][j] = k  
    total_cost = polygonPerimeter(polygon_vertices)  # computing the polygon parameter 
    chords, chord_length_sum = compute_chord_sum(polygon_vertices, track)  # computing chords and additional cost
    total_cost += chord_length_sum
    return total_cost, chords



# displayOutput method will displays the triangulation result for each convex polygon
# Satish Dodda , 5-nov-2024 started at 4:30pm finsihed at 4:40pm

def displayOutput(polygon_number, triangulation_weight, chords):
    print(f"\n**Polygon no.{polygon_number} is convex.")
    print(f"Optimal Triangulation: minimum weight = {triangulation_weight:.6f}")
    print(f"{len(chords)} chords: (xi, yi)-(xj, yj)")
    for chord in chords:
        print(f"({chord[0][0]:.6f}, {chord[0][1]:.6f})-({chord[1][0]:.6f}, {chord[1][1]:.6f})")

# reads the polygons from the file where polygon is started when '--' encountered then it will identify as new polygon was started to it will add the vertices and calls the compute_minimum_triangualtion method and display the ouput 
# Satish Dodda , 5-nov-2024 started at 2pm finsihed at 4:45pm
index=0
def read_polygons(file_path):
    global index
    file = open(file_path)
    lines = file.readlines()
    vertices = []
    for line in lines:
        if '--' in line:
            if vertices:
                if is_convex_polygon(vertices):
                    triangulation_weight, chords = compute_minimum_triangulation(vertices)
                    displayOutput(index + 1, triangulation_weight, chords)
                else:
                    print(f"\n**Polygon no.{index + 1} is not convex.")
                index+=1
            vertices = []
        elif line.strip():
            vertices.append(tuple(map(float, line.strip().split())))
    if vertices:
        if is_convex_polygon(vertices):
            triangulation_weight, chords = compute_minimum_triangulation(vertices)
            displayOutput(index + 1, triangulation_weight, chords)
        else:
            print(f"\n**Polygon no.{index + 1} is not convex.")


polygons = read_polygons(sys.argv[1])


print("By Satish Dodda")
