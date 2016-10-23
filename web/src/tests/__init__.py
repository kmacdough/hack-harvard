import unittest
from .test_api import TestApi


def suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestApi)
    return suite

suite = suite()
