import datetime

class TimeStamper:
    @staticmethod
    def stamp(timeSinceStartInSeconds: str):
        utcnow = datetime.datetime.utcnow()
        now = datetime.datetime.now()
        return f'T+{str(datetime.timedelta(seconds=timeSinceStartInSeconds))} Local: {TimeStamper.local()} UTC: {TimeStamper.utc()}'
    
    @staticmethod
    def utc():
        return datetime.datetime.utcnow().isoformat()
    
    @staticmethod
    def local():
        return datetime.datetime.now().strftime("%I:%M %p")