from dataclasses import dataclass
from typing import List


@dataclass
class CronTimeTable:
    minute: List[int]
    hour: List[int]
    day_of_month: List[int]
    month: List[int]
    day_of_week: List[int]
    command: str
