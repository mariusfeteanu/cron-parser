from typing import List, Tuple
from dataclasses import dataclass
from enum import Enum

from field_tokenizer import tokenize, TokenType, Token, token_types
from input_output import CronSpec


class ParsingException(Exception):
    pass


class ValidationException(Exception):
    pass


class Interval(Enum):
    MINUTE = (0, 59)
    HOUR = (0, 23)
    DAY_OF_MONTH = (1, 31)
    MONTH = (1, 12)
    DAY_OF_WEEK = (0, 6)


class StateTransition:
    def __init__(self, token_type, next_state):
        self.token_type: TokenType = token_type
        self.next_state: State = next_state


class State:
    def __init__(self, name, transitions = None, allow_stop = False):
        if transitions is None:
            transitions = []
        self.transitions: List[StateTransition] = transitions
        self.allow_stop: bool = allow_stop
        self.name = name
    
    def add(self, token_type, next_state):
        self.transitions.append(
            StateTransition(token_type, next_state)
        )
    
    def __repr__(self):  # pragma: no cover
        return self.name

START = State('START')
ALL = State('ALL', allow_stop=True)
RANGE = State('RANGE')
RANGE_NUMBER = State('RANGE_NUMBER', allow_stop=True)
NUMBER = State('NUMBER', allow_stop=True)
LIST = State('LIST')
LIST_NUMBER = State('LIST_NUMBER', allow_stop=True)
STEP = State('STEP')
STEP_NUMBER = State('STEP_NUMBER', allow_stop=True)

# *
START.add(TokenType.ALL, ALL)

START.add(TokenType.NUMBER, NUMBER)

# 1-3
NUMBER.add(TokenType.RANGE_SEP, RANGE)
RANGE.add(TokenType.NUMBER, RANGE_NUMBER)

# */5
ALL.add(TokenType.STEP_SEP, STEP)
STEP.add(TokenType.NUMBER, STEP_NUMBER)

# 1,2,3
NUMBER.add(TokenType.LIST_SEP, LIST)
LIST.add(TokenType.NUMBER, LIST_NUMBER)
LIST_NUMBER.add(TokenType.LIST_SEP, LIST)


def machine(
    state: State,
    input: List[Token],
    collected_params: List[str] = None
    ) -> Tuple[State, List[str]]:
    VALUE_TOKEN_TYPES = [TokenType.NUMBER]

    if collected_params is None:
        collected_params = []

    if not input:  # end of input
        if state.allow_stop:
            return state, collected_params
        else:
            raise ParsingException(f'end of input in non-final state: {state}'
                                   f', parsed input {collected_params}')
    
    token = input[0]
    remaining_input = input[1:]

    for transition in state.transitions:
        if token.token_type == transition.token_type:
            next_state = transition.next_state
            
            if token.token_type in VALUE_TOKEN_TYPES:
                next_params = collected_params + [token.value]
            else:
                next_params = collected_params
            
            return machine(next_state, remaining_input, next_params)
    
    raise ParsingException(f'Could not parse token "{token.value}" in state {state}')


def interval_range(interval: Interval) -> List[int]:
    start, end = interval.value
    return list(range(start, end+1))


def validate_value(interval: Interval, value: int):
    if value < interval.value[0] or value > interval.value[1]:
        raise ValidationException(
            f'Invalid value "{value}" for field {interval.name}, must be in {interval.value}')


def validate_range(interval: Interval, start: int, end: int):
    validate_value(interval, start)
    validate_value(interval, end)
    if end < start:
        raise ValidationException(
            f'Invalid range ({start}, {end}), end ({end}) is before start ({start}) in field {interval.name}')


def parse_field(interval: Interval, value: str) -> List[int]:
    tokens = tokenize(value)

    final_state, params = machine(START, tokens)

    if final_state == NUMBER:
        v = int(params[0])
        validate_value(interval, v)
        return [v]
    elif final_state == ALL:
        return interval_range(interval)
    elif final_state == STEP_NUMBER:
        all_times = interval_range(interval)
        step = int(params[0])
        validate_value(interval, step)
        return [t for t in all_times if t % step == 0]
    elif final_state == RANGE_NUMBER:
        all_times = interval_range(interval)
        start = int(params[0])
        end = int(params[1])
        validate_range(interval, start, end)
        return [t for t in all_times if start <= t <= end]
    elif final_state == LIST_NUMBER:
        all_times = interval_range(interval)
        selected_times = [int(p) for p in params]
        for st in selected_times:
            validate_value(interval, st)
        return [t for t in all_times if t in selected_times]
    else:  # pragma: no cover
        raise ParsingException(f'Unable to parse final state: {final_state} with params {params}')
