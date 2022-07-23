import pytest
from learn.leetcode.two_sum import Solution


examples = [
    ([2, 7, 11, 15], 9, [0, 1]),
    ([3, 2, 4], 6, [1, 2]),
    ([3, 3], 6, [0, 1]),
]


@pytest.mark.parametrize("nums,target,expected", examples)
def test_examples(nums, target, expected):
    actual = Solution().twoSum(nums, target)
    assert expected == actual


@pytest.mark.parametrize("nums,target,expected", examples)
def test_cache_searches(nums, target, expected):
    actual = Solution().cache_searches(nums, target)
    assert expected == actual
