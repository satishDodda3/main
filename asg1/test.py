import sys 
#reading filename and opening the file 
f=open(sys.argv[1])
f1=open("./test.txt",'a')

f1.seek(0)
f1.truncate()
f1.write("Gale-Shapley Algorithm\n\n")
from matching.algorithms import galeshapley
def printL(men, women,count):
    f1.write(" ** Set "+str(count)+"\n")
    matching = galeshapley(men, women)
    l=''
    for i, j in matching.items():
        l+=str((i,j))+" "
    l=l[0:-1]
    f1.write("(m, w): "+str(l)+'\n')
    matching = galeshapley(women, men)
    l1=''
    for i, j in matching.items():
        l1+=str((i,j))+" "
    l1=l1[0:-1]
    f1.write("(w, m): "+str(l1)+"\n")
    f1.write("\n")
men={}
women={}
count=0
#if i encounter m and : in the line that means i got men perference list so i am processing the data and storing it into map
for i in f:
    if len(i)!=0 and 'm' in i and ":" in i:
        s=i.split(":")
        if len(s[1].strip())>1:
            men[int(s[0][1::])]=eval(s[1].strip())
    if  len(i)!=0 and 'w' in i and ":" in i:
        s=i.split(":")
        if len(s[1].strip())>1:
            women[int(s[0][1::])]=(eval(s[1].strip()))
    #if i encounter the * means new set is begging so , processing the old list by calling printList method and clearing the men and woman map's
    if '*' in i and len(men)>0:
        count+=1
        printL(men,women,count)
        men={}
        women={}
printL(men,women,count+1)
f1.write("Satish Dodda")

