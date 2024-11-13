#Name: Satish Dodda
#uild: 809961786
#pledge: This entire code was written by Satish Dodda 
#copyright: 2024 satish Dodda, unauthorized copying of code is not allowed

#importing sys to handle commandline arugments 
import sys 
#reading filename and opening the file 
f=open(sys.argv[1])
print("Gale-Shapley Algorithm")

#Satish dodda ,5-sep-2024, started at 4pm and finished 7 pm
#Method computeGaleShapley which will accept men preference list and woman preference list , w, m variables for men m, and woman w 
#This method will only return dictionary 
def computeGaleShapley(men,women,w,m)->dict:
    #not_at_paired will store men/woman who are not at engaged 
    not_at_paired={}
    #men_status will store men as key and value as list in that first value is 0(unengaged ) or 1(engaged) second element is current prefered element index in preference list 
    men_status={}
    #woman_status will store woman as key and value as list in that first value is 0(unengaged ) or 1(engaged) second element is current prefered element index in preference list
    women_status={}
    #for men and woman i have updated name as key and 0,-1 as values 
    for i in men:
        not_at_paired[i]=0
        men_status[i]=[0,-1]
    for i in women:
        women_status[i]=[0,-1]
    #if any men/woman is not at paried then it will enter into while loop
    while(len(not_at_paired)>0):
        for i in men:
            #if men/woman not in paired list then updating his/her perference list index  and getting perfered men/woman based on index
            if i in not_at_paired:
                men_index=int(i[1::])
                men_status[i][1]+=1
                prefer=men[i][men_status[i][-1]]
                men_prew=w+str(prefer)
                #if men/woman is not at engaged , then updating the men and woman status with 1 and removing men/woman from not_at_paired map
                if women_status[men_prew][0]==0:
                    not_at_paired.pop(i)
                    women_status[men_prew][0]=men_status[i][0]=1
                    women_status[men_prew][1]=men_index
                #if woman is already engaged
                else:
                    #then finding the index of new men and old men  and if new men index is less than old men index in woman preference list 
                    #then ending relationship with old men and getting engaged with new men and updating the status of new men with 1 and adding old men again to not_at_paired map
                    men_index_in_wp=women[men_prew].index(men_index)
                    old_men_index_in_wp=women[men_prew].index(women_status[men_prew][1])
                    old_man=m+str(women[men_prew][old_men_index_in_wp])
                    if(men_index_in_wp<old_men_index_in_wp):
                        not_at_paired.pop(i)
                        not_at_paired[old_man]=men_status[old_man][0]=0
                        men_status[i][0]=1
                        women_status[men_prew][1]=int(i[1::])
    #finally returning the list   
    return women_status

#satish dodda ,5-sep-2024 ,started at 7:10pm finished at 7:30pm
#this method will process the returned list from computeGaleShapley method and sort the data to get correct order and then printing it 
def printList(men,women,count,m,w):
    print("\n ** Set",count)
    final_list=sorted([(j[1],int(i[1::])) for i ,j in computeGaleShapley(men,women,'w','m').items()])
    print("(m, w):",*final_list)
    final_list=sorted([(j[1],int(i[1::])) for i ,j in computeGaleShapley(women,men,'m','w').items()])
    print("(w, m):",*final_list)
#men and woman dict is used to store preference list 
men={}
women={}
count=0
#if i encounter m and : in the line that means i got men perference list so i am processing the data and storing it into map
for i in f:
    if len(i)!=0 and 'm' in i and ":" in i:
        s=i.split(":")
        if len(s[1].strip())>1:
            men[s[0]]=eval(s[1].strip())
    if  len(i)!=0 and 'w' in i and ":" in i:
        s=i.split(":")
        if len(s[1].strip())>1:
            women[s[0]]=(eval(s[1].strip()))
    #if i encounter the * means new set is begging so , processing the old list by calling printList method and clearing the men and woman map's
    if '*' in i and len(men)>0:
        count+=1 
        printList(men,women,count,'m','w')
        men={}
        women={}
printList(men,women,count+1,'m','w')
f.close()
print("\nSatish Dodda")
