# code from Module 6 Sorting Powerpoint Slide 89 - 90

def Merge(item, left, mid, right):
    n1 = mid - left + 1
    n2 = right - mid 
    itemOne = [0] * n1
    itemTwo = [0] * n2

    # creating two array to store left and right half 
    for i in range(0, n1):
        itemOne[i] = item[left + 1]

    for j in range(0, n2):
        itemTwo[j] = item[mid + 1 + j]

    # merging the arrays 
    i = 0 
    j = 0 
    k = left 

    # check to see if we reached the end of the arrays 
    while i < n1 and j < n2:
        if (itemOne[i] <= itemTwo[j]):
            item[k] = itemOne[i]
            i = i + 1

        else: 
            item[k] = itemTwo[j]
            j = j + 1
        
        k = k + 1
    

    # when we run out of elements from one of the array 
    # append the rest of the array to the item 
    while (i < n1):
        item[k] = itemOne[i]
        i = i + 1
        k = k + 1

    while (j < n2):
        item[k] = itemTwo[j]
        j = j + 1
        k = k + 1
    


def MergeSort(item, left, right):
    if (left < right):
        # diving the item (// to return whole number)-----------------------------------> right here 
        mid = left + (right - left) // 2
        MergeSort(item, left, mid)
        MergeSort(item, mid + 1, right)

        # merging back the lsit 
        Merge(item, left, mid, right)



# test code 1 
item = [15, 2, 7, 0]

size = len(item)
print ("Array before sorting: ")
for i in range(size):
    print(item[i]),

MergeSort(item, 0, size - 1)

print ("\nArray after sorting: ")
for i in range(size):
    print(item[i]),
