import unittest
from x16test import x16Test, TestResult

class TestStdio(unittest.TestCase):
    src = []
    src_path = "src/"

    @x16Test("stdio.c")
    def test_Printf(self, result: TestResult):
        self.assertEqual(result.CPU.A, 0x00)
        self.assertEqual(result.RAM[0x90], 0x00)
