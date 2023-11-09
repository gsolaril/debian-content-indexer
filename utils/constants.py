import os
from platform import uname

# Get the local machine's CPU architecture.
# Will be used as default when no input given.
ARCH_LOCAL_MACHINE = uname().machine.lower()
# Just the local path of wherever this repo is held.
THIS_PATH = os.path.split(__file__)[0]

SEPARATOR = "–" * 100