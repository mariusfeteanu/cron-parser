from pytest import mark, raises

from field_parser import parse_field, Interval, ParsingException, ValidationException


@mark.parametrize('interval, value, expected_parsed_values',[
    # 1
    (Interval.MINUTE, '1', [1]),
    (Interval.HOUR, '1', [1]),
    (Interval.DAY_OF_MONTH, '1', [1]),
    (Interval.MONTH, '1', [1]),
    (Interval.DAY_OF_WEEK, '1', [1]),
    # *
    (Interval.MINUTE, '*', list(range(60))),
    (Interval.HOUR, '*', list(range(24))),
    (Interval.DAY_OF_MONTH, '*', list(range(1, 32))),
    (Interval.MONTH, '*', list(range(1, 13))),
    (Interval.DAY_OF_WEEK, '*', list(range(0, 7))),
    # */5
    (Interval.MINUTE, '*/30', [0, 30]),
    (Interval.HOUR, '*/12', [0, 12]),
    (Interval.DAY_OF_MONTH, '*/10', [10, 20, 30]),
    (Interval.MONTH, '*/4', [4, 8, 12]),
    (Interval.DAY_OF_WEEK, '*/2', [0, 2, 4, 6]),
    # 1-3
    (Interval.MINUTE, '1-3', [1, 2, 3]),
    (Interval.HOUR, '1-3', [1, 2, 3]),
    (Interval.DAY_OF_MONTH, '1-3', [1, 2, 3]),
    (Interval.MONTH, '1-3', [1, 2, 3]),
    (Interval.DAY_OF_WEEK, '1-3', [1, 2, 3]),
    # 1,4,5
    (Interval.MINUTE, '1,4,5', [1, 4, 5]),
    (Interval.HOUR, '1,4,5', [1, 4, 5]),
    (Interval.DAY_OF_MONTH, '1,4,5', [1, 4, 5]),
    (Interval.MONTH, '1,4,5', [1, 4, 5]),
    (Interval.DAY_OF_WEEK, '1,4,5', [1, 4, 5]),
])
def test_parse_field(interval, value, expected_parsed_values):
    parsed_values = parse_field(interval, value)
    assert parsed_values == expected_parsed_values


def test_parse_field_short():
    with raises(ParsingException, match='end of input'):
        parse_field(Interval.MINUTE, "*/")


def test_parse_field_unexpected():
    with raises(ParsingException, match='Could not parse token'):
        parse_field(Interval.MINUTE, "*/-")


def test_parse_field_invalid_value():
    with raises(ValidationException, match='Invalid value'):
        parse_field(Interval.MINUTE, "100")


def test_parse_field_invalid_range():
    with raises(ValidationException, match='Invalid range'):
        parse_field(Interval.MINUTE, "5-1")
