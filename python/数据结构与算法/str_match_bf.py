"""字符串匹配-BF算法"""
def index_bf(s, t):
    i = j = 0
    while i <= len(s)-1 and j <= len(t)-1:
        if s[i] == t[j]:
            i += 1
            j += 1
        else:
            i = i - j + 1
            j = 0
    if j > len(t)-1:
        return i - len(t)  # 或者 return i - j
    else:
        return False


print(index_bf('woiqfepfqref', 'qfep'))
