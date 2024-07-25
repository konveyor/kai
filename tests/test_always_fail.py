import unittest


class TestAlwaysFail(unittest.TestCase):
    def test_always_fail(self):
        self.fail("This test always fails")
