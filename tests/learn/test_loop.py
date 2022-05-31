"""Python Loops
See: https://docs.python.org/3.9/tutorial/controlflow.html#for-statements
"""
def test_for():
    numbers = [1, 2, 3]
    out = ""

    for num in numbers:
        out += str(num)

    assert out == "123"

def test_for_range():
    out = ""
    for value in range(1,3):
        out += str(value)
    assert out == "12"

def test_comprehension():
    bikes = ["yeti", "bmc", "salsa"]
    out = [bike.title() for bike in bikes]
    assert out == ["Yeti", "Bmc", "Salsa"]
