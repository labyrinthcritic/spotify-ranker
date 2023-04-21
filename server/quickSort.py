# code from Module 6 Sorting Powerpoint Slide 20 - 21

def Partition(item, low, high):
    parPivot = item[low]
    up = low
    down = high

    while low < high:
        j = up 
        for j in range(high):
            if (item[up] > parPivot):
                break
            up  = up + 1

        j = high 
        for j in range (low, 0, -1):
            if (item[down] < parPivot):
                break
            down = down - 1
        
        if (up < down):
            item[up], item[down] = item[down], item[up]

        item[low], item[down] = item[down], item[low]
        
        return down
    

def QuickSort(item, low, high):
    
    if (low < high):
        pivot = Partition(item, low, high)
        QuickSort(item, low, pivot - 1)
        QuickSort(item, pivot + 1, high)



"""
# Test Code 

data = [15, 0, 5, 6]
size = len(data)

print ("Array before sorting: ")
for i in range (size):
    print(data[i]),

QuickSort(data, 0, size - 1)

print ("Array after sorting: ")
for i in range (size):
    print (data[i])

"""