import unittest

from tests.job_worker.test_parser import TestParser


def create_test_suite():
    test_suite = unittest.TestSuite()

    test_suite.addTest(TestParser())

    return test_suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    test_suite = create_test_suite()

    runner.run(test_suite)
