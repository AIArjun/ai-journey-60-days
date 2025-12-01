# day2/task_tracker.py

# Each task will look like:
# {"id": 1, "title": "Learn Python", "done": False}

def show_menu():
    print("\n=== TASK TRACKER ===")
    print("1. Add task")
    print("2. List tasks")
    print("3. Exit")


def add_task(tasks, next_id):
    """Ask user for a task title and add it to the list."""
    title = input("Enter task title: ").strip()

    if title == "":
        print("Task title cannot be empty.")
        return next_id  # id does not change

    task = {
        "id": next_id,
        "title": title,
        "done": False
    }

    tasks.append(task)
    print(f"Task added with id {next_id}")
    return next_id + 1  # next available id


def list_tasks(tasks):
    """Print all tasks in a readable way."""
    if not tasks:
        print("No tasks yet.")
        return

    print("\nYour tasks:")
    for task in tasks:
        status = "✓" if task["done"] else "✗"
        print(f"[{status}] {task['id']}: {task['title']}")


def main():
    tasks = []      # list to store all task dictionaries
    next_id = 1     # id for the next new task

    while True:
        show_menu()
        choice = input("Choose an option (1/2/3): ").strip()

        if choice == "1":
            next_id = add_task(tasks, next_id)

        elif choice == "2":
            list_tasks(tasks)

        elif choice == "3":
            print("Exiting Task Tracker. Bye!")
            break

        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()
