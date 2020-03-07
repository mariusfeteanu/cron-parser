from pytest import raises

from input_output import parse_args, format_timetable
from model import CronTimeTable


def test_parse_args():
    args = ['cron_parser.py', '*/15 0 1,2 * 1-5 /usr/bin/find']
    cron_spec = parse_args(args)
    assert cron_spec.command == '/usr/bin/find'
    assert cron_spec.minute == '*/15'
    assert cron_spec.hour == '0'
    assert cron_spec.day_of_month == '1,2'
    assert cron_spec.month == '*'
    assert cron_spec.day_of_week == '1-5'


def test_format_timetable():
    timetable = CronTimeTable(
        minute = [0, 15, 30, 45],
        hour = [0],
        day_of_month = [1, 2],
        month = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        day_of_week = [1, 2, 3, 4, 5],
        command = '/usr/bin/find'
    )
    result = format_timetable(timetable)
    expected_result = """
minute        0 15 30 45
hour          0
day of month  1 2
month         1 2 3 4 5 6 7 8 9 10 11 12
day of week   1 2 3 4 5
command       /usr/bin/find
""".strip()
    assert result == expected_result


def test_parse_args_error_argcount():
    with raises(ValueError):
        args = ['cron_parser.py', '*/15 0 1,2 * 1-5 /usr/bin/find', '--help']
        cron_spec = parse_args(args)


def test_parse_args_error_cron_spec():
    with raises(ValueError):
        args = ['cron_parser.py', '*/15 0 1,2 * 1-5 * /usr/bin/find']
        cron_spec = parse_args(args)

    with raises(ValueError):
        args = ['cron_parser.py', '*/15 0 1,2 * /usr/bin/find']
        cron_spec = parse_args(args)
