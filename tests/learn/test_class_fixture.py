# https://pytest.org/en/7.1.x/how-to/unittest.html?highlight=unittest#mixing-pytest-fixtures-into-unittest-testcase-subclasses-using-marks
# doesn't work
# class TestExampleClass(unittest.TestCase):
#     @pytest.fixture()
#     def api_data(self):
#         return {
#             "results": [
#                 {"name": "first"},
#                 {"name": "second"},
#                 {"name": "third"},
#             ]
#         }

#     def test_fixture_param(self, api_data):
#         assert api_data["results"][0]["name"] == "first"
