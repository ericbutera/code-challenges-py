import pytest
from leetcode.valid_parenthesis import Solution


examples = [
    ("()", True),
    ("(]", False),
    ("([", False),
    ("{[]}", True),
    ("(({}))", True),
]


@pytest.mark.parametrize("input,expected", examples)
def test_is_valid(input: str, expected: bool):
    s = Solution()
    assert s.isValid(input) == expected
