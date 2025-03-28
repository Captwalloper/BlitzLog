from datetime import datetime
from dateutil import tz
    
class TimeStamper:
    def __init__(self, startUtcIso: str):
        self.startUtcIso = startUtcIso

    def stamp(self, nowUtcIso: str = None):
        nowUtc = datetime.fromisoformat(nowUtcIso) if nowUtcIso != None else datetime.now(tz=tz.tzutc())
        nowUtcIso = nowUtc.isoformat()
        return f'T+{str(nowUtc - self.startUtc())}\tLocal: {TimeStamper.local(nowUtc).strftime("%I:%M %p")}\tUTC: {nowUtcIso}'
    
    def startUtc(self):
        return datetime.fromisoformat(self.startUtcIso)

    @staticmethod
    def utc():
        return datetime.now(tz=tz.tzutc())
    
    @staticmethod
    def local(utc: datetime = None):
        return (utc or datetime.now()).astimezone(tz.tzlocal())