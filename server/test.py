import random

from shell_sort import shell_sort
from merge_sort import merge_sort

def run_all_tests() -> None:
    tests = [test_shell_sort_one, test_shell_sort_two, test_merge_sort]
    for test in tests:
        test()

def test_shell_sort_one() -> None:
    list = [12, 34, 54, 2, 3]
    
    size = len(list)
    print("Array before sorting: ")
    for i in range(size):
        print(list[i]), 
    
    shell_sort(list)
    
    print("\nArray after sorting: ")
    for i in range(size):
        print(list[i]),

def test_shell_sort_two() -> None:
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

def test_merge_sort() -> None:
    item = [15, 2, 7, 0]
    
    size = len(item)
    print("Array before sorting: ")
    for i in range(size):
        print(item[i]),
    
    merge_sort(item, 0, size - 1)
    
    print("\nArray after sorting: ")
    for i in range(size):
        print(item[i])
