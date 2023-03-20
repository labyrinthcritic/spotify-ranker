import random

from shell_sort import shell_sort

def test_shell_sort_one():
    list = [12, 34, 54, 2, 3]
    
    size = len(list)
    print("Array before sorting: ")
    for i in range(size):
        print(list[i]), 
    
    shell_sort(list)
    
    print("\nArray after sorting: ")
    for i in range(size):
        print(list[i]),

def test_shell_sort_two():
    randomList = []
    n = 100 
    for i in range(n): 
        randomList.append(random.randint(0,100))
    
    print("Array before sorting: ")
    for i in range(n):
        print(randomList[i]),
    
    shell_sort(randomList)
    
    print("\nArray after sorting: ")
    for i in range(n):
        print(randomList[i])
