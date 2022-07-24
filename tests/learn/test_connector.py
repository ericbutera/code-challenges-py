from unittest import mock

import pytest

from learn.connector import Connector, ConnectorWithClient


class TestConnector:
    @pytest.fixture
    def buckets(self):
        return {
            "buckets": [
                {"name": "mock-bucket-1", "location": "mock-location-1"},
                {"name": "mock-bucket-2", "location": "mock-location-2"},
            ]
        }

    @pytest.fixture()
    def s3_buckets(self, buckets):
        with mock.patch("learn.connector.Boto.get_client") as mock_client:
            mock_client.return_value.get_buckets.return_value = buckets
            yield mock_client

    @pytest.fixture()
    def s3_client(self, buckets):
        with mock.patch.object(Connector, "get_client") as mock_client:
            yield mock_client

    def test_scan_bucket_fetches_buckets(self, s3_buckets, buckets):
        # this bit of "much too clever" code will wire up get_buckets
        # inside `s3_buckets`
        connector = Connector()
        found = connector.run()
        assert buckets == found

    def test_scan_bucket_fetches_buckets2(self, s3_client, buckets):
        s3_client.return_value.get_buckets.return_value = buckets

        connector = Connector()
        found = connector.run()

        assert buckets == found

    @mock.patch("learn.connector.Boto.get_client")
    def test_scan_bucket_emits_findings(self, mock_s3_client):
        data = {
            "buckets": [
                {"name": "mock-bucket-1", "location": "mock-location-1"},
                {"name": "mock-bucket-2", "location": "mock-location-2"},
            ]
        }

        connector = Connector()
        mock_s3_client.return_value.get_buckets.return_value = data

        connector.run()

        assert len(connector._findings) == 2


class TestConnectorWithClient:
    @pytest.fixture
    def buckets(self):
        return {
            "buckets": [
                {"name": "mock-bucket-3", "location": "mock-location-3"},
                {"name": "mock-bucket-4", "location": "mock-location-4"},
            ]
        }

    @mock.patch("learn.connector.ConnectorWithClient.fetch_buckets")
    def test_patch_fetch_buckets(self, fetch_buckets, buckets):
        connector = ConnectorWithClient()
        fetch_buckets.return_value = buckets
        connector.run()
        assert len(connector._findings) == 2

    # TODO fix this
    # @mock.patch("learn.connector.ConnectorWithClient")
    # def test_patch_entire_class(self, connector, buckets):
    #     connector.fetch_buckets.return_value = buckets
    #     connector.run()
    #     assert len(connector._findings) == 2

    def test_patch_object_context(self, buckets):
        with mock.patch.object(
            ConnectorWithClient, "fetch_buckets", return_value=buckets
        ):
            connector = ConnectorWithClient()
            connector.run()
            assert len(connector._findings) == 2

    @mock.patch.object(ConnectorWithClient, "fetch_buckets")
    def test_patch_object_decorator(self, fetch_buckets, buckets):
        fetch_buckets.return_value = buckets
        connector = ConnectorWithClient()
        connector.run()
        assert len(connector._findings) == 2

    def test_patch_context(self, buckets):
        label = "learn.connector.ConnectorWithClient.fetch_buckets"
        with mock.patch(label, return_value=buckets):
            connector = ConnectorWithClient()
            connector.run()
            assert len(connector._findings) == 2
