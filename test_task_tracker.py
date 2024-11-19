import dataclasses
from datetime import datetime
import io
import itertools
import json
import unittest
from unittest.mock import patch, mock_open
import pytest
from task_schema import Task
from json_tasks import TasksJSON
from task_cli import TaskCLI, TaskManager, ManageTasksCLI


@pytest.fixture(name="test_task")
def fixture_test_task():
    now = datetime.now()
    test_task = Task(description="Test task", created_at=now, updated_at=now)
    return test_task


@pytest.fixture(name="reset_id")
def fixture_reset_id():
    Task.id_counter = itertools.count(1)


class TestTaskSchema:
    def test_task_init(self, reset_id, test_task):
        now = test_task.created_at
        assert test_task.description == "Test task"
        assert test_task.created_at == now
        assert test_task.updated_at == now
        assert test_task.status == "todo"
        assert test_task.id == 1

    def test_task_id_incrementation(self, reset_id):
        now = datetime.now()
        test_task1 = Task(description="First task", created_at=now, updated_at=now)
        test_task2 = Task(description="Second task", created_at=now, updated_at=now)

        assert test_task1.id == 1
        assert test_task2.id == 2

    def test_get_last_id(self):
        tasks = [{"id": 1}, {"id": 2}, {"id": 3}]
        Task.get_last_id(tasks)
        now = datetime.now()
        test_task = Task(description="Test task", created_at=now, updated_at=now)

        assert test_task.id == 4


class TestTaskJson:
    def test_json_read(self, test_task):
        test_tasks = [dataclasses.asdict(test_task)]
        test_tasks = json.loads(json.dumps(test_tasks, default=str))
        mocked_open = mock_open(read_data=json.dumps(test_tasks))
        with patch("builtins.open", mocked_open):
            json_tasks = TasksJSON()
            result = json_tasks.json_read()
            assert result == test_tasks

    def test_json_read_file_not_found(self):
        with patch("builtins.open", mock_open()) as mocked_open:
            mocked_open.side_effect = FileNotFoundError
            json_tasks = TasksJSON()
            result = json_tasks.json_read()
            assert result == []

    def test_json_write(self, test_task):
        test_tasks = [dataclasses.asdict(test_task)]
        mocked_open = mock_open()

        with patch("builtins.open", mocked_open):
            json_tasks = TasksJSON()
            json_tasks.json_write(task=test_task)

            mocked_open.assert_any_call(json_tasks.filepath, "r+", encoding="utf-8")
            mocked_open.assert_any_call(json_tasks.filepath, "w", encoding="utf-8")

            handle = mocked_open()
            written_data = "".join(call.args[0] for call in handle.write.call_args_list)
            expected_data = json.dumps(
                test_tasks,
                indent=4,
                sort_keys=True,
                separators=(",", ": "),
                default=str,
                ensure_ascii=False,
            )

            assert written_data == expected_data
            handle.flush.assert_called_once()

    def test_json_print_pretty(self, test_task):
        test_tasks = [dataclasses.asdict(test_task)]
        json_tasks = TasksJSON()
        result = json_tasks.json_print_pretty(test_tasks)
        expected_result = json.dumps(
            test_tasks, indent=4, ensure_ascii=False, default=str
        )
        assert result == expected_result


class TestTaskCLI(unittest.TestCase):
    def setUp(self):
        self.cli = TaskCLI()

    def test_quit(self):
        self.assertTrue(self.cli.do_quit(""))

    def test_postcmd(self):
        self.assertFalse(self.cli.postcmd(False, "test"))
        self.assertTrue(self.cli.postcmd(True, "test"))

    def test_emptyline(self):
        self.assertIsNone(self.cli.emptyline())


