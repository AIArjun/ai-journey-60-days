import json
import os

TASKS_FILE = os.path.join("day3", "tasks.json")

if os.path.exists(TASKS_FILE):
    try:
        with open(TASKS_FILE, "r") as f:
            tasks = json.load(f)
    except FileNotFoundError:
            tasks = []
else:
    tasks = []
    print("Loaded tasks:", tasks)

def save_tasks():
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f)

def add_task():
    task = input("Enter task: ")
    tasks.append(task)
    save_tasks()
    print("Task added!")

def list_tasks():
    if len(tasks) == 0:
        print("No tasks found.")
    else:
        for index, task in enumerate(tasks, start=1):
            print(index, task)

def show_menu():
    print("\n=== TASK TRACKER ===")
    print("1. Add task")
    print("2. List tasks")
    print("3. Exit")

while True:
    show_menu()
    choice = input("Choose option: ")

    if choice == "1":
        add_task()
    elif choice == "2":
        list_tasks()
    elif choice == "3":
        save_tasks()
        print("Goodbye, Arjun!")
        break
    else:
        print("Invalid choice. Try again")
