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
    
    #▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
    def __init__(self, filename: str):

        self.filename = filename
        self.url = self.URL_BASE.format(filename = filename)
    
#█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████
#██████████████████████████████████████████████████████████████████████████████████████████████████████   Quick test   ███
#█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████

if (__name__ == "__main__"):

    obj = DebianDownloader(filename = "Contents-amd64")
    print("Filename:", obj.filename)
    print("URL:", obj.url)
