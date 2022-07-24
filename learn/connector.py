from array import array


class ServiceClient:
    account: str
    secret: str
    region: str

    def __init__(self, account: str, secret: str, region: str):
        self.account = account
        self.secret = secret
        self.region = region


class S3Client(ServiceClient):
    def get_buckets(self):
        return {
            "buckets": [
                {"name": "live-service-1", "location": "live-location-1"},
                {"name": "live-service-2", "location": "live-location-2"},
            ]
        }


class Boto:
    def get_client(service: str, account: str, secret: str, region: str):
        if service == "s3":
            return S3Client(account, secret, region)
        raise Exception("Unknown service: " + service)


# TODO record type
class Finding:
    label: str
    value: str

    def __init__(self, label: str, value: str) -> None:
        self.label = label
        self.value = value


class Connector:
    _findings: array  # [Finding]

    def __init__(self):
        self._findings = []

    def get_client(self, service: str) -> ServiceClient:
        return Boto.get_client(service, "account", "secret", "region")

    def run(self):
        client = self.get_client("s3")
        buckets = client.get_buckets()

        for bucket in buckets.get("buckets"):
            name = bucket.get("name")
            value = bucket.get("location")
            self.emit(Finding(name, value))

        return buckets

    def emit(self, data: Finding):
        self._findings.append(data)


class ConnectorWithClient:
    _findings: array  # [Finding]

    def __init__(self):
        self._findings = []

    def run(self):
        buckets = self.fetch_buckets()
        for bucket in buckets.get("buckets"):
            name = bucket.get("name")
            value = bucket.get("location")
            self.emit(Finding(name, value))

    def get_client(self, service: str) -> ServiceClient:
        """Boto Service Client Factory"""
        return Boto.get_client(service, "account", "secret", "region")

    def fetch_buckets(self):
        client = self.get_client("s3")
        return client.get_buckets()

    def emit(self, data: Finding):
        self._findings.append(data)


class ConnectorClientFactory:
    def get_client(service: str) -> ServiceClient:
        """Boto Service Client Factory"""
        return Boto.get_client(service, "account", "secret", "region")


class ConnectorInjection:
    _findings: array  # [Finding]

    def __init__(self):
        self._findings = []

    def run(self):
        buckets = self.fetch_buckets()
        self.process_buckets(buckets)
        return True

    def process_buckets(self):
        buckets = self.fetch_buckets()
        for bucket in buckets.get("buckets"):
            name = bucket.get("name")
            value = bucket.get("location")
            self.emit(Finding(name, value))

    def fetch_buckets(self):
        bucket_client = ConnectorClientFactory().get_client("s3")
        return bucket_client.get_buckets()

    def emit(self, data: Finding):
        self._findings.append(data)
