#import random 

def ShellSort(list):
    
    # initial value of the gap n / 2 
    size = len(list)
    gap = int(size / 2)

    # iterating until gap == 1 
    while gap > 0:

        # iterating through arr by gap size 
        for i in range(size): 
            slowNum = i 
            fastNum = i 

            # check if numbers are in range 
            if (fastNum + gap) < size:
                fastNum = i + gap

                # check to see if swap is required 
                if list[slowNum] > list[fastNum]:
                    temp = list[slowNum]
                    list[slowNum] = list[fastNum]
                    list[fastNum] = temp 

                    # checking to see if swaps before is required 
                    slowNum = slowNum - gap 
                    fastNum = fastNum - gap  

                    while (slowNum >= 0 and fastNum <= size): 
                       # swap required 
                       if list[slowNum] > list[fastNum]:
                            temp = list[slowNum]
                            list[slowNum] = list[fastNum]
                            list[fastNum] = temp

                            slowNum = slowNum - gap 
                            fastNum = fastNum - gap  

                       else: 
                           break; 


        # after iterating through the array with the gap 
        # increment the gap --> incrementation from shell sort pseudocode slide 74
        if gap == 2:
            gap = 1
 
        else:
            gap = int(gap / 2)



"""
# test code 1
list = [12, 34, 54, 2, 3]

size = len(list)
print ("Array before sorting: ")
for i in range(size):
    print (list[i]), 

ShellSort(list)

print ("\nArray after sorting: ")
for i in range(size):
    print(list[i]),


# test code 2
randomList = []
n = 100 
for i in range(n): 
    randomList.append(random.randint(0,100))

print ("Array before sorting: ")
for i in range(n):
    print (randomList[i]),

ShellSort(randomList)

print ("\nArray after sorting: ")
for i in range(n):
    print(randomList[i])

"""


                    
            




