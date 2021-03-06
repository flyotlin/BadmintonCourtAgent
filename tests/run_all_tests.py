import unittest

from tests.job_worker.test_parser import TestParser
from tests.test_agent_check import TestAgentCheck
from tests.test_db import TestDB


def create_test_suite():
    test_suite = unittest.TestSuite()

    test_suite.addTest(TestParser())
    test_suite.addTest(TestAgentCheck())
    test_suite.addTest(TestDB())

    return test_suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    test_suite = create_test_suite()

    runner.run(test_suite)
