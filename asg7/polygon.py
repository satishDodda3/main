import numpy as np
import math
import matplotlib.pyplot as plt
import sys

# Function to read vertices from a file
def read_vertices(filename):
    vertices = []
    with open(filename) as file:
        for line in file:
            if '--' in line:
                continue
            vertices.append(tuple(map(float, line.split())))
    return vertices

# Function to compute the cross product of vectors
def cross_product(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

# Function to check if the polygon is convex
def is_convex(polygon):
    n = len(polygon)
    if n < 3:
        return False
    direction = 0
    for i in range(n):
        a, b, c = polygon[i], polygon[(i + 1) % n], polygon[(i + 2) % n]
        cross = cross_product(a, b, c)
        if cross != 0:
            if direction == 0:
                direction = 1 if cross > 0 else -1
            elif (cross > 0 and direction < 0) or (cross < 0 and direction > 0):
                return False
    return True

# Function to plot the polygon with the given vertices
def plot_polygon(vertices):
    x_coords, y_coords = zip(*vertices)

    # Close the polygon by adding the first point at the end
    x_coords += (x_coords[0],)
    y_coords += (y_coords[0],)

    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.plot(x_coords, y_coords, 'b-', linewidth=2, marker='o')  # Polygon edges with markers for vertices
    plt.fill(x_coords, y_coords, alpha=0.3)  # Fill the polygon with transparency

    # Annotate the vertices
    for i, (x, y) in enumerate(vertices):
        plt.annotate(f'v{i+1}', (x, y), textcoords="offset points", xytext=(0,10), ha='center')

    plt.title('Polygon')
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.grid(True)
    plt.xlim(min(x_coords) - 10, max(x_coords) + 10)
    plt.ylim(min(y_coords) - 10, max(y_coords) + 10)
    plt.show()

def main(file_path):
    vertices = read_vertices(file_path)

    if is_convex(vertices):
        print("The given polygon is convex.")
        plot_polygon(vertices)
    else:
        print("The given polygon is not convex.")
        plot_polygon(vertices)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python plot_polygon.py <path_to_input_file>")
    else:
        main(sys.argv[1])
