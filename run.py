#!/usr/bin/env python3
"""Run the Book Library API from the project root."""

import subprocess
import sys
from pathlib import Path

# Change to library-api directory
app_dir = Path(__file__).parent / "library-api"
sys.exit(subprocess.call([sys.executable, str(app_dir / "main.py")], cwd=app_dir))
