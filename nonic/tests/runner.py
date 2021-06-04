import time
from unittest.runner import TextTestResult, TextTestRunner

from django.test.runner import DiscoverRunner


class TimedTextTestResult(TextTestResult):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.clocks = dict()

    def startTest(self, test):
        self.clocks[test] = time.time()
        super().startTest(test)
        self.stream.write(self.getDescription(test))
        self.stream.write("-->")
        self.stream.flush()

    def addSuccess(self, test):
        super().addSuccess(test)
        self.stream.write(f" {time.time() - self.clocks[test]:.3f}s\n")


class TimedTextTestRunner(TextTestRunner):
    resultclass = TimedTextTestResult


class TimedRunner(DiscoverRunner):
    test_runner = TimedTextTestRunner


