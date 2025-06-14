from datetime import datetime, timedelta
from dateutil import tz

from app.util import alert
    
class TimeStamper:
    def __init__(self, startUtcIso: str = None):
        self.__startUtcIso = startUtcIso
        self.__lastUtc = self.startUtc()

    def stamp(self, nowUtc: datetime = None, splitUtc: datetime = None):
        startUtc = self.startUtc()
        lastUtc = self.__lastUtc if splitUtc == None else splitUtc
        nowUtc = nowUtc if nowUtc != None else TimeStamper.utc()
        nowUtcIso = nowUtc.isoformat()
        if (startUtc != nowUtc):
            self.__lastUtc = nowUtc
        return f'{TimeStamper.prettyPrint(nowUtc - startUtc)}\t{TimeStamper.prettyPrint(nowUtc - lastUtc)}\t{TimeStamper.local(nowUtc).strftime("%I:%M:%S %p")}\t{nowUtcIso}'
    
    def start(self, startUtcIso: str = None):
        self.__startUtcIso = startUtcIso if startUtcIso != None else TimeStamper.utc().isoformat()
        self.__lastUtc = datetime.fromisoformat(self.__startUtcIso)
    
    def startUtc(self):
        return datetime.fromisoformat(self.__startUtcIso) if self.__startUtcIso != None else None
    
    def startStamp(self):
        return self.stamp(self.startUtc(), self.startUtc())
    
    @staticmethod
    def utc():
        return datetime.now(tz=tz.tzutc())
    
    @staticmethod
    def local(utc: datetime = None):
        return (utc or TimeStamper.utc()).astimezone(tz.tzlocal())
    
    @staticmethod
    def prettyPrint(elapsed: timedelta):
        total_seconds = int(elapsed.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)