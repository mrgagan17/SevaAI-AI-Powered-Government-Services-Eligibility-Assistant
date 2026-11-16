import sys
import os

# Ensure backend package is in python import path for pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
