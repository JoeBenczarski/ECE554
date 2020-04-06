#
# reverse.py
#

def reverse(arr, start, end):
    while start < end:
        temp = arr[start]
        arr[start] = arr[end]
        arr[end] = temp
        start += 1
        end -= 1
    
def rotate_left(arr, d):
    n = len(arr)    
    reverse(arr, 0, d-1)
    reverse(arr, d, n-1)
    reverse(arr, 0, n-1)

def rotate_right(arr, d):
    n = len(arr)
    reverse(arr, n-d, n-1)
    reverse(arr, 0, n-d-1)
    reverse(arr, 0, n-1)
