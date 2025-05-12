import argparse
import json
import os
from datetime import datetime

TASKS_FILE = "tasks.json"

class TaskManager:
    def __init__(self, file_name="tasks.json"):
        self.file_name = file_name

    def load_tasks(self):
        if not os.path.exists(self.file_name):
            return []
        try:
            with open(self.file_name, "r") as file:
                content = file.read()
                if not content.strip():  # Проверяем, что файл не пустой
                    return []
                return json.loads(content)  # Используем json.loads для явной обработки строки
        except json.JSONDecodeError:
            print("Error: The tasks file is corrupted or contains invalid JSON.")
            return []

    def save_tasks(self, tasks):
        with open(self.file_name, "w") as file:
            json.dump(tasks, file, indent=4)

    def add_task(self, description):
        tasks = self.load_tasks()
        if tasks:  # Если список задач не пустой
            max_id = max(task["id"] for task in tasks)  # Находим максимальный id
        else:
            max_id = 0  # Если задач нет, начинаем с 0

        new_task = {
            "id": max_id + 1,
            "description": description,
            "status": "todo",
            "createdAt": datetime.now().isoformat(),
            "updatedAt": datetime.now().isoformat()
        }
        tasks.append(new_task)
        self.save_tasks(tasks)
        print(f"Task added successfully (ID: {new_task['id']})")

    def update_task(self, task_id, new_description):
        tasks = self.load_tasks()
        for task in tasks:
            if task["id"] == task_id:
                task["description"] = new_description
                task["updatedAt"] = datetime.now().isoformat()
                self.save_tasks(tasks)
                print(f"Task {task_id} updated successfully")
                return
        print(f"Task with ID {task_id} not found")

    def delete_task(self, task_id):
        tasks = self.load_tasks()
        for i, task in enumerate(tasks):
            if task["id"] == task_id:
                deleted_task = tasks.pop(i)  # Удаляем задачу из списка
                self.save_tasks(tasks)
                print(f"Task {task_id} deleted successfully")
                return
        print(f"Task with ID {task_id} not found")

    def mark_in_progress_task(self, task_id):
        tasks = self.load_tasks()
        for task in tasks:
            if task["id"] == task_id:
                task["status"] = "in-progress"
                self.save_tasks(tasks)
                print(f"Task {task_id} in-progress")
                return
        print(f"Task with ID {task_id} not found")

    def mark_done_task(self, task_id):
        tasks = self.load_tasks()
        for task in tasks:
            if task["id"] == task_id:
                task["status"] = "done"
                self.save_tasks(tasks)
                print(f"Task {task_id} done")
                return
        print(f"Task with ID {task_id} not found")

    def list_tasks(self, status=None):
        tasks = self.load_tasks()
        if not tasks:
            print("No tasks found.")
            return

        filtered_tasks = tasks
        if status:
            filtered_tasks = [task for task in tasks if task["status"] == status]

        if not filtered_tasks:
            print(f"No tasks with status '{status}' found.")
            return

        for task in filtered_tasks:
            print(f"ID: {task['id']}")
            print(f"Description: {task['description']}")
            print(f"Status: {task['status']}")
            print(f"Created At: {task['createdAt']}")
            print(f"Updated At: {task['updatedAt']}")
            print("-" * 30)

# Настройка парсера argparse
parser = argparse.ArgumentParser(description="Task Tracker CLI")
subparsers = parser.add_subparsers(dest="command")

# Add command
add_parser = subparsers.add_parser("add", help="Add a new task")
add_parser.add_argument("description", type=str, help="Task description")

# Update command
update_parser = subparsers.add_parser("update", help="Update a task")
update_parser.add_argument("id", type=int, help="Task ID")
update_parser.add_argument("description", type=str, help="New task description")

# Delete command
delete_parser = subparsers.add_parser("delete", help="Delete a task")
delete_parser.add_argument("id", type=int, help="Task ID")

# Mark-in-progress command
mark_in_progress_parser = subparsers.add_parser("mark-in-progress", help="Task in-progress")
mark_in_progress_parser.add_argument("id", type=int, help="Task ID")

# Mark-done command
mark_done_parser = subparsers.add_parser("mark-done", help="Task done")
mark_done_parser.add_argument("id", type=int, help="Task ID")

# List-tasks command
list_parser = subparsers.add_parser("list", help="List tasks")
list_parser.add_argument("status", nargs="?", choices=["todo", "in-progress", "done"], help="Filter tasks by status")

# Parse arguments
args = parser.parse_args()

# Создаем экземпляр класса
manager = TaskManager()

if args.command == "add":
    manager.add_task(args.description)

elif args.command == "update":
    manager.update_task(args.id, args.description)

elif args.command == "delete":
    manager.delete_task(args.id)

elif args.command == "mark-in-progress":
    manager.mark_in_progress_task(args.id)

elif args.command == "mark-done":
    manager.mark_done_task(args.id)

elif args.command == "list":
    manager.list_tasks(args.status)