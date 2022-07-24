"""Python Lists
See: https://docs.python.org/3.9/tutorial/datastructures.html
"""


def test_read():
    bikes = ["yeti", "bmc"]
    assert bikes[1] == "bmc"


def test_modify():
    bikes = ["yeti"]
    bikes[0] = "yeti sb130"
    assert bikes[0] == "yeti sb130"


def test_append():
    bikes = []
    bikes.append("cinelli")
    assert bikes[0] == "cinelli"


def test_insert():
    bikes = ["yeti"]
    bikes.insert(0, "salsa")
    assert bikes[0] == "salsa"


def test_pop():
    bikes = ["yeti"]
    item = bikes.pop()
    assert item == "yeti"


def test_slice():
    """
    Note: Python's slices stop 1 index before item specified
    """
    bikes = ["yeti", "bmc", "salsa", "cinelli", "bianchi"]
    assert bikes[1:4] == ["bmc", "salsa", "cinelli"]
    assert bikes[4] == "bianchi"


def test_in():
    bikes = ["yeti"]
    assert "yeti" in bikes


def test_size():
    bikes = ["yeti"]
    assert len(bikes) == 1


def test_for_loop():
    bikes = ["yeti", "bmc"]

    out = ""
    for bike in bikes:
        out += bike

    assert out == "yetibmc"
