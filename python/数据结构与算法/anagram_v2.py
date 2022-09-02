"""变位词判断：计数比较法"""


def anagram_judge(s1, s2):
    if len(s1) == len(s2):
        s1_counter = {}
        s2_counter = {}
        for i, j in zip(s1, s2):
            s1_counter[i] = s1_counter.setdefault(i, 0) + 1
            s2_counter[j] = s2_counter.setdefault(j, 0) + 1
        for c in s1_counter.keys():
            if s1_counter.get(c) != s2_counter.get(c):
                return False
        return True
    else:
        return False


print(anagram_judge('rrroy', 'yrrow'))
