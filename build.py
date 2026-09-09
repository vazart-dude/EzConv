"""Build script for EzConv using PyInstaller."""
import os
import sys
import subprocess
import shutil
from pathlib import Path

# Clean previous builds
build_dir = Path("build")
dist_dir = Path("dist")
spec_dir = Path(".")

for dir_path in [build_dir, dist_dir]:
    if dir_path.exists():
        shutil.rmtree(dir_path)

# PyInstaller command for one-directory build
cmd = [
    sys.executable,
    "-m",
    "PyInstaller",
    "--noconfirm",
    "--clean",
    "--windowed",  # Hide console for GUI app
    "--name", "EzConv",
    "--add-data", "bin;bin",
    "--add-data", "img;img",
    "--add-data", "GUI;GUI",
    "--hidden-import", "PyQt6",
    "--hidden-import", "PyQt6.QtWidgets",
    "--hidden-import", "PyQt6.QtGui",
    "--hidden-import", "PyQt6.QtCore",
    "--hidden-import", "PyQt6.uic",
    "--hidden-import", "requests",
    "--hidden-import", "csv",
    "--hidden-import", "arrow",
    "main.py",
]

print("Building EzConv with PyInstaller...")
print("Command:", " ".join(cmd))

result = subprocess.run(cmd, check=False)

if result.returncode != 0:
    print("Build failed!")
    sys.exit(1)

print("Build completed successfully!")
print(f"Output directory: {dist_dir.absolute()}")