# Project Overview
**task-tracker-cli** is a command-line interface (CLI) application designed to manage and track tasks effectively. It allows users to add, update, delete, and mark tasks, as well as list tasks based on their status. The application uses a JSON file for persistent storage of task data.

# Features
- **Add a Task**: Add new tasks to your task list with a description.
- **Update a Task**: Update the description of an existing task.
- **Delete a Task**: Remove a task from your list.
- **Mark a Task**: Change the status of a task to "in progress" or "done".
- **List Tasks**: Display all tasks or filter tasks based on their status (done, in-progress, todo).

# Task Properties
Each task has the following properties:
- **id**: Unique identifier for the task.
- **description**: Short description of the task.
- **status**: Status of the task (todo, in-progress, done).
- **createdAt**: Date and time when the task was created.
- **updatedAt**: Date and time when the task was last updated.

# How to Run
To run the TaskTrackerCLI application, follow these steps:
1. **Clone the repository:**
``` bash
git clone git@github.com:Zo2Be/task-tracker-CLI.git
```

2. **Navigate into the project directory:**
``` bash
cd task-tracker-CLI
```
3. **Run the CLI application:**
``` bash
python task_cli.py
```

4. **Use the available commands (see below)**

# Commands and Usage
## Adding a Task
``` python
task-cli add "Buy groceries"
# Output: Task added successfully (ID: 1)
```

## Updating a Task
``` python
task-cli update 1 "Buy groceries and cook dinner"
# Output: Task with id=1 updated successfully.
```

## Deleting a Task
``` python
task-cli delete 1
# Output: Task with id=1 deleted successfully.
```

## Marking a Task as In Progress
``` python
task-cli mark-in-progress 1
# Output: Task with id=1 marked as in progress.
```

## Marking a Task as Done
``` python
task-cli mark-done 1
# Output: Task with id=1 marked as done.
```

## Listing All Tasks
``` python
task-cli list
# Output: List of all tasks in JSON format.
```

## Listing Tasks by Status
``` python
task-cli list done
# Output: List of all tasks marked as done.

task-cli list todo
# Output: List of all tasks marked as todo.

task-cli list in-progress
# Output: List of all tasks marked as in progress.
```
# Implementation Details
## Modules
1. **task_schema.py**
- Defines the Task dataclass with properties id, description, status, createdAt, and updatedAt.
- Manages task ID generation.

2. **json_tasks.py**
- Handles reading from and writing to the JSON file.
- Contains methods for pretty-printing the tasks in JSON format.

3. **task_cli.py**
- Implements the CLI commands using the cmd module.
- Defines the TaskManager class for managing task operations.
- Contains command methods for adding, updating, deleting, marking, and listing tasks.

4. **test_task_tracker.py**
- Contains tests for the various modules and functionalities of the application.

---
Sample solution for the [task-tracker](https://roadmap.sh/projects/task-tracker) challenge from [roadmap.sh](https://roadmap.sh).
