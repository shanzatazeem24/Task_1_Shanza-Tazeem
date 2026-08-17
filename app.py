from flask import Flask, render_template, request, redirect
import json
import os

app = Flask(__name__)

DATA_FILE = "tasks.json"


def load_tasks():
    if not os.path.exists(DATA_FILE):
        return []

    with open(DATA_FILE, "r") as file:
        return json.load(file)


def save_tasks(tasks):
    with open(DATA_FILE, "w") as file:
        json.dump(tasks, file, indent=4)


# Home page
@app.route("/shanza")
def home():
    tasks = load_tasks()
    return render_template("index.html", tasks=tasks)


# Add task
@app.route("/add", methods=["POST"])
def add_task():
    task_name = request.form.get("task")

    if task_name:
        tasks = load_tasks()

        new_task = {
            "id": len(tasks) + 1,
            "title": task_name,
            "completed": False
        }

        tasks.append(new_task)
        save_tasks(tasks)

    return redirect("/shanza")


# Complete task
@app.route("/complete/<int:task_id>")
def complete_task(task_id):
    tasks = load_tasks()

    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = True

    save_tasks(tasks)
    return redirect("/shanza")


# Delete task
@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    tasks = load_tasks()

    tasks = [
        task for task in tasks
        if task["id"] != task_id
    ]

    save_tasks(tasks)
    return redirect("/shanza")


# Clear completed tasks
@app.route("/clear")
def clear_completed():
    tasks = load_tasks()

    tasks = [
        task for task in tasks
        if not task["completed"]
    ]

    save_tasks(tasks)
    return redirect("/shanza")


# Run Flask
if __name__ == "__main__":
    app.run(debug=True)