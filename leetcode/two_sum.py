# https://leetcode.com/problems/two-sum/
from typing import List


class Solution:
    """Given nums, an array of ints and target, return indices of the two
    numbers such that they add up to target.

    Assume only one solution exists.
    Do not reuse elements.
    Return the answer in any order.
    """

    def twoSum(self, nums: List[int], target: int) -> List[int]:
        """

        Args:
            nums (List[int]): integers to use
            target (int): target

        Returns:
            List[int]: _description_
        """
        return Solution.brute_force(self, nums, target)

    def brute_force(self, nums: List[int], target: int) -> List[int]:
        """O(n^2)"""
        x = 0
        total = len(nums)
        for x in range(0, total):
            for y in range(x + 1, total):
                attempt = nums[x] + nums[y]
                if attempt == target:
                    return [x, y]

        raise Exception("Solution not found")

    def cache_searches(self, nums: List[int], target: int) -> List[int]:
        """
        Deduce the missing pair value (search) using the
        difference of target and number.

        Example:
        nums = [2,7]
        target = 9

        cache[7] = 1
        index = 0
        number = 2
        search = 7 # target - number
        if 7 in cache
            return [cache[7]=1, index]

        """
        cache: dict = {}
        for index, number in enumerate(nums):
            search = target - number
            if search in cache:
                return [cache[search], index]
            else:
                cache[number] = index

        raise Exception("Solution not found")


SCRATCH = """
Concerns:
- what if less than two elements given?
    - can't happen, there's always a solution AND constraints call out
      nums.length BETWEEN 2 && 10^4 (100,000)

nums = [2,7,11,15]
target = 9
output = [0,1]

O(n^2) quadratic solution
for idx, num in nums[0,nums.length-1]:
    for idx2, num2 in nums[idx+1,nums.length]:
        attempt = idx + idx2
        if attempt == target:
            return [idx, idx2]

"""
