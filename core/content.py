import os, sys, re, json
from pandas import Series, Index

sys.path.append("./")
from utils.constants import *
from core.base import DebianDownloader

#█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████
#██████████████████████████████████████████████████████████████████████████████████████████████████████   Main class   ███
#█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████

class DebianContentIndex(DebianDownloader):
    """
    Class to download and parse specific contents-index files from the Debian mirror.
    Inherits its structure from parent class "`DebianDownloader`". Upon instantiation, it will parse the
    associated contents-index file and tabulate its data based on existent Debian packages and inner files.
    Inputs:
     - "`arch`" (`str`): The architecture on which the contents-index file is to be downloaded. If not
        specified, it will consider the architecture of the machine where this code is executed in. An
        "`ArchitectureNotFound`" error will be triggered when given architecture is not available.\n
    Methods:
     - "`directory`" (property, `str`) to get the available files with download count.
     - "`list_archs`" (property, `list`) to get the architectures that are available on directory.
     - "`table_file_packs`" (property, `Series`) to get a table of existent files and which packages they belong to.
     - "`table_pack_files`" (property, `Series`) to get a table of existent packages and which files do they include.
     - "`get_ranking`" (method, `Series`) to get a ranking of the packages with the most files included.\n
    For more info visit:
     - Help and definitions: "https://wiki.debian.org/RepositoryFormat#A.22Contents"
     - Mirror page with directory: "http://ftp.uk.debian.org/debian/dists/stable/main/"
    """

    class ArchitectureNotFound(Exception): pass

    FILENAME_ARCH = "Contents-{arch}.gz" # Filename format.
    URL_ARCH = DebianDownloader.URL_BASE + FILENAME_ARCH

    # Find like: "Contents- | alphanumeric whatever | .gz"
    REGEX_ARCH_LOCATE = "(?<=Contents-)\\w+(?=\\.gz)"
    # To keep the "alphanumeric whatever" from the middle.
    REGEX_ARCH_EXTRACT = "(Contents-|\\.gz)"

    #▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
    def __init__(self, arch: str = None):

        super().__init__() # Construct parent class instance.
        if arch is None: # When no arch given, use the one found above.
            comment = "Warning - No architecture given. Using local:"
            print(comment, "\"%s\"" % (arch := ARCH_LOCAL_MACHINE))

        # Regex patterns: hover mouse over "self.REGEX_ARCH_..." right below.
        finder_locate_arch = lambda s: re.findall(self.REGEX_ARCH_LOCATE, s)
        filter_extract_arch = lambda s: re.sub(self.REGEX_ARCH_EXTRACT, "", s)
        # Find filenames with an architecture string. Extract such strings.
        self._archs = filter(finder_locate_arch, self._directory.keys())
        self._archs = list(map(filter_extract_arch, self._archs))
        # If the given architecture is not in the list, raise error.
        if not self._check_exist_arch(arch):
            error = f"\"{arch}\" is invalid. Please use one of these:\n  ==> "
            raise self.ArchitectureNotFound(error + str.join(", ", self._archs))
        
        self._arch = arch # Store arch and associated filename for URL.
        self._filename = self.FILENAME_ARCH.format(arch = self._arch)
        
        # Download decoded file content, like the parent class.
        content = super().download(self._filename)
        # Parse content and get "filename vs list of its packages" table.
        self._table_file_packs = self.get_table_file_packs(content)
        # Group content and get "package vs list of its filenames" table.
        self._table_pack_files = self.get_table_pack_files(self._table_file_packs)
    
    #▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
    def _check_exist_arch(self, arch: str):
        """[PRIVATE] Verify if specified file exists."""
        return (arch in self._archs)
        
    #▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
    @classmethod
    def get_table_file_packs(cls, content: str):
        """
        [PRIVATE] Build an actual table from the content of the file.\n
        Can be easily manipulated further on with the use of Pandas' operations.\n
        Inputs:
        - `content` (`str`): The content of the downloaded file.\n
        Outputs:
        - `packages` (`Series[str, str]`): Parsed contents' table. Each row holds
            a filename (left/index), with its associated packages to the right.\n
        """
        # Get a list of the file content's lines, and turn into series.
        packages = Series(content.splitlines())
        # Remove any empty / meaningless line.
        packages = packages.loc[packages != ""]
        # Split each line into its 2 parts: filename (left) and its packages (right).
        # Careful: some filenames may have spaces so the split count is not always 2.
        packages = packages.str.split(" +")
        # Package name is the rightmost element (no spaces).
        # Join back the others at the left and get the filename.
        files = packages.str[: -1].str.join(" ")
        # Convert to index.
        files = Index(files, name = "filename")
        # Comma-split rightmost packages and get package list.
        packages = packages.str[-1].str.split(",")
        # Use packages' "series" as a 2-column table.
        return Series(data = packages.values, index = files, name = "packages")

    #▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
    @classmethod
    def get_table_pack_files(cls, file_packs: Series) -> Series:
        """
        [PRIVATE] "Flip" the contents' index structure to get packages and its associated files.\n
        Inputs:
        - `file_packs` (`Series[str, str]`): The tabulated "filename -> packages" series.\n
        Outputs:
        - `pack_files` (`Series[str, list[str]]`): The tabulated "package -> filenames" series.
        """
        # Expand each row with multiple packages into individual file-package rows.
        # "file: [pack_a, pack_b, pack_c]" -> "file: pack_a, file: pack_b, file: pack_c"
        pack_files = file_packs.explode().reset_index()
        # Get a table of one row per package, and all of its associated files.
        return pack_files.groupby("packages")["filename"].apply(list)

    #▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
    @property
    def arch(self):
        """Getter for specified architecture."""
        return self._arch
    @property
    def list_archs(self):
        """Getter for available architectures"""
        return self._archs
    @property
    def table_file_packs(self):
        """Getter for "filename -> packages" table."""
        return self._table_file_packs.copy()
    @property
    def table_pack_files(self):
        """Getter for "package -> filenames" table."""
        return self._table_pack_files.copy()
        
    #▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
    def get_ranking(self, top: int = 10):
        """
        Get the "top N" packages with the most files.\n
        Inputs:
        - `top` (`int`): The number of packages to return.\n
        Outputs:
        - `counter` (`Series`): The number of files for each package.
        """
        # Count the amount of files for each package.
        counter = self._table_pack_files.str.len()
        # Rename the column for better visualization.
        counter = counter.rename("file_count")
        # Return the top N packages, highest being above.
        return counter.sort_values(ascending = False).head(top)
    
#█████████████████████████████████████████ Small test
    
if (__name__ == "__main__"):

    obj = DebianContentIndex("i386")
    print(obj.get_ranking(10))
