import dataclasses
import json
import os
from task_schema import Task


class TasksJSON:

    def __init__(self) -> None:
        self.filepath = os.path.join(os.path.dirname(__file__), "tasks.json")

    def json_read(self) -> list:
        try:
            with open(self.filepath, "r+", encoding="utf-8") as openfile:
                return json.load(openfile)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            return []

    def json_write(self, task: Task | None = None, tasks: list | None = None) -> None:
        if tasks is None:
            tasks = self.json_read()
        if task is not None:
            task_dict: dict = dataclasses.asdict(task)
            tasks.append(task_dict)
        with open(self.filepath, "w", encoding="utf-8") as outfile:
            json.dump(
                tasks,
                outfile,
                indent=4,
                sort_keys=True,
                separators=(",", ": "),
                default=str,
                ensure_ascii=False,
            )
            outfile.flush()

    def json_print_pretty(self, tasks: list) -> str:
        return json.dumps(tasks, indent=4, ensure_ascii=False, default=str)
