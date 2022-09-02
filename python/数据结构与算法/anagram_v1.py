"""变位词判断：计数比较法"""
from collections import Counter


def anagram_judge(s1, s2):
    if len(s1) == len(s2):
        s1_counter = Counter(s1)
        s2_counter = Counter(s2)
        for c in s1_counter.keys():
            if s1_counter.get(c) != s2_counter.get(c):
                return False
        return True
    else:
        return False


print(anagram_judge('rrwoy', 'yrrow'))
