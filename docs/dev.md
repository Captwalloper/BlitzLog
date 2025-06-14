# Notes
* All commands assume workind directory of BlitzLog

# Setup
* get python3
* `pip install -r requirements.txt`

# Run
* `python -m app.app`

# Distribute (Windows only)
* [pyinstaller](https://pyinstaller.org/en/stable/)
* `pyi-makespec --onefile --windowed --name BlitzLog app.py`
* `pyinstaller --clean BlitzLog.spec`
* use Microsoft's DebugView to check the runtime errors

# Test
* `pytest`