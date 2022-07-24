# https://leetcode.com/problems/valid-parentheses/


class Solution:
    INVERSE = {
        "[": "]",
        "]": "[",
        "(": ")",
        ")": "(",
        "{": "}",
        "}": "{",
    }
    STARTS = ["[", "{", "("]
    ENDS = ["]", "}", ")"]

    stack: list[str]

    def isValid(self, s: str) -> bool:
        # print(f"parsing `{s}`")

        # reset stack per run; would be better not to be a class prop
        self.stack = []

        for char in s:
            if not self.parse_char(char):
                return False

        if len(self.stack) > 0:
            # print(f"error: found {len(self.stack)} unclosed expressions")
            return False

        # TODO i don't like an implicit pass, find a way to invert so it
        # fails unless explicitly allowed
        return True

    def parse_char(self, char: str) -> bool:
        # TODO assumption that input chars are expression only
        if char in self.STARTS:
            self.stack.append(char)
            return True

        if char in self.ENDS:
            if len(self.stack) == 0:
                return False  # not enough stack to close

            last = self.stack.pop()
            inverse = self.INVERSE[char]
            if last == inverse:
                return True

            # print(f"error: found {char}; expected {inverse}")

        return False


NOTES = """
- track open/close of () {} and []
- brackets must be closed by same type
- must be closed in correct order

constants:
INVERSE = {
    '[' => ']',
    ']' => '[',
    '(' => ')',
    ')' => '(',
    '{' => '}',
    '}' => '{',
}
STARTS = ["[", "{", "("]
ENDS = ["]", "}", ")"]

# keeps track of opened expressions & order (required to close)
stack = []


char-parser(char):
    switch (char):
    char in starts:
        # nesting always allowed
        stack.add(char)

    char in ends:
        # closing requires last stack char to match 'inverse' of current char
        last-open-char = stack.pop
        inverse-char = INVERSE[char] # '}' becomes '{'
        if last-open-char != inverse-of-end-char
            syntax-error

is-valid(string):
    for char in string:
        char-parser(char)


potential things that might help:
- tokenizer
- state machine
"""
