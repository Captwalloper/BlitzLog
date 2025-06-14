from __future__ import annotations
from typing import List
from app.time.time_stamper import TimeStamper as TS
from app.util import alert

class BlitzLog:
    def __init__(self):
        self.operations: List[Operation] = []
        self.beginNewOp()
        self.TS = TS()

    def currentOp(self):
        return len(self.operations)
    
    def currentMission(self):
        return 0 if self.currentOp() == 0 else len(self.operations[-1].missions) + 1

    def calcPoints(self):
        points = 0
        for op in self.operations:
            points += (1 if op.completed() else 0)
        return points
    
    def hasStarted(self):
        return self.TS.startUtc() != None
    
    def start(self, startUtcIso: str = None):
        self.TS.start(startUtcIso)

    def beginNewOp(self):
        self.operations.append(Operation())

    def completeMission(self):
        op = self.operations[-1]
        if (self.currentMission() < 4):
            op.missions.append(f'OP{self.currentOp()}_M{self.currentMission()}\t{self.TS.stamp()}')
        else:
            op.missions.append(f'OP{self.currentOp()}_SUMM\t{self.TS.stamp()}')
            self.beginNewOp()

    def failLastMission(self):
        # failed mission previously assumed as successful
        if (self.currentMission() > 1):
            self.operations[-1].failed = True
            self.beginNewOp()
        elif (self.currentOp() > 1):
            self.operations[-2].failed = True

    def nameScreenshot(self):
        op = self.currentOp()
        m = self.currentMission()
        return f'op{op}_m{m}.jpg' if m < 4 else f'op{op}_summary.jpg'
    
    def overwriteFrom(self, log: BlitzLog):
        self.operations.clear()
        self.operations.extend(log.operations)
        self.TS.start(log.TS.startUtc().isoformat())

    def toLog(self):
        if (not self.hasStarted()):
            return ''
        lines: List[str] = [
            'Event\tElapsed\tSplit\tLocal\tUTC',
            f'START\t{self.TS.startStamp()}'
        ]
        for op in self.operations:
            lines.extend(op.toLines())
        return "\n".join(lines)
    
    @staticmethod
    def fromLog(contents: str):
        log = BlitzLog()
        log.operations.clear()
        lines = contents.splitlines()
        opNum = 1
        i = 1
        while i < len(lines):
            if (i == 1):
                # Start
                if (not len(lines) >= 2 and lines[i].startswith('START')):
                    return log
                startLineTokens = lines[i].split('\t')
                if (len(startLineTokens) != 5):
                    tokens = '\n'.join(startLineTokens)
                    alert(f'Invalid startline, expected 4 segements (START, T, local, utc), found:\n{tokens}')
                    return log
                log.start(startLineTokens[4].removeprefix('UTC: '))
            else:
                # OPs
                k = i
                opLines: List[str] = []
                while (k < len(lines) and (lines[k].startswith(f"OP{opNum}") or lines[k].startswith('FAILED'))):
                    opLines.append(lines[k])
                    k += 1
                if (len(opLines) > 0):
                    op = Operation.fromLines(opLines)
                    log.operations.append(op)
                    opNum += 1
                i = k - 1
            i += 1
        if (len(log.operations) < 1):
            log.beginNewOp()
        return log
    
class Operation:
    def __init__(self):
        self.missions: List[str] = []
        self.failed = False
        self.startUtc = TS.utc()

    def completed(self):
        return len(self.missions) > 2 and not self.failed

    def toLines(self):
        lines: List[str] = self.missions.copy()
        if (self.failed):
            lines.append('FAILED')
        return lines
    
    @staticmethod
    def fromLines(lines: List[str]):
        op = Operation()
        for line in lines:
            if (line.startswith('FAILED')):
                op.failed = True
            elif (line.startswith('OP')):
                op.missions.append(line)
            else:
                opLines = '\n'.join(lines)
                alert(f"Failed to parse operation from:\n{opLines}")
                break
        return op

