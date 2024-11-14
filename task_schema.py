from dataclasses import dataclass, field
from datetime import datetime
import itertools


@dataclass
class Task:
    description: str
    created_at: datetime
    updated_at: datetime
    id: int = field(default_factory=lambda: next(Task.id_counter), init=False)
    status: str = "todo"

    id_counter = itertools.count(1)

    @classmethod
    def get_last_id(cls, tasks: list) -> None:
        if tasks:
            last_id = max((task["id"]) for task in tasks)
        else:
            last_id = 0
        cls.id_counter = itertools.count(last_id + 1)
