PythonBot – Installation & Usage Guide
======================================

1. Requirements
---------------
- Windows PC
- Python 3.8 or newer (https://www.python.org/downloads/)
- Alternatively: Use the ready-to-run EXE from the release (no Python installation needed)

2. Installation (Python version)
-------------------------------
a) Download all files from the release (including main.py, requirements.txt, icon.ico).
b) Open a command prompt in the project folder.
c) Install dependencies:
   pip install -r requirements.txt

3. Running (Python version)
---------------------------
a) Start the program:
   python main.py

b) On first start, you will be asked for a 4-digit code.
   - Open the website: https://ljashub.github.io/triggerbot-gui/
   - Enter the current code shown there.

c) The graphical interface will open. Choose your settings, hotkeys, colors, etc.

4. Using the EXE (recommended for end users)
--------------------------------------------
a) Download the ready-to-use PythonBot.exe from:
   https://github.com/ljashub/triggerbot-gui/releases/tag/pythonbot

b) Start PythonBot.exe with a double-click.
c) Follow the instructions as above (Verification Code).

5. Notes
--------
- The verification code changes every 30 seconds on the website.
- For updates, simply download the new version.
- If you have problems: provide the error message and your Python version.

6. Build your own EXE (optional)
--------------------------------
a) Install PyInstaller:
   pip install pyinstaller

b) Build the EXE:
   python -m PyInstaller --onefile --noconsole --icon=icon.ico --name PythonBot main.py

c) The EXE will be in the dist/ folder.

Enjoy using PythonBot!
