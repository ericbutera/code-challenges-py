from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

import pytest


@dataclass
class RawScanData:
    type: str
    data: dict


class Emitter:
    _data: list[RawScanData] = []

    def emit(self, scan_data: RawScanData):
        """Save collected raw scan data"""
        print(f"Emitting {scan_data}")
        self._data.append(scan_data)


class Scanner(ABC):
    """Scan a specific thing."""

    @abstractmethod
    def scan(self, emitter: Emitter) -> None:
        pass


class ScannerSuite(ABC):
    """Suite comprised of scanners."""

    _scanners: list[Scanner] = []
    _emitter: Emitter

    def __init__(self, emitter: Optional[Emitter] = None) -> None:
        self._emitter = emitter or Emitter()

    def scanners(self, *scanners: Scanner):
        self._scanners = []
        for scanner in scanners:
            print(f"Adding scanner {scanner}")
            self._scanners.append(scanner)

    def scan(self):
        # async scanning of things
        for scanner in self._scanners:
            print(f"ScannerSuite scan {scanner}")
            # TODO i wonder if its possible to pass this as a callable
            # how would callable arg typing work?
            scanner.scan(self._emitter)

        print(f"Finished {len(self._scanners)} scanners")


# normally these would be in modules
class Aws:
    class S3(Scanner):
        TYPE = "s3"

        def scan(self, emitter: Emitter) -> None:
            print(f"Scanning {self.__class__}")
            emitter.emit(RawScanData(type=self.TYPE, data=self.fetch()))

        def fetch(self):
            # concerns: paging, client connections, credential refresh, etc
            return {"Buckets": [{"Name": "bucket1"}, {"Name": "bucket2"}]}

    class EC2(Scanner):
        TYPE = "ec2"

        def scan(self, emitter: Emitter) -> None:
            print(f"Scanning {self.__class__}")
            emitter.emit(RawScanData(type=self.TYPE, data=self.fetch()))

        def fetch(self):
            instance = {"InstanceId": "i-12345"}
            reservation = {"Instances": [instance]}
            return {"Reservations": [reservation]}

    class Suite(ScannerSuite):
        pass


@pytest.fixture()
def full_scanner():
    emitter = Emitter()
    aws = Aws.Suite(emitter)
    aws.scanners(Aws.S3(), Aws.EC2())
    return aws, emitter


def test_aws(full_scanner):
    aws, emitter = full_scanner
    aws.scan()
    assert len(emitter._data) == 2
