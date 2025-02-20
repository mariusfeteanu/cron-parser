from sys import argv

from field_parser import parse_field, Interval
from input_output import parse_args, format_timetable
from model import CronTimeTable


def main():
    cron_spec = parse_args(argv)

    timetable = CronTimeTable(
        minute=parse_field(Interval.MINUTE, cron_spec.minute),
        hour=parse_field(Interval.HOUR, cron_spec.hour),
        day_of_month=parse_field(Interval.DAY_OF_MONTH, cron_spec.day_of_month),
        month=parse_field(Interval.MONTH, cron_spec.month),
        day_of_week=parse_field(Interval.DAY_OF_WEEK, cron_spec.day_of_week),
        command=cron_spec.command)

    timetable_string = format_timetable(timetable)

    print(timetable_string)


if __name__ == "__main__":
    main()
