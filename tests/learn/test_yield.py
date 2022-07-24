from unittest import mock

import pytest


class Loopy:
    """Experiment to hide the complexity of pagination behind an iterator.

    In Ruby this can be done with a lazy iterator utilizing yield.

    This approach allows clients to easily iterate very large data sets
    without Out Of Memory errors. It also hides the "complexity" of pagination.
    """

    def get_all(self, per_page=100):
        page = 0
        while True:
            data = self._get_page(per_page, page)

            if not data:
                break

            for item in data["data"]:
                yield item

            if not data["next"]:
                break

            page += 1

    def _get_page(self, per_page: int = 100, page: int = 0) -> dict:
        return {"page": page, "next": None, "data": []}


@pytest.fixture
def pages():
    data1 = [{"name": "first"}, {"name": "second"}]
    page1 = {"page": 1, "next": 2, "data": data1}

    data2 = [{"name": "third"}, {"name": "fourth"}]
    page2 = {"page": 2, "next": None, "data": data2}
    return [
        page1,
        page2,
    ]


def test_default_is_empty():
    loopy = Loopy()
    data = list(loopy.get_all())
    assert len(data) == 0


@mock.patch.object(Loopy, "_get_page")
def test_all_returns_everything(mock_page, pages):
    loopy = Loopy()

    mock_page.side_effect = pages

    data = list(loopy.get_all())

    assert len(data) == 4


# TODO is there a way to use fixtures in patches?
# it'd be cool to pass in a fixture which can auto-wire
# the return using another fixture
@mock.patch.object(Loopy, "_get_page")
def test_iterator_yields_items(mock_page, pages):
    loopy = Loopy()

    mock_page.side_effect = pages

    names = []
    for item in loopy.get_all():
        names.append(item["name"])

    assert names == ["first", "second", "third", "fourth"]
