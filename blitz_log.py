from typing import List
from time_stamper import TimeStamper as TS


class BlitzLog:
    def __init__(self):
        self.startTimeLocal = ''
        self.startTimeUtcIso = ''
        self.operations: List[Operation] = []
        self.currentOp = 0
        self.currentMission = 0
        self.beginNewOp()
        self.errorMessages: List[str] = []

    def calcPoints(self):
        points = 0
        for op in self.operations:
            points += (3 if op.completed() else 0)
        return points
    
    def hasStarted(self):
        return self.startTimeUtcIso != ''
    
    def start(self):
        self.startTimeUtcIso = TS.utc()
        self.startTimeLocal = TS.local()

    def beginNewOp(self):
        self.operations.append(Operation())
        self.currentOp += 1
        self.currentMission = 1

    def completeMission(self, secondsElapsed):
        self.operations[-1].missions.append(f'OP{self.currentOp} M{self.currentMission} {TS.stamp(secondsElapsed)}')
        if (self.currentMission < 3):
            self.currentMission += 1
        else:
            self.beginNewOp()

    def failMission(self, secondsElapsed):
        self.operations[-1].missions.append(f'OP{self.currentOp} M{self.currentMission} {TS.stamp(secondsElapsed)}')
        self.operations[-1].failed = True
        self.beginNewOp()

    def toLog(self):
        if (not self.hasStarted()):
            return ''
        lines: List[str] = [f'START {TS.stamp(0)}']
        for op in self.operations:
            lines.extend(op.toLines())
        return "\n".join(lines)
    
    def fromLog(self, contents: str):
        log = BlitzLog()
        lines = contents.splitlines()
        if (not lines.count >= 1 and lines[0].startswith('START')):
            return log
        startLineTokens = lines[0].split(' ')
        if (startLineTokens != 4):
            log.errorMessages.append(f'Invalid startline, expected 3 segements (START, T, local, utc), found {startLineTokens.count}')
            return log
        log.startTimeLocal = startLineTokens[2]
        log.startTimeUtcIso = startLineTokens[3]
        # todo OPs
        return log


class Operation:
    def __init__(self):
        self.missions: List[str] = []
        self.failed = False

    def toLines(self):
        lines: List[str] = self.missions.copy()
        if (self.failed):
            lines.append('FAILED')
        return lines
    
    def completed(self):
        return len(self.missions) == 3 and not self.failed


        
