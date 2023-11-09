import os, sys
sys.path.append("./")
from core.base import *
from core.content import *
from unittest import TestCase, main

#█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████
#████████████████████████████████████████████████████████████████████████████████████████████████   Base class tests   ███
#█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████

class TestDebianDownloader(TestCase):
    """Test case for "`DebianDownloader`" class."""

    invalid_file = "Contents-invalid.gz"
    sample_files = [sample_file := "Contents-amd64.gz",
              "Contents-arm64.gz", "Contents-armel.gz",
              "Contents-armhf.gz", "Contents-i386.gz" ]
    
    path_sample = "./temp/test_content_sample.txt"
    path_verify = "./temp/test_content_verify.txt"

    #▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
    def setUp(self):
        self.obj = DebianDownloader()

    #▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
    def test_directory_exists(self):
        """
        Test case for successful "`_get_directory`" function.
        """
        # Check if directory is indeed a dict.
        msg_fail = "Directory is not a dict."
        self.assertIsInstance(self.obj.directory, dict, msg = msg_fail)
        # Check if directory is not empty.
        msg_fail = "Directory is empty."
        self.assertGreater(len(self.obj.directory), 0, msg = msg_fail)

    #▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
    def test_directory_content(self):
        """
        Test case for content inside "`_directory`" attribute.
        """    
        for file in self.sample_files:
            # Check if sample files are available in directory.
            msg_fail = f"\"{file}\" not found in directory."
            self.assertTrue(self.obj._check_exist_file(file), msg = msg_fail)
            # Check if there's any path (not file) in directory.
            msg_fail = f"\"{file}\" is a path, not a file."
            self.assertFalse(file.__contains__("/"), msg = msg_fail)
            # Check if download count is an integer.
            msg_fail = f"\"{file}\" download count is not an integer."
            self.assertIsInstance(self.obj.directory[file], int, msg = msg_fail)
    
    #▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
    def test_download_sample(self):
        """
        Test case for "`download`" method - retrieval and storage.
        """
        # First check if it raises "FileNotFound" when file does not exist in mirror.
        self.assertRaises(self.obj.FileNotFound, self.obj.download, self.invalid_file)
        # Then check if it correctly downloads and interprets the sample arch file.
        content_sample = self.obj.download(self.sample_file, path_save = self.path_sample)
        msg_fail = f"Returned sample content from \"{self.sample_file}\" not string."
        self.assertIsInstance(content_sample, str, msg = msg_fail)

        # Now check if it correctly saves the sample arch file.
        msg_fail = f"File was not correctly saved in \"{self.path_sample}\"."
        self.assertTrue(os.path.isfile(self.path_sample), msg = msg_fail)

    #▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
    def test_download_verify(self):
        """
        Test case for "`download_verify`" method - size and content.
        """
        # Read the sample content file downloaded within the previous test.
        with open(self.path_sample, "r") as file:
            content_sample = file.read().splitlines()
        # Verify that the sample content file didn't end up empty.
        msg_fail = f"Sample content from file \"{self.sample_file}\" is empty."
        self.assertTrue(content_sample != "", msg = msg_fail)
        # Read one "verifying" file that will be compared to sample content.
        with open(self.path_verify, "r") as file:
            content_verify = file.read().splitlines()
        # Shorten the sample content to the length of the verifying content.
        content_sample_short = content_sample[: len(content_verify)]
        # Both contents should be identical (though can fail if mirror was updated)
        msg_fail = f"Sample content does not match the one in \"{self.path_verify}\"."
        self.assertEqual(content_sample_short, content_verify, msg = msg_fail)

#█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████
#███████████████████████████████████████████████████████████████████████████████████████████████████   Run all tests   ███
#█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████

if (__name__ == "__main__"): main()