import math
from enum import Enum

INVERSION_BOUND = 10  # pre-defined constant; independent of list input sizes

class MagicCase(Enum):
    GENERAL = 0
    SORTED = 1
    CONSTANT_NUM_INVERSIONS = 2
    REVERSE_SORTED = 3


def linear_scan(L):
    """checks whether a list is sorted, reverse sorted, or has a constant number of inversions. if not, then it is deemed a general list"""
    if all(L[i] <= L[i+1] for i in range(len(L)-1)):
        return MagicCase.SORTED
    elif all(L[i] >= L[i+1] for i in range(len(L)-1)):
        return MagicCase.REVERSE_SORTED
    
    inversion_count = 0
    for i in range(len(L)-1):
        if (L[i] > L[i+1]):
            inversion_count+=1
    if inversion_count < INVERSION_BOUND:
        return MagicCase.CONSTANT_NUM_INVERSIONS
    return MagicCase.GENERAL


def reverse_list(L, alg_set=None):
    """reverse a list by swapping the first and last elements, then the second and penultimate elements, and so on"""
    if alg_set is None:
        alg_set = set()
    left = 0
    right = len(L) - 1

    while left < right:
        L[left], L[right] = L[right], L[left]
        left += 1
        right -= 1
    return alg_set

def magic_insertionsort(L, left, right, alg_set=None):
    """insertion sort function that sorts within the given left and rught indices"""
    if alg_set is None:
        alg_set = set()
    for i in range(left+1, right):
        key = L[i]
        j = i - 1
        while j >= left and key < L[j]:
            L[j+1] = L[j]
            j -= 1
        L[j+1] = key
    return alg_set

def magic_mergesort(L, left, right, alg_set=None):
    """merge sort function that sorts within the given left and right indices"""
    if alg_set is None:
        alg_set = set()
    if right - left <= 20:
        magic_insertionsort(L, left, right, alg_set)
        alg_set.add('magic_insertionsort')
        return alg_set
    
    mid = (left+right)//2         
    magic_mergesort(L,left,mid, alg_set)
    magic_mergesort(L,mid,right, alg_set)

    _merge(L, left, mid, right)
    return alg_set 

def _merge(L, left, mid, right):
    """merges two sublists together"""
    A = L[left:mid]
    B = L[mid:right]

    i=0
    j=0
    index = left
    while i<len(A) or j<len(B):
        if (j==len(B)) or (i<len(A) and A[i] <= B[j]):
            L[index] = A[i]
            i+=1
        else:
            L[index] = B[j]
            j+=1
        index +=1

def magic_quicksort(L, left, right, depth=0, alg_set=None):
    """quick sort function that sorts within the given left and right indices"""
    if alg_set is None:
        alg_set = set()
    if right - left <= 20:
        magic_insertionsort(L, left, right, alg_set)
        alg_set.add('magic_insertionsort')
        return alg_set
    max_depth = math.log2(right-left)+1
    if depth > 2 * max_depth:
        magic_mergesort(L, left, right, alg_set)
        alg_set.add('magic_mergesort')
        return alg_set

    pivot_index = _partition(L, left, right)
    magic_quicksort(L, left, pivot_index, depth + 1, alg_set)
    magic_quicksort(L, pivot_index + 1, right, depth + 1, alg_set)
    return alg_set

def _partition(L, left, right):
    pivot = right - 1
    i=left
    j=pivot-1
    while i<j:
        while L[i] < L[pivot]:
            i+=1
        while i<j and L[j] >= L[pivot]:
            j-=1
        if i < j:
            L[i], L[j] = L[j], L[i]
    if L[pivot] <= L[i]:
        L[pivot], L[i] = L[i], L[pivot]
        pivot = i
    return pivot


def magicsort(L, alg_set = None):
    if alg_set is None:
        alg_set = set()  
    
    case = linear_scan(L)
    
    if case == MagicCase.SORTED:
        return alg_set
    elif case == MagicCase.CONSTANT_NUM_INVERSIONS:
        magic_insertionsort(L, 0, len(L))
        alg_set.add("magic_insertionsort")
    elif case == MagicCase.REVERSE_SORTED:
        reverse_list(L)
        alg_set.add("reverse_list")
        magic_mergesort(L, 0, len(L))
        alg_set.add("magic_mergesort")
    else:
        alg_set.add("magic_quicksort")
        magic_quicksort(L, 0, len(L), alg_set=alg_set)
    
    return alg_set
