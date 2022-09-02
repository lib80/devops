"""变位词判断：清点法"""


def anagram_judge(s1, s2):
    if len(s1) == len(s2):
        l1 = list(s1)
        l2 = list(s2)
        for c in l1:
            for pos in range(len(l2)):
                if l2[pos] == c:
                    l2[pos] = None
                    break
            else:
                return False
        return True
    else:
        return False


print(anagram_judge('wrroy', 'yrrow'))
