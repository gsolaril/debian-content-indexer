import os, sys
sys.path.append("./")
from core.base import *
from core.content import *
from unittest import TestCase, main

#█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████
#████████████████████████████████████████████████████████████████████████████████████████████████   Base class tests   ███
#█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████

class TestDebianContentIndex(TestCase):
    """Test case for "`DebianContentIndex`" class."""

    invalid_arch = "arm32"
    sample_archs = [sample_arch := "amd64",
                 "arm64", "armel", "armhf"]

    #▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
    def setUp(self):
        self.obj = DebianContentIndex()

    #▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
    def test_arch_exists(self):
        """
        Test case for accurate "`list_archs`" attribute - list and content.
        """
        # Check if list of architectures is indeed a list.
        msg_fail = "List of architectures is not a list."
        self.assertIsInstance(self.obj.list_archs, list, msg = msg_fail)
        # Check if list of architectures  is not empty.
        msg_fail = "Directory is empty."
        self.assertGreater(len(self.obj.list_archs), 0, msg = msg_fail)
        # Check if list of architectures has the given architectures.
        msg_fail = "List of architectures does not contain given architectures."
        sample_archs_included = set(self.sample_archs).issubset(self.obj.list_archs)
        self.assertTrue(sample_archs_included, msg = msg_fail)

#█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████
#███████████████████████████████████████████████████████████████████████████████████████████████████   Run all tests   ███
#█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████

if (__name__ == "__main__"): main()