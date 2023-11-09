import sys, re, requests
from gzip import GzipFile
from io import BytesIO

sys.path.append("./")
from utils.constants import *

#█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████
#██████████████████████████████████████████████████████████████████████████████████████████████████████   Base class   ███
#█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████

class DebianDownloader:
    """
    Base class for content indexer of Debian packages. Instantiate and use:
     - "`directory`" property to get the available files with download count.
     - "`download`" method to specify and download files.\n
    For more info visit:
     - Help and definitions: "https://wiki.debian.org/RepositoryFormat#A.22Contents"
     - Mirror page with directory: "http://ftp.uk.debian.org/debian/dists/stable/main/"
    """
    class FileNotFound(Exception): pass

    URL_BASE = "http://ftp.uk.debian.org/debian/dists/stable/main/{filename}"
    REGEX_HREF = "(?<=href=\")[^/]+(?=\">)" # Should only include files, not subpaths (/).
    REGEX_DCNT = "(?<= )[0-9]+(?=\r)"       # Should only include numbers next to carry char.
    
    #▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
    def __init__(self):

        self._directory = self._get_directory()

    #▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
    @classmethod
    def _get_directory(cls):
        """[PRIVATE] Get file directory with download count."""
        url = cls.URL_BASE.format(filename = "")        # Use URL without endpoint to get directory page.
        resp = requests.get(url = url, timeout = 30)    # HTTP request for directory page content.
        resp = resp.content.decode("utf-8")             # Decode and convert binary content to string.
        files = re.findall(cls.REGEX_HREF, resp)        # Extract filenames from "href" tags in the HTML.
        dcount = re.findall(cls.REGEX_DCNT, resp)       # Extract download count; rightmost number in each line.
        return dict(zip(files, map(int, dcount)))       # Zip both lists as dictionary. Numbers shall be ints.
    
    #▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
    @property
    def directory(self):
        """Returns a dict with available filenames as keys and download counts as values."""
        return self._directory.copy()
    
    #▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
    def _check_exist_file(self, filename: str):
        """[PRIVATE] Verify if specified file exists."""
        return (filename in self._directory.keys())
    
    #▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
    def download(self, filename: str, path_save: str = None):
        """
        Download specified file from Debian repository.\n
        Inputs:
        - `filename` (`str`): The name of the file to download.\n
        - `path_save` (`str`) (optional): Path to save file to.\n
        Outputs:
        - `content` (`str`): The content of the downloaded file.\n
        """
        # Check if file exists. Else raise error.
        if not self._check_exist_file(filename):
            raise self.FileNotFound("\"%s\"" % filename)
        # If all good, HTTP request and download file.
        url = self.URL_BASE.format(filename = filename)
        resp = requests.get(url = url, timeout = 30)
        content = resp.content

        # If compressed, decompress before decoding.
        if filename.endswith(".gz"):
            content = BytesIO(content)
            with GzipFile(fileobj = content) as file:
                content = file.read()
        # Convert content into string.
        content = content.decode("utf-8")

        # Store content if path is given.
        if path_save is not None:
            with open(path_save, "w", errors = "ignore") as file:
                file.write(content) # Save content to path's file.
                print(f"Saved \"{filename}\" to \"{path_save}\".")
                
        return content
    
#█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████
#██████████████████████████████████████████████████████████████████████████████████████████████████████   Quick test   ███
#█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████

if (__name__ == "__main__"):

    obj = DebianDownloader()
    filename = "Contents-amd64"
    filename_gz = filename + ".gz"
    filename_txt = "./temp/" + filename + ".txt"
    print(SEPARATOR)
    print("About to download \"%s\"" % filename_gz)
    content = obj.download(filename_gz, filename_txt)

    preview = content.splitlines()
    print("\nPreview - first and last 5 lines:\n")
    preview = [*preview[: 5], "...", *preview[-5 :]]
    [print(line) for line in preview]; print(SEPARATOR)