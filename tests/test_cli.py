from rcpack import cli
from datetime import datetime, timedelta
import io
import sys


def test_log_verbose_when_enabled():
    captured_output = io.StringIO()
    original_stderr = sys.stderr
    sys.stderr = captured_output
    
    try:
        # log_verbose should print to stderr when verbose=True
        cli.log_verbose("test message", verbose=True)
        output = captured_output.getvalue()
        assert "test message" in output
    finally:
        sys.stderr = original_stderr


def test_log_verbose_when_disabled():
    captured_output = io.StringIO()
    original_stderr = sys.stderr
    sys.stderr = captured_output
    
    try:
        # log_verbose should NOT print when verbose=False
        cli.log_verbose("test message", verbose=False)
        output = captured_output.getvalue()
        assert output == ""
    finally:
        sys.stderr = original_stderr


def test_human_readable_age_just_now():
    recent_time = datetime.now() - timedelta(seconds=30)
    assert cli.human_readable_age(recent_time) == "just now"


def test_human_readable_age_minutes():
    minutes_ago = datetime.now() - timedelta(minutes=5)
    result = cli.human_readable_age(minutes_ago)
    assert "minute" in result
    assert "5" in result


def test_human_readable_age_hours():
    hours_ago = datetime.now() - timedelta(hours=3)
    result = cli.human_readable_age(hours_ago)
    assert "hour" in result
    assert "3" in result


def test_human_readable_age_days():
    days_ago = datetime.now() - timedelta(days=2)
    result = cli.human_readable_age(days_ago)
    assert "day" in result
    assert "2" in result


def test_human_readable_age_singular_day():
    one_day_ago = datetime.now() - timedelta(days=1)
    result = cli.human_readable_age(one_day_ago)
    assert result == "1 day ago"


def test_human_readable_age_singular_hour():
    one_hour_ago = datetime.now() - timedelta(hours=1, minutes=0)
    result = cli.human_readable_age(one_hour_ago)
    assert result == "1 hour ago"
