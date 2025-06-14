import pytest
from datetime import datetime, timedelta

from app.time.time_stamper import TimeStamper

@pytest.fixture
def startUtcIso():
    return '2025-06-12T23:26:53.675796+00:00'

@pytest.fixture
def ts(startUtcIso):
    return TimeStamper(startUtcIso)

def test_pretty_print():
    assert TimeStamper.prettyPrint(timedelta(days=2, hours=1, minutes=59, seconds=59)) == '49:59:59'

def test_stamp(startUtcIso, ts):
    now = datetime.fromisoformat(startUtcIso) + timedelta(hours=99, minutes=59, seconds=59)
    assert ts.stamp(now, now) == '99:59:59\t00:00:00\t11:26:52 PM\t2025-06-17T03:26:52.675796+00:00'

def test_startUtc(startUtcIso, ts):
    assert ts.startUtc().isoformat() == startUtcIso

def test_startStamp(ts):
    assert ts.startStamp() == '00:00:00\t00:00:00\t07:26:53 PM\t2025-06-12T23:26:53.675796+00:00'