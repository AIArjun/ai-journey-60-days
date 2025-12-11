tasks = [
    "Read file using read()",
    "Count lines using readlines()",
    "Loop over lines",
    "Search for a word",
    "Learn write() and append()"
]
with open("task_list.txt", "w") as f:
    for task in tasks:
        f.write(task + "\n")