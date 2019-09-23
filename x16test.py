import unittest
import os.path
import re
import struct
from functools import wraps
from subprocess import run

class CPUResult:
    def __init__(self, file):
        s = struct.unpack('<BBBBBH', file.read(7))

        self.A = s[0]
        self.X = s[1]
        self.Y = s[2]
        self.SP = s[3]
        self.STATUS = s[4]
        self.PC = s[5]

class VRAMResult:
    def __init__(self, file):
        self.RAM = file.read(128 * 1024)
        self.COMPOSER = file.read(32)
        self.PALLETE = file.read(512)
        self.LAYER0 = file.read(16)
        self.LAYER1 = file.read(16)
        self.SPRITE_ATTRIBUTES = file.read(16)
        self.SPRITE_DATA = file.read(2 * 1024)

class TestResult:
    def __init__(self, file, stdout, shouldfail):
        self.CPU = CPUResult(file)
        self.RAM = file.read(4 * 1024)
        self.BANK = file.read(2 * 1024 * 1024)
        self.VIDEO = VRAMResult(file)
        if shouldfail:
            self.is_success = (self.RAM[0x90] != 0)
        else:
            self.is_success = (self.RAM[0x90] == 0)
        self.stdout = stdout
        pass

class Test(object):

    def __init__(self, *args, shouldfail=False):
        self.args = args
        self.sources = []
        self.shouldfail = shouldfail

    def __call__(self, func):
        def x16Test_wrapper(test):          
            path = self.__build(test)
            result = self.__run(path)

            test.assertTrue(result.is_success, "\n" + result.stdout)

            func(test, result)
        return x16Test_wrapper

    # __ build returns the path to the PRG file
    def __build(self, test) -> str:
        # Get sources (from sources and decorator parameters)
        if hasattr(test, "src"):
            if all(isinstance(s, str) for s in test.src):
                self.sources += test.src
            else:
                raise Exception("not all arguments in test class attribute 'src' are strings")
        if all(isinstance(s, str) for s in self.args):
                self.sources += self.args
        else:
            raise Exception("not all arguments in decorator arguments are strings")

        # Add source folder path to source files if present
        if hasattr(test, "src_path"):
            if isinstance(test.src_path, str):
                self.sources = list(map(lambda x: os.path.join(test.src_path, x), self.sources))
            else:
                raise Exception("the test class attribute 'src_path' is not a string")

        # compile + link files (using cl65!)
        return self.__compile()

    # returns the path to the compiled program
    def __compile(self):
        ret = run(["cl65", "-t", "cx16", "-o", "test.prg"] + self.sources, capture_output=True)
        if ret.returncode != 0:
            raise Exception("error while compiling test:\n" + str(ret.stderr))

        # calculate object file paths and remove them
        regex_sub = re.compile(r"(?i)\.asm$|\.[cs]$")
        regex_match = re.compile(r".*\.o$")     
        object_files = list(filter(regex_match.match, map(lambda x: regex_sub.sub(".o", x), self.sources)))
        for object_file in object_files:
            os.remove(object_file)

        return "test.prg"

    def __run(self, path):
        # Remove old dump files
        for item in os.listdir(os.getcwd()):
            if item.endswith(".bin"):
                os.remove(os.path.join(os.getcwd(), item))

        # Run with x16emu -dump CRBV, capture input and test if there is an error / state of STATUS
        # TODO: We could try to add a special encoding for the special codepage
        ret = run(["x16emu", "-dump", "CRBV", "-prg", "test.prg", "-run", "-echo"], capture_output=True, encoding="latin_1", timeout=30)
        if ret.returncode != 0:
            raise Exception("error while running test:\n" + ret.stderr)
        return self.__parseResult(ret.stdout)

    def __parseResult(self, stdout):
        dump = open("dump.bin","rb")
        result = TestResult(dump, stdout, self.shouldfail)
        dump.close()
        return result
