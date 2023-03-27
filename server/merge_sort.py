# code from Module 6 Sorting Powerpoint Slide 89 - 90

def merge(item, left, mid, right):
    n1 = mid - left + 1
    n2 = right - mid 
    itemOne = [0] * n1
    itemTwo = [0] * n2

    # creating two array to store left and right half 
    for i in range(0, n1):
        itemOne[i] = item[left + i]

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
    


def merge_sort(item, left, right):
    if (left < right):
        # diving the item (// to return whole number)
        mid = left + (right - left) // 2
        merge_sort(item, left, mid)
        merge_sort(item, mid + 1, right)

        # merging back the lsit 
        merge(item, left, mid, right)

# based on my haskell implementation
def functional_merge_sort(items):
    def merge(left, right):
        if len(left) == 0:
            return right
        if len(right) == 0:
            return left

        if left[0] < right[0]:
            return left[:1] + merge(left[1:], right)
        else:
            return right[:1] + merge(left, right[1:])
    
    if len(items) == 1:
        return items
    else:
        mid = int(len(items) / 2)
        left = items[mid:]
        right = items[:mid]

        return merge(merge_sort(left), merge_sort(right))
