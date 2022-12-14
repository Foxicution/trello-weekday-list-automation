from typing import NamedTuple
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


class Info(NamedTuple):
    day_index: int
    name: str
    id: str
