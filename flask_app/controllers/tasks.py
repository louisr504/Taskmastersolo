from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_app.models import task, user
from flask_app.models.user import User
from flask_app.models.task import Task


# Visible Routes

# add task form


@app.route("/task/new")
def new_task_page():
    if "user_id" not in session:  # if not logged in, you can not access route
        return redirect("/")
    data = {
        "id": session["user_id"]
    }
    return render_template("newtask.html", user=User.get_by_id(data))

# edit task form


@app.route("/task/<int:id>/edit")
def edit_task_page(id):
    if "user_id" not in session:  # if not logged in, you can not access route
        return redirect("/")
    return render_template("edittask.html")

# view task


@app.route("/task/<int:id>")
def view_task_page(id):
    if "user_id" not in session:  # if not logged in, you can not access route
        return redirect("/")
    return render_template("viewtask.html")

# Invisible Routes


# delete a task
@app.route("/tasks/<int:id>/deletetask")
def delete_task(id):
    if "user_id" not in session:  # if not logged in, you can not access route
        return redirect("/")
    pass


# add a task to DB (POST METHOD)
@app.route("/tasks/add_to_db", methods=["POST"])
def add_task_to_db():
    if "user_id" not in session:
        return redirect("/")
    # Validate the task
    if not task.Task.validate_task(request.form):
        return redirect("/task/new")
    else:
        # communicate with model and add task to db
        data = {
            "job": request.form["job"],
            "description": request.form["description"],
            "area": request.form["area"],
            "user_id": session["user_id"]
        }
        task.Task.add_task(data)
        return redirect("/dashboard")
        # Redirect to all tasks (dashboard)


# edit a task to DB (POST METHOD)


@app.route("/tasks/<int:id>/edit_to_db", methods=["POST"])
def edit_task_to_db(id):
    if "user_id" not in session:  # if not logged in, you can not access route
        return redirect("/")
    pass
