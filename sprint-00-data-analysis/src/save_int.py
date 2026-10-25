from heapq import *


def find_pair(nums, target):
    vals = set()
    for i in nums:
        if (target-i) in vals:
            return [i, target-i]
        else:
            vals.add(i)


print(find_pair([3, 8, 2, 10, 5],13))
##