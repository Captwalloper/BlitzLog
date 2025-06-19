# Dev Notes
Short and sweet cliffnotes for anyone working with this project. (Probably just versions of future me... hello from the past guys!)
* All commands assume working directory of BlitzLog

## Setup
* get python3
* `pip install -r requirements.txt`

## Run
* `python -m app.app`

## Distribute (Windows only)
* [pyinstaller](https://pyinstaller.org/en/stable/)
* *fresh start only* `pyi-makespec --onefile --windowed --name BlitzLog app.py`
* `pyinstaller --clean BlitzLog.spec`
* use Microsoft's DebugView to check the runtime errors

## Test
* `pytest`

## Task runner
* [invoke](https://www.pyinvoke.org/)
* `invoke --help`
* `invoke --list`
* Examples: `invoke test`, `invoke restore build`
