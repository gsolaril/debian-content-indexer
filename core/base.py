import os, sys, re, requests
from gzip import GzipFile
from io import BytesIO

sys.path.append("./")
from utils.constants import *

#█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████
#██████████████████████████████████████████████████████████████████████████████████████████████████████   Base class   ███
#█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████

class DebianDownloader:

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
    
#█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████
#██████████████████████████████████████████████████████████████████████████████████████████████████████   Quick test   ███
#█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████

if (__name__ == "__main__"):

    obj = DebianDownloader()
    print("Directory:\n", obj.directory)
