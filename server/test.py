from random import randint

from shell_sort import shell_sort
from merge_sort import merge_sort

def run_all_tests() -> None:
    tests = [test_shell_sort, test_merge_sort]
    for test in tests:
        test()

def test_shell_sort() -> None:
    print('Testing shell sort.')
    
    items = [randint(1, 30) for _ in range(30)]
    
    print(f'Before: {items}')    
    
    shell_sort(items)

    print(f' After: {items}')

def test_merge_sort() -> None:
    print('Testing merge sort.')
    
    items = [randint(1, 30) for _ in range(30)]
    
    print(f'Before: {items}')    
    
    merge_sort(items, 0, len(items) - 1)

    print(f' After: {items}')
