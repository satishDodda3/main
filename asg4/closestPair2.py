import sys 
import math
import time 
f=open(sys.argv[1])

# Helper function to calculate the Euclidean distance between two points
def euclidean_distance(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

# Brute force approach for small number of points (when n <= 3)
def brute_force(points):
    min_dist = float('inf')
    closest_pair = None
    n = len(points)
    for i in range(n):
        for j in range(i + 1, n):
            dist = euclidean_distance(points[i], points[j])
            if dist < min_dist:
                min_dist = dist
                closest_pair = (points[i], points[j])
    return closest_pair, min_dist

# Function to find the closest pair in a strip (points within a small range of the midpoint)
def closest_in_strip(strip, min_dist):
    strip.sort(key=lambda point: point[1])  # Sort strip by y-coordinate
    closest_pair = None
    n = len(strip)
    for i in range(n):
        for j in range(i + 1, min(i + 7, n)):  # Compare only with next 7 points (based on theory)
            dist = euclidean_distance(strip[i], strip[j])
            if dist < min_dist:
                min_dist = dist
                closest_pair = (strip[i], strip[j])
    return closest_pair, min_dist

# Recursive function to find the closest pair of points
def closest_pair_recursive(Px, Py):
    n = len(Px)

    # Base case: if 3 or fewer points, use brute force
    if n <= 3:
        return brute_force(Px)

    # Split points into two halves
    mid = n // 2
    Qx = Px[:mid]
    Rx = Px[mid:]

    # Find the midpoint line
    mid_x = Px[mid][0]
    Qy = list(filter(lambda p: p[0] <= mid_x, Py))
    Ry = list(filter(lambda p: p[0] > mid_x, Py))

    # Recursively find closest pairs in both halves
    (q_pair, q_min_dist) = closest_pair_recursive(Qx, Qy)
    (r_pair, r_min_dist) = closest_pair_recursive(Rx, Ry)

    # Find the minimum distance between the two halves
    if q_min_dist < r_min_dist:
        d_min = q_min_dist
        closest_pair = q_pair
    else:
        d_min = r_min_dist
        closest_pair = r_pair

    # Create a strip of points within distance d_min of the midpoint line
    strip = [p for p in Py if abs(p[0] - mid_x) < d_min]

    # Find closest pair in the strip
    (strip_pair, strip_min_dist) = closest_in_strip(strip, d_min)

    if strip_min_dist < d_min:
        return strip_pair, strip_min_dist
    else:
        return closest_pair, d_min

def closest_pair(points):
    Px = sorted(points, key=lambda point: point[0])
    Py = sorted(points, key=lambda point: point[1])

    # Call the recursive function
    return closest_pair_recursive(Px, Py)

l=[]
count=1
for i in f: 
    if '(' in i: 
        l.append(eval(i))
    elif '--' in i:
        start=time.time()
        pair, distance = closest_pair(l)
        end=time.time()
        print(f"Set No {count}: {len(l)} points \n ({pair[0][0]:10.5f} ,{pair[0][1]:10.5f})-({pair[1][0]:10.5f} ,{pair[1][1]:10.5f})\n Distance = {"{:11.6f}".format(distance)} ({round((end-start)*1000,2)} ms)\n")
        count+=1
        l.clear()
print("By Satish Dodda")