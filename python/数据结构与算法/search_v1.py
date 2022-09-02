"""查找算法之折半查找"""


def search(e, ls):
    """非递归算法"""
    low, high = 0, len(ls)-1
    while low <= high:
        mid = (low + high) // 2
        if e < ls[mid]:
            high = mid - 1
        elif e > ls[mid]:
            low = mid + 1
        else:
            return mid
    return None


def search_v2(e, ls, low, high):
    """递归算法"""
    if low > high:
        return None
    else:
        mid = (low + high) // 2
        if e == ls[mid]:
            return mid
        elif e < ls[mid]:
            return search_v2(e, ls, low, mid-1)
        else:
            return search_v2(e, ls, mid+1, high)



print(search(50, [2, 5, 8, 15, 22, 50, 100]))
print(search_v2(8, [2, 5, 8, 15, 22, 50, 100], 0, 6))
