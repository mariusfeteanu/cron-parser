from dataclasses import dataclass
from typing import List

from model import CronTimeTable


@dataclass
class CronSpec:
    minute: str
    hour: str
    day_of_month: str
    month: str
    day_of_week: str
    command: str


def parse_args(args: List[str]) -> CronSpec:
    USAGE = 'Usage: python cron_parser.py "*/15 0 1,15 * 1-5 /usr/bin/find"'
    if len(args) != 2:
        raise ValueError(USAGE)

    argument_parts = args[1].split()
    if len(argument_parts) < 6:
        raise ValueError(USAGE)

    return CronSpec(
        minute=argument_parts[0],
        hour=argument_parts[1],
        day_of_month=argument_parts[2],
        month=argument_parts[3],
        day_of_week=argument_parts[4],
        command=' '.join(argument_parts[5:]),
    )


def format_timetable(timetable: CronTimeTable):
    FIELD_WIDTH = 14

    def field2str(name: str, value: List[int]):
        values_as_str = ' '.join([str(val) for val in value])
        return name.ljust(FIELD_WIDTH).replace('_', ' ') + values_as_str + '\n'

    result = field2str('minute', timetable.minute)
    result += field2str('hour', timetable.hour)
    result += field2str('day_of_month', timetable.day_of_month)
    result += field2str('month', timetable.month)
    result += field2str('day_of_week', timetable.day_of_week)
    result += 'command'.ljust(FIELD_WIDTH)
    result += timetable.command

    return result
