import bisect
from cmd import Cmd
from datetime import datetime
import shlex
from task_schema import Task
from json_tasks import TasksJSON


class TaskCLI(Cmd):
    prompt = "task-cli "
    intro = "Welcome to TaskCLI. Type 'help' for available commands."

    def do_quit(self, line) -> bool:
        """Quit CLI"""
        print("Bye!")
        return True

    def postcmd(self, stop, line) -> bool:
        print()
        return stop

    def emptyline(self) -> None:
        """Do nothing on empty input line"""
        return None


class TaskManager:
    def __init__(self) -> None:
        self.tasks_json = TasksJSON()
        self.get_last_id()

    def get_last_id(self) -> None:
        json_data: list = self.tasks_json.json_read()
        Task.get_last_id(json_data)

    def add_task(self, description: str) -> None:
        time_create_task: datetime = datetime.now()
        task = Task(
            description=description,
            created_at=time_create_task,
            updated_at=time_create_task,
        )
        self.tasks_json.json_write(task=task)
        print(f"Task added successfully (ID: {task.id})")

    def update_task(
        self, task_id: int, description: str | None = None, status: str | None = None
    ) -> None:
        json_data: list = self.tasks_json.json_read()
        index: int = self.get_index_of_id(task_id, json_data)
        if self.is_valid_index(index, task_id, json_data):
            if description:
                json_data[index]["description"] = description
            if status:
                json_data[index]["status"] = status
            json_data[index]["updated_at"] = datetime.now()
            self.tasks_json.json_write(tasks=json_data)
            print(f"Task with id={task_id} updated successfully.")
        else:
            print(f"No task with id={task_id} was found. Check!")

    def delete_task(self, task_id: int) -> None:
        json_data: list = self.tasks_json.json_read()
        index: int = self.get_index_of_id(task_id, json_data)
        if self.is_valid_index(index, task_id, json_data):
            del json_data[index]
            self.tasks_json.json_write(tasks=json_data)
            print(f"Task with id={task_id} deleted successfully.")
        else:
            print(f"No task with id={task_id} was found. Check!")

    def mark_task_in_progress(self, task_id: int) -> None:
        self.update_task(task_id, status="in-progress")

    def mark_task_done(self, task_id: int) -> None:
        self.update_task(task_id, status="done")

    def get_tasks_by_status(self, status: str | None = None) -> list:
        tasks: list = self.tasks_json.json_read()
        if status:
            return [task for task in tasks if task.get("status") == status]
        return tasks

    def get_index_of_id(self, target_id: int, json_data: list) -> int:
        ids: list = [task["id"] for task in json_data]
        index: int = bisect.bisect_left(ids, target_id)
        return index

    def is_valid_index(self, index: int, task_id: int, json_data: list) -> bool:
        return index < len(json_data) and json_data[index]["id"] == task_id


class ManageTasksCLI(TaskCLI):
    def __init__(self) -> None:
        super().__init__()
        self.task_manager = TaskManager()

    def do_add(self, line: str) -> None:
        """Adding a task description\nExample: add My first task"""
        try:
            if line:
                self.task_manager.add_task(line)
            else:
                print(
                    "Please, write a description for the task after the 'add' command."
                )
        except Exception as e:
            print(e)

    def do_update(self, line: str) -> None:
        """Updating the task description by ID\nExample: update 1 New description"""
        try:
            args: list[str] = shlex.split(line)
            if len(args) < 2:
                print(
                    "Please, write the id and a description "
                    "for the task after the 'update' command."
                )
            else:
                task_id = int(args[0])
                new_description: str = " ".join(args[1:])
                self.task_manager.update_task(task_id, description=new_description)
        except ValueError as ve:
            print(
                "The first argument is an id with type int, "
                "the second argument is a description."
            )
            print(ve)
        except Exception as e:
            print(e)

    def do_delete(self, line: int) -> None:
        """Deleting a task by ID\nExample: delete 1"""
        try:
            task_id = int(line)
            self.task_manager.delete_task(task_id)
        except ValueError as ve:
            print("Please, write the integer ID.")
            print(ve)
        except Exception as e:
            print(e)

    def do_mark_in_progress(self, line: int) -> None:
        """Marking a task as in-progress by ID\nExample: mark_in_progress 1"""
        try:
            task_id = int(line)
            self.task_manager.mark_task_in_progress(task_id)
        except ValueError as ve:
            print("Please, write the integer ID.")
            print(ve)
        except Exception as e:
            print(e)

    def do_mark_done(self, line: int) -> None:
        """Marking a task as done by ID\nExample: mark_done 1"""
        try:
            task_id = int(line)
            self.task_manager.mark_task_done(task_id)
        except ValueError as ve:
            print("Please, write the integer ID.")
            print(ve)
        except Exception as e:
            print(e)

    def do_list(self, line: str) -> None:
        """Get a list of tasks"""
        tasks: list = self.task_manager.get_tasks_by_status()
        output: str = self.task_manager.tasks_json.json_print_pretty(tasks)
        print(output)

    def do_list_done(self, line: str) -> None:
        """Get a list of done tasks"""
        done_tasks: list = self.task_manager.get_tasks_by_status("done")
        output: str = self.task_manager.tasks_json.json_print_pretty(done_tasks)
        print(output)

    def do_list_todo(self, line: str) -> None:
        """Get a list of todo tasks"""
        todo_tasks: list = self.task_manager.get_tasks_by_status("todo")
        output: str = self.task_manager.tasks_json.json_print_pretty(todo_tasks)
        print(output)

    def do_list_in_progress(self, line: str) -> None:
        """Get a list of in-progress tasks"""
        in_progress_tasks: list = self.task_manager.get_tasks_by_status("in-progress")
        output: str = self.task_manager.tasks_json.json_print_pretty(in_progress_tasks)
        print(output)


if __name__ == "__main__":
    ManageTasksCLI().cmdloop()
