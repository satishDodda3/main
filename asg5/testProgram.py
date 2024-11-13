import numpy as np
import matplotlib.pyplot as plt
import sys 
file=open(sys.argv[1])
lines=[]
for i in file:
    if '--' in i:
        continue 
    lines.append(tuple(map(float,i.split())))
lines=list(lines)

# Define the slopes and intercepts of the lines (m, c)
lines = np.array(lines)
highlighted_lines_indices = [0,1,2,3,4,5]

# Generate a wide range of x-values to simulate infinite length of lines
x_values = np.linspace(-1000, 1000, 10000)

# Plot each line
plt.figure(figsize=(20, 20))
for idx, line in enumerate(lines):
    m, c = line  # Extract slope and intercept
    y_values = m * x_values + c  # Calculate y-values for each line
    if idx in highlighted_lines_indices:
        plt.plot(x_values, y_values, label=f'Line {idx + 1} (y = {m:.2f}x + {c:.2f})', linewidth=2)
    else:
        plt.plot(x_values, y_values, color='black', linewidth=2)

# Highlight the point in the center
center_x = 0
center_y = 0
plt.plot(center_x, center_y, 'ro', markersize=10)  # Plot the center point in red with larger size
plt.text(center_x, center_y, f'({center_x}, {center_y})', fontsize=12, ha='right')

# Add labels and legend
plt.xlabel('x')
plt.ylabel('y')
plt.title('Top-Level View: Plotting All Lines with Infinite Length')
plt.legend()

# Set zoomed-out view to show more of the lines
plt.xlim([-1500, 1500])
plt.ylim([-1500, 1500])

# Display the plot with zoom in and zoom out functionality
plt.grid(True)
plt.show()
