"""排序算法之交换排序"""


def sort(ls):
    """冒泡排序"""
    len_ls = len(ls)
    m, flag = 0, 1
    while flag == 1 and m <= len_ls-2:  # 要进行 len(ls)-1 趟的比较
        flag = 0
        for n in range(len_ls-m-1):
            if ls[n] > ls[n+1]:
                flag = 1
                ls[n], ls[n+1] = ls[n+1], ls[n]
        m += 1
    return ls

def sort_v2(ls):
    """冒泡排序-for循环写法"""
    for i in range(len(ls)-1):  # 要进行 len(ls)-1 趟的比较
        flag = False
        for j in range(len(ls)-1-i):
            if ls[j] > ls[j+1]:
                flag = True
                temp = ls[j]
                ls[j] = ls[j+1]
                ls[j+1] = temp
        if not flag:
            break
    return ls


def partition(ls, low, high):
    x = ls[low]
    while low < high:
        while low < high and ls[high] > x:
            high -= 1
        ls[low] = ls[high]
        while low < high and ls[low] < x:
            low += 1
        ls[high] = ls[low]
    focus = low
    ls[focus] = x
    return focus


def sort_v3(ls, low, high):
    """快速排序"""
    if low < high:
        focus = partition(ls, low, high)
        sort_v3(ls, low, focus-1)
        sort_v3(ls, focus+1, high)
    return ls


print(sort([33, 8, 45, 88, 99, 5, 11, 100]))
print(sort_v3([33, 8, 45, 88, 99, 5, 11, 100], 0, 7))
