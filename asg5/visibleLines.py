import sys 
file =open(sys.argv[1])
#Name: Satish Dodda
#uild: sdodda1
#pledge: This entire code was written by Satish Dodda 
#copyright: 2024 satish Dodda, unauthorized copying or modiying the code is not allowed 

# divide_lines it will recurssively divides the lines in two half if number of lines greater than 1 and named then left and right half's  ,after divison it will call merge method to merge the lines 
# @ lines contains list of lines which conatins slopes and y intersect's 
# Satish Dodda , 22-oct-2024 started at 4pm finsihed at 4:15pm
def divide_lines(lines):
    n = len(lines)
    if n >=2:
        left_half = lines[:n // 2]
        right_half = lines[n // 2:]
        return merge_lines(divide_lines(left_half), divide_lines(right_half))
    
    return lines

#find_intersection_point method will find inserting point bewteen two lines 
# @ lines1 , lines2 contains which conatins slopes and y intersect's
# Satish Dodda , 22-oct-2024 started at 4:15pm finsihed at 4:20pm
def find_intersection_point(line1, line2):
    return (line2[1]-line1[1])/(line1[0]-line2[0])

#merge_lines function will merge the lines and remove un visible lines from list of lines and return visible lines back
# @ left_half contains list of lines which conatins slopes and y intersect's 
# @ right_half contains list of lines which conatins slopes and y intersect's 
# Satish Dodda , 22-oct-2024 started at 4:20pm finsihed at 5pm
def merge_lines(left_half, right_half):
    lines = []
    #adding left_hlaf and right_half to lines because these lines are already sorted 
    lines.extend(left_half)
    lines.extend(right_half)

    final_visible_lines = []
    # if we found paraller lines in the lines then , will consider the lines with hightest y intersect 
    for line in lines:
        if not final_visible_lines or final_visible_lines[-1][0] != line[0]:
            final_visible_lines.append(line)
        elif final_visible_lines[-1][1] < line[1]:
            final_visible_lines[-1] = line
    
    if len(final_visible_lines)<2:
        return final_visible_lines
    
    visible_lines = [final_visible_lines.pop(0), final_visible_lines.pop(0)]
    num_visible = 2
    # here checking if three lines are intersecting with each other 
    for l in final_visible_lines:
        last_line ,next_to_last_line= visible_lines[num_visible - 1],visible_lines[num_visible - 2]
        prev_intersect=find_intersection_point(next_to_last_line,last_line)
        curr_intersect=find_intersection_point(next_to_last_line,l)
        # if inserting point of first and second line is greater than thrid and second , then removing unvisible second line 
        while curr_intersect < prev_intersect:
            visible_lines.pop(num_visible - 1)
            num_visible -= 1
            if num_visible == 1:
                break
            last_line,next_to_last_line = visible_lines[num_visible - 1],visible_lines[num_visible - 2]
            prev_intersect=find_intersection_point(next_to_last_line,last_line)
            curr_intersect=find_intersection_point(next_to_last_line,l)
        visible_lines.append(l)
        num_visible += 1
    #returning the visible lines 
    return visible_lines

#lines is list to store the slope and y intersect of points 
lines=[]
for i in file:
    # '--' in line then ignoring those lines 
    if '--' in i:
        continue 
    # adding lines to list 
    lines.append(list(map(float,i.split())))
#sorting the lines using the slope 
lines.sort()

count=0
#printing the visible lines 
for line in divide_lines(lines):
        print(f"{count}: m: {line[0]:.5f} k: {line[1]:.5f}")
        count+=1