class TestTaskManager(unittest.TestCase):
    def setUp(self):
        self.task_manager = TaskManager()

    @patch("json_tasks.TasksJSON.json_read", return_value=[])
    def test_get_last_id(self, mock_json_read):
        self.task_manager.get_last_id()
        self.assertEqual(next(Task.id_counter), 1)

    @patch("json_tasks.TasksJSON.json_write")
    def test_add_task(self, mock_json_write):
        with patch("builtins.open", mock_open()):
            description = "New Task"
            self.task_manager.add_task(description)
            mock_json_write.assert_called()

    @patch(
        "json_tasks.TasksJSON.json_read",
        return_value=[
            {
                "id": 1,
                "description": "Test",
                "status": "todo",
                "created_at": "2024-11-14T12:00:00",
                "updated_at": "2024-11-14T12:00:00",
            }
        ],
    )
    @patch("json_tasks.TasksJSON.json_write")
    def test_update_task(self, mock_json_write, mock_json_read):
        self.task_manager.update_task(1, description="Updated Task")
        mock_json_write.assert_called()

    @patch(
        "json_tasks.TasksJSON.json_read",
        return_value=[
            {
                "id": 1,
                "description": "Test",
                "status": "todo",
                "created_at": "2024-11-14T12:00:00",
                "updated_at": "2024-11-14T12:00:00",
            }
        ],
    )
    @patch("json_tasks.TasksJSON.json_write")
    def test_delete_task(self, mock_json_write, mock_json_read):
        self.task_manager.delete_task(1)
        mock_json_write.assert_called()

    @patch(
        "json_tasks.TasksJSON.json_read",
        return_value=[
            {
                "id": 1,
                "description": "Test",
                "status": "todo",
                "created_at": "2024-11-14T12:00:00",
                "updated_at": "2024-11-14T12:00:00",
            }
        ],
    )
    @patch("json_tasks.TasksJSON.json_write")
    def test_mark_task_in_progress(self, mock_json_write, mock_json_read):
        self.task_manager.mark_task_in_progress(1)
        mock_json_write.assert_called()

    @patch(
        "json_tasks.TasksJSON.json_read",
        return_value=[
            {
                "id": 1,
                "description": "Test",
                "status": "todo",
                "created_at": "2024-11-14T12:00:00",
                "updated_at": "2024-11-14T12:00:00",
            }
        ],
    )
    @patch("json_tasks.TasksJSON.json_write")
    def test_mark_task_done(self, mock_json_write, mock_json_read):
        self.task_manager.mark_task_done(1)
        mock_json_write.assert_called()

    def test_get_index_of_id(self):
        json_data = [
            {"id": 1, "description": "Task 1"},
            {"id": 2, "description": "Task 2"},
            {"id": 3, "description": "Task 3"},
        ]

        index = self.task_manager.get_index_of_id(2, json_data)
        self.assertEqual(index, 1)

        index = self.task_manager.get_index_of_id(4, json_data)
        self.assertEqual(index, 3)

    def test_is_valid_index(self):
        json_data = [
            {"id": 1, "description": "Task 1"},
            {"id": 2, "description": "Task 2"},
            {"id": 3, "description": "Task 3"},
        ]

        valid = self.task_manager.is_valid_index(1, 2, json_data)
        self.assertTrue(valid)

        invalid = self.task_manager.is_valid_index(2, 2, json_data)
        self.assertFalse(invalid)

        invalid = self.task_manager.is_valid_index(3, 4, json_data)
        self.assertFalse(invalid)


class TestManageTasksCLI(unittest.TestCase):
    def setUp(self):
        self.cli = ManageTasksCLI()

    @patch.object(ManageTasksCLI, "do_add")
    def test_do_add(self, mock_do_add):
        self.cli.do_add("Test task")
        mock_do_add.assert_called_with("Test task")

    @patch.object(ManageTasksCLI, "do_update")
    def test_do_update(self, mock_do_update):
        self.cli.do_update("1 New description")
        mock_do_update.assert_called_with("1 New description")

    @patch.object(ManageTasksCLI, "do_delete")
    def test_do_delete(self, mock_do_delete):
        self.cli.do_delete("1")
        mock_do_delete.assert_called_with("1")

    @patch.object(ManageTasksCLI, "do_mark_in_progress")
    def test_do_mark_in_progress(self, mock_do_mark_in_progress):
        self.cli.do_mark_in_progress("1")
        mock_do_mark_in_progress.assert_called_with("1")

    @patch.object(ManageTasksCLI, "do_mark_done")
    def test_do_mark_done(self, mock_do_mark_done):
        self.cli.do_mark_done("1")
        mock_do_mark_done.assert_called_with("1")

    @patch.object(ManageTasksCLI, "do_list")
    def test_do_list(self, mock_do_list):
        self.cli.do_list("")
        mock_do_list.assert_called_with("")

    @patch.object(ManageTasksCLI, "do_list_done")
    def test_do_list_done(self, mock_do_list_done):
        self.cli.do_list_done("")
        mock_do_list_done.assert_called_with("")

    @patch.object(ManageTasksCLI, "do_list_todo")
    def test_do_list_todo(self, mock_do_list_todo):
        self.cli.do_list_todo("")
        mock_do_list_todo.assert_called_with("")

    @patch.object(ManageTasksCLI, "do_list_in_progress")
    def test_do_list_in_progress(self, mock_do_list_in_progress):
        self.cli.do_list_in_progress("")
        mock_do_list_in_progress.assert_called_with("")

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_do_add_no_description(self, mock_stdout):
        self.cli.do_add("")
        self.assertIn(
            "Please, write a description for the task after the 'add' command.",
            mock_stdout.getvalue(),
        )

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_do_update_invalid_id(self, mock_stdout):
        self.cli.do_update("invalid_id New description")
        self.assertIn(
            "The first argument is an id with type int", mock_stdout.getvalue()
        )

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_do_delete_invalid_id(self, mock_stdout):
        self.cli.do_delete("invalid_id")
        self.assertIn("Please, write the integer ID.", mock_stdout.getvalue())

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_do_mark_done_invalid_id(self, mock_stdout):
        self.cli.do_mark_done("invalid_id")
        self.assertIn("Please, write the integer ID.", mock_stdout.getvalue())

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_do_mark_in_progress_invalid_id(self, mock_stdout):
        self.cli.do_mark_in_progress("invalid_id")
        self.assertIn("Please, write the integer ID.", mock_stdout.getvalue())
