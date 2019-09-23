from unittest import TestCase, expectedFailure
from x16test import Test, TestResult

class TestStdio(TestCase):
    src = ["quit.s"]
    src_path = "src/"

    @Test("printf.c")
    def test_printf(self, result: TestResult):
        pass

    @expectedFailure
    @Test("bcd.s")
    def test_bcd(self, result: TestResult):
        self.assertEqual(result.RAM[0x0], 32)
