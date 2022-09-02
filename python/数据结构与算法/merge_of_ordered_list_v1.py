"""有序表的合并-顺序表实现"""
lc = []


def merge_ordered_list(la, lb):
    i, j = 0, 0
    while i <= len(la)-1 and j <= len(lb)-1:
        if la[i] <= lb[j]:
            lc.append(la[i])
            i += 1
        else:
            lc.append(lb[j])
            j += 1

    if i > len(la)-1:
        while j <= len(lb)-1:
            lc.append(lb[j])
            j += 1
    else:
        while i <= len(la)-1:
            lc.append(lb[i])
            i += 1

    return lc


print(merge_ordered_list([1, 7, 8], [2, 4, 6, 8, 10, 11]))
