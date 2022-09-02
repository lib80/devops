"""排序算法之插入排序"""


def sort(ls):
    """直接插入排序"""
    for i in range(1, len(ls)):
        e = ls[i]
        j = i - 1
        while j >= 0 and e < ls[j]:
            ls[j+1] = ls[j]  # 记录后移
            j -= 1
        ls[j+1] = e  # 插入到正确位置
    return ls


def sort_v2(ls):
    """折半插入排序"""
    for i in range(1, len(ls)):
        e = ls[i]
        low, high = 0, i-1
        while low <= high:
            mid = (low+high) // 2
            if e < ls[mid]:
                high = mid - 1
            else:
                low = mid + 1
        # 循环结束，high+1为插入位置
        for j in range(i-1, high, -1):
            ls[j+1] = ls[j]  # 插入前先移动元素
        ls[high+1] = e  # 插入到正确位置
    return ls


def shell_insert(ls, step):
    for i in range(step, len(ls)):
        e = ls[i]
        j = i - step
        while j >= 0 and e < ls[j]:
            ls[j+step] = ls[j]  # 记录后移
            j -= step
        ls[j+step] = e  # 插入到正确位置


def sort_v3(ls, dlta_ls):
    """希尔排序"""
    for step in dlta_ls:  # dlta_ls为步长因子列表
        shell_insert(ls, step)
    return ls


print(sort([33, 8, 45, 88, 99, 5, 11, 100]))
print(sort_v2([33, 8, 45, 88, 99, 5, 11, 100]))
print(sort_v3([33, 8, 45, 88, 99, 5, 11, 100], [5, 3, 1]))
