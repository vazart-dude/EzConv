# EzConv - Currency Converter

## Build Instructions

### Prerequisites
1. Python 3.x with pip
2. PyInstaller (`pip install pyinstaller`)
3. Inno Setup (https://www.jrsoftware.org/is.php)
4. PyQt6 (`pip install PyQt6`)
5. requests, arrow, bs4, python-dotenv

### Build Steps

#### 1. Install Python dependencies
```bash
pip install -r requirements.txt
```

#### 2. Build the executable with PyInstaller
```bash
python build.py
```

This creates a standalone executable in `dist/EzConv/`.

#### 3. Build the installer with Inno Setup
1. Open Inno Setup Compiler
2. Open `EzConv.iss`
3. Press F9 to compile
4. The installer will be created in the `Output` directory

#### 4. Test the installer
Run the generated `.exe` file to install EzConv on your system.

### Project Structure
- `main.py` - Main application entry point
- `rate_update.py` - Fiat currency rates updater
- `rate_update_crypto.py` - Cryptocurrency rates updater
- `GUI/` - UI design files
- `bin/` - Data files (currencies, logs)
- `img/` - Application icons and images

### Dependencies
See `requirements.txt` for all dependencies.