# code from Module 6 Sorting Powerpoint Slide 20 - 21

def partition(item, low, high):
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
        for j in range(low, 0, -1):
            if (item[down] < parPivot):
                break
            down -= 1
        
        if (up < down):
            item[up], item[down] = item[down], item[up]

        item[low], item[down] = item[down], item[low]
        
        return down
    

def quick_sort(item, low, high):
    if (low < high):
        pivot = partition(item, low, high)
        quick_sort(item, low, pivot - 1)
        quick_sort(item, pivot + 1, high)
