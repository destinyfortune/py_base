# -*- coding: utf-8 -*-


# 查找列表中重复元素
def get_duplicate_set(some_list):
    duplicates = set([x for x in some_list if some_list.count(x) > 1])
    return duplicates


# 求两个列表的交集
def get_interset_set(list1, list2):
    valid = set(list1)
    input_set = set(list2)
    return input_set.intersection(valid)


# 求两个列表的差集
def get_difference_set(list1, list2):
    valid = set(list1)
    input_set = set(list2)
    return input_set.difference(valid)

