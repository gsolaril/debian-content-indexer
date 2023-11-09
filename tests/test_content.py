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
    
    path_sample = "./temp/test_json_sample.json"
    path_verify = "./temp/test_json_verify.json"
    sample_filename = "usr/sbin/sendmail"
    sample_package = "devel/piglit"

    #▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
    @classmethod
    def setUpClass(cls):
        print(SEPARATOR)
        print("Note: default architecture \"amd64\" will be used.")
        #local_arch_allowed = ARCH_LOCAL_MACHINE in self.sample_archs
        #arch = None if local_arch_allowed else "amd64"
        cls.obj = DebianContentIndex(arch = "amd64")

    #▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
    def test_arch_exists(self):
        """
        Test case for accurate "`list_archs`" attribute - list and content.
        """
        print(" ===========> running test_arch_exists")
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
        print(" ===========> test_arch_exists OK!")

    #▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
    def test_file_packs(self):
        """
        Test case for accurate "filename vs list of its packages" table.
        """
        # Copy table so as not to affect the original.
        print(" ===========> running test_file_packs")
        msg_fail = "Table is empty."
        table = self.obj.table_file_packs.copy()
        self.assertGreater(table.shape[0], 0, msg = msg_fail)
        # Verify that the value type is a list of packages.
        msg_fail = "Table rightmost values are not lists"
        self.assertIsInstance(table.iloc[0], list, msg = msg_fail)
        # Verify that there are no duplicates.
        msg_fail = "Table contains duplicates."
        self.assertFalse(table.index.duplicated().any(), msg = msg_fail)
        # Filenames should all be given as paths.
        msg_fail = "Filenames should all be given as paths (contain \"/\")."
        self.assertTrue(table.index.str.contains("/").all(), msg = msg_fail)
        # Up to date, file included in the most packages should be the sample one.
        msg_fail = f"File \"{self.sample_filename}\" should be included in the most packages"
        count_packages = table.str.len().sort_values(ascending = False)
        filename_top, count_top = count_packages.index[0], count_packages.iloc[0]
        self.assertEqual(filename_top, self.sample_filename, msg = msg_fail)
        self.assertGreaterEqual(count_top, 8, msg = msg_fail)
        print(" ===========> test_table_file_packs OK!")

    #▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
    def test_pack_files(self):
        """
        Test case for accurate "package vs list of its filenames" table.
        """
        # Copy table so as not to affect the original.
        print(" ===========> running test_pack_files")
        msg_fail = "Table is empty."
        table = self.obj.table_pack_files.copy()
        self.assertGreater(table.shape[0], 0, msg = msg_fail)
        # Verify that the value type is a list of filenames.
        msg_fail = "Table rightmost values are not lists"
        self.assertIsInstance(table.iloc[0], list, msg = msg_fail)
        # Verify that there are no duplicates.
        msg_fail = "Table contains duplicates."
        self.assertFalse(table.index.duplicated().any(), msg = msg_fail)
        # Package names should not contain spaces.
        msg_fail = "Package names should not contain spaces."
        self.assertFalse(table.index.str.contains(" ").any(), msg = msg_fail)
        print(" ===========> test_table_pack_files OK!")

    #▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
    def test_ranking(self):
        """
        Test case for ranking table.
        """
        # Run ranking function for no top.
        print(" ===========> running test_ranking")
        table = self.obj.get_ranking(top := 0)
        msg_fail = "Ranking table should be empty."
        self.assertEqual(table.shape[0], 0, msg = msg_fail)
        # Run ranking function for 20 entries.
        table = self.obj.get_ranking(top := 20)
        # See if table type is alright: a Series.
        msg_fail = "Ranking table is not a Pandas' Series"
        self.assertIsInstance(table, Series, msg = msg_fail)
        # See if table size matches the given top parameter.
        msg_fail = "Ranking table doesn't have the right size."
        self.assertEqual(table.shape[0], top, msg = msg_fail)
        # See if the table is correctly sorted: max as first element.
        msg_fail = "Ranking table should have its max at the top."
        self.assertEqual(table.max(), table.iloc[0], msg = msg_fail)
        # Choose a random package and its file count.
        sample = table.sample(1)
        package, count = sample.index[0], sample.iloc[0]
        package_files = self.obj.table_pack_files[package]
        # Compare to source "package -> filenames" table.
        msg_fail = "File count in ranking is different to file list size in source table."
        self.assertEqual(count, len(package_files), msg = msg_fail)  
        # Check if topmost package in the ranking is the one considered.
        msg_fail = f"Package with largest file count is not \"{self.sample_package}\""
        self.assertEqual(table.index[0], self.sample_package, msg = msg_fail)
        print(" ===========> test_ranking OK!")
        
    #▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
    def test_save_package_json(self):
        """
        Test case for "`save_package_json`" method - json size and content.
        """
        print(" ===========> running test_save_package_json")
        # Save JSON file into specified temp directory.
        self.obj.save_package_json(json_save = self.path_sample)
        # Check if JSON file has been well generated.
        msg_fail = f"JSON file in \"{self.path_sample}\" does not exist."
        self.assertTrue(os.path.isfile(self.path_sample), msg = msg_fail)

        # Verify that the sample content json didn't end up empty.
        with open(self.path_sample) as json_file: sample = json.load(json_file)
        msg_fail = f"Sample content from file \"{self.path_sample}\" is empty."
        self.assertGreater(len(sample), 0, msg = msg_fail)

        # Note: JSONS are too heavy to be stored in "temp" folder in Github. So you'll have to generate the
        # verify file for yourself. Thus, don't enable the following section of the test unless having made
        # a JSON package-filenames' file beforehand, and having renamed it as "./temp/test_json_verify".

        if os.path.isfile(self.path_verify):
            # Read one "verifying" file that will be compared to sample content.
            with open(self.path_verify) as json_file: verify = json.load(json_file)
            # Both contents should be identical (though can fail if mirror was updated)
            msg_fail = f"Sample content does not match the one in \"{self.path_verify}\"."
            pack_sample = set(sample[self.sample_package])
            pack_verify = set(verify[self.sample_package])
            self.assertEqual(len(sample), len(verify), msg = msg_fail)
            self.assertEqual(pack_sample, pack_verify, msg = msg_fail)        
            print(" ===========> test_save_package_json OK!")

#█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████
#███████████████████████████████████████████████████████████████████████████████████████████████████   Run all tests   ███
#█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████

if (__name__ == "__main__"): main()