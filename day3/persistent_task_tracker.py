import json
import os

# File location for saving tasks
TASK_FILE = "tasks.json"


# -----------------------------
# Load tasks from JSON file
# -----------------------------
def load_tasks():
    # If file does not exist → return empty list
    if not os.path.exists(TASK_FILE):
        return [], 1   # return tasks list & next_id

    with open(TASK_FILE, "r") as f:
        tasks = json.load(f)

    # Determine the next ID
    if len(tasks) == 0:
        next_id = 1
    else:
        next_id = max(task["id"] for task in tasks) + 1

    return tasks, next_id


# -----------------------------
# Save tasks into JSON file
# -----------------------------
def save_tasks(tasks):
    with open(TASK_FILE, "w") as f:
        json.dump(tasks, f, indent=4)
    print("Tasks saved successfully.")


# -----------------------------
# Show menu
# -----------------------------
def show_menu():
    print("\n=== TASK TRACKER (Persistent) ===")
    print("1. Add task")
    print("2. List tasks")
    print("3. Exit")


# -----------------------------
# Add a new task
# -----------------------------
def add_task(tasks, next_id):
    title = input("Enter task title: ").strip()

    if title == "":
        print("Task title cannot be empty.")
        return next_id

    task = {
        "id": next_id,
        "title": title,
        "done": False
    }

    tasks.append(task)
    print(f"Task added with ID {next_id}")

    return next_id + 1


# -----------------------------
# List all tasks
# -----------------------------
def list_tasks(tasks):
    if not tasks:
        print("No tasks available.")
        return

    print("\nYour Tasks:")
    for task in tasks:
        status = "✔" if task["done"] else "✘"
        print(f"{task['id']}. {task['title']} [{status}]")


# -----------------------------
# Main loop
# -----------------------------
def main():
    tasks, next_id = load_tasks()

    while True:
        show_menu()
        choice = input("Choose an option (1/2/3): ").strip()

        if choice == "1":
            next_id = add_task(tasks, next_id)

        elif choice == "2":
            list_tasks(tasks)

        elif choice == "3":
            save_tasks(tasks)
            print("Exiting program. Goodbye!")
            break

        else:
            print("Invalid option. Please choose 1, 2, or 3.")


# -----------------------------
# Entry point
# -----------------------------
if __name__ == "__main__":
    main()
