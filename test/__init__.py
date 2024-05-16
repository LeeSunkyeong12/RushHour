## every file should have __init__.py
# This will allow the pytest modules to be tested
# as long as under the same working directory as `__init__.py`

import sys
import os

# getcwd : get current working directory
sys.path.append(os.getcwd())
