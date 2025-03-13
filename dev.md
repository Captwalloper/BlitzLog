# Setup
* get python3
* `pip install -r requirements.txt`

# Run
* `python app.py`

# Distribute (Windows only)
* [pyinstaller](https://pyinstaller.org/en/stable/)
* `pyi-makespec --onefile --windowed --name BlitzLog app.py`
* `pyinstaller --clean BlitzLog.spec`