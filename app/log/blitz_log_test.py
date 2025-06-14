import pytest

from app.log.blitz_log import BlitzLog

def test_fromLog_start():
    contents = '''Event	Elapsed	Split	Local	UTC
START	00:00:00	00:00:00	07:59:16 PM	2025-06-12T23:59:16.719551+00:00'''
    log = BlitzLog.fromLog(contents)
    assert log.calcPoints() == 0
    assert log.hasStarted()
    assert log.currentOp() == 1
    assert log.currentMission() == 1
    assert log.nameScreenshot() == 'op1_m1.jpg'

def test_fromLog_fullOp():
    contents = '''Event	Elapsed	Split	Local	UTC
START	00:00:00	00:00:00	08:36:09 PM	2025-06-13T00:36:09.291510+00:00
OP1_M1	00:00:03	00:00:03	08:36:12 PM	2025-06-13T00:36:12.426937+00:00
OP1_M2	00:00:06	00:00:03	08:36:15 PM	2025-06-13T00:36:15.733970+00:00
OP1_M3	00:00:09	00:00:02	08:36:18 PM	2025-06-13T00:36:18.606742+00:00
OP1_SUMM	00:00:11	00:00:02	08:36:21 PM	2025-06-13T00:36:21.284664+00:00
OP2_M1	00:00:15	00:00:03	08:36:24 PM	2025-06-13T00:36:24.602347+00:00'''
    log = BlitzLog.fromLog(contents)
    assert log.calcPoints() == 1
    assert log.hasStarted()
    assert log.currentOp() == 2
    assert log.currentMission() == 2
    assert log.nameScreenshot() == 'op2_m2.jpg'

def test_fromLog_Failed():
    contents = '''Event	Elapsed	Split	Local	UTC
START	00:00:00	00:00:00	08:36:09 PM	2025-06-13T00:36:09.291510+00:00
OP1_M1	00:00:03	00:00:03	08:36:12 PM	2025-06-13T00:36:12.426937+00:00
OP1_M2	00:00:06	00:00:03	08:36:15 PM	2025-06-13T00:36:15.733970+00:00
OP1_M3	00:00:09	00:00:02	08:36:18 PM	2025-06-13T00:36:18.606742+00:00
OP1_SUMM	00:00:11	00:00:02	08:36:21 PM	2025-06-13T00:36:21.284664+00:00
OP2_M1	00:00:15	00:00:03	08:36:24 PM	2025-06-13T00:36:24.602347+00:00
FAILED'''
    log = BlitzLog.fromLog(contents)
    assert log.calcPoints() == 1
    assert log.hasStarted()
    assert log.currentOp() == 2
    assert log.currentMission() == 2
    assert log.nameScreenshot() == 'op2_m2.jpg'

def test_fromLog_Failed_nextMission():
    contents = '''Event	Elapsed	Split	Local	UTC
START	00:00:00	00:00:00	08:53:49 PM	2025-06-13T00:53:49.628466+00:00
OP1_M1	00:00:03	00:00:03	08:53:53 PM	2025-06-13T00:53:53.140422+00:00
OP1_M2	00:00:06	00:00:02	08:53:55 PM	2025-06-13T00:53:55.933041+00:00
OP1_M3	00:00:08	00:00:02	08:53:58 PM	2025-06-13T00:53:58.368112+00:00
OP1_SUMM	00:00:11	00:00:02	08:54:01 PM	2025-06-13T00:54:01.095779+00:00
OP2_M1	00:00:14	00:00:02	08:54:03 PM	2025-06-13T00:54:03.864084+00:00
FAILED
OP3_M1	00:00:21	00:00:07	08:54:10 PM	2025-06-13T00:54:10.895537+00:00'''
    log = BlitzLog.fromLog(contents)
    assert log.calcPoints() == 1
    assert log.hasStarted()
    assert log.currentOp() == 3
    assert log.currentMission() == 2
    assert log.nameScreenshot() == 'op3_m2.jpg'