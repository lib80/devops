"""二叉树：列表实现"""


def binary_tree(data, left=None, right=None):
    return [data, left, right]


def is_empty_btree(btree):
    return btree is None


def get_root(btree):
    return btree[0]


def get_left(btree):
    return btree[1]


def get_right(btree):
    return btree[2]


def set_root(btree, data):
    btree[0] = data


def set_left(btree, left):
    btree[1] = left


def set_right(btree, right):
    btree[2] = right


def depth(btree):
    if not btree:
        return 0
    else:
        m = depth(btree[1])
        n = depth(btree[2])
        if m > n:
            return m + 1
        else:
            return n + 1


def copy(btree):
    if not btree:
        new_t = None
    else:
        left = copy(btree[1])
        right = copy(btree[2])
        new_t = binary_tree(btree[0], left, right)
    return new_t


def node_count(btree):
    if not btree:
        return 0
    else:
        return node_count(btree[1]) + node_count(btree[2]) + 1


def lead_count(btree):
    if not btree:
        return 0
    if not (btree[1] or btree[2]):  # 左右子树均为None才是叶子节点
        return 1
    return lead_count(btree[1]) + lead_count(btree[2])



my_tree = ['a', ['b', ['d', [], []], ['e', [], []]], ['c', ['f', [], []], []]]
print(depth(my_tree))
print(copy(my_tree))
