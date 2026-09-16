"""Pytest bootstrap: expose the src package so tests import finbank without installing it."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))
