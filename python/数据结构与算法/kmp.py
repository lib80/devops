"""字符串匹配之kmp算法"""


def kmp(ori_s, pat_s, next_ls):
    i, j = 0, 0
    while i <= len(ori_s)-1 and j <= len(pat_s)-1:
        if j == -1 or ori_s[i] == pat_s[j]:
            i += 1
            j += 1
        else:
            j = next_ls[j]
    if j > len(pat_s)-1:
        return i-len(pat_s)
    else:
        return 0


if __name__ == '__main__':
    ori_s = 'batdcibanbckbanbatanbw'
    pat_s = 'banbat'
    next_ls = [-1, 0, 0, 0, 1, 2]
    print(kmp(ori_s, pat_s, next_ls))
