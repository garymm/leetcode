import collections
import copy
from typing import Optional
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def pathSum(self, root: Optional[TreeNode], targetSum: int, cumSum: int = 0, cumSumCount: Optional[dict[int, int]] = None) -> int:
        """
        Depth first traversal of the tree
        Keep a cumulative sum as we go
        keep a count of all cumSums along the current path
        We're looking for the number of paths that end here with the right sum,
        which means the cumSum here - cumSum to start of path = targetSum.
        So we search for cumSum here - targetSum = cumSum to start of path in the dict.
        That is the count of hits at the current node.
        The recurse.
        """
        if not root:
            return 0

        # need a count of 1 for zero to handle paths that include the root
        cumSumCount = cumSumCount or {0: 1}
        cumSum += root.val
        targetDiff = cumSum - targetSum
        hits = cumSumCount.get(targetDiff, 0)
        # add to dict after counting hits, otherwise we may double count.
        cumSumCount[cumSum] = cumSumCount.get(cumSum, 0) + 1

        left = self.pathSum(root.left, targetSum, cumSum=cumSum, cumSumCount=cumSumCount)
        right = self.pathSum(root.right, targetSum, cumSum=cumSum, cumSumCount=cumSumCount)

        cumSumCount[cumSum] -= 1

        return hits + left + right

def list_to_tree(lst):
    if not lst:
        return None

    root = TreeNode(lst[0])
    queue = [root]
    i = 1

    while queue and i < len(lst):
        node = queue.pop(0)
        if i < len(lst) and lst[i] is not None:
            node.left = TreeNode(lst[i])
            queue.append(node.left)
        i += 1

        if i < len(lst) and lst[i] is not None:
            node.right = TreeNode(lst[i])
            queue.append(node.right)
        i += 1

    return root

sol = Solution()
test_tree = list_to_tree([10,5,-3,3,2,None,11,3,-2,None,1])
res = sol.pathSum(test_tree, 8)
assert res == 3, res

test_tree = list_to_tree([5,4,8,11,None,13,4,7,2,None,None,5,1])
res = sol.pathSum(test_tree, 22)
assert res == 3, res

test_tree = list_to_tree([1])
res = sol.pathSum(test_tree, 0)
assert res == 0, res
