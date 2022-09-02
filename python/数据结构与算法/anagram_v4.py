"""变位词判断：排序后逐字比较法"""


def anagram_judge(s1, s2):
    if len(s1) == len(s2):
        l1 = sorted(s1)
        l2 = sorted(s2)
        for pos in range(len(l1)):
            if l1[pos] != l2[pos]:
                return False
        return True
    else:
        return False


print(anagram_judge('irroy', 'yrrow'))
