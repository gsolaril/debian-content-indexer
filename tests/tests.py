import os, sys
sys.path.append("./")
from core.base import *
from unittest import TestCase, main

#█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████
#████████████████████████████████████████████████████████████████████████████████████████████████   Base class tests   ███
#█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████

class TestDebianDownloader(TestCase):
    """Test case for "`DebianDownloader`" class."""

    def setUp(self):
        self.obj = DebianDownloader()

#█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████
#███████████████████████████████████████████████████████████████████████████████████████████████████   Run all tests   ███
#█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████

if (__name__ == "__main__"): main()