import copy
from typing import Optional
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def pathSum(self, root: Optional[TreeNode], targetSum: int, cumSums: Optional[list[int]] = None) -> int:
        """
        Maybe
        Construct all paths from root to all leaves
        Keep running cumsum
        Search for pairs that differ by targetSum: O(n^2)
        """
        if not root:
            return 0

        hits = int(root.val == targetSum)
        cumSums = cumSums or []
        targetDiff = targetSum - root.val
        for cumSum in cumSums:
            if cumSum == targetDiff:
                hits += 1

        # print("cumSums", cumSums)

        cumSums.append(0)
        for i in range(len(cumSums)):
            cumSums[i] += root.val


        left = self.pathSum(root.left, targetSum, cumSums=copy.copy(cumSums))
        right = self.pathSum(root.right, targetSum, cumSums=copy.copy(cumSums))

        # print("root", root.val, "hits", hits, "left", left, "right", right)

        return (hits +
                left +
                right)

sol = Solution()
test_tree = TreeNode(
    10,
    right=TreeNode(-3, right=TreeNode(11)),
)
res = sol.pathSum(test_tree, 8)
assert res == 1, res
