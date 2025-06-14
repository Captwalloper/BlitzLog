from enum import Enum

_ICON = 'assets/icons/'
class Icon(str, Enum):
    blitz = _ICON +  'blitz.png'
    op = _ICON +     'op.svg'
    steam = _ICON +  'steam.png'