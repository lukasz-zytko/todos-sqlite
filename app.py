from flask import Flask, request, render_template, redirect, url_for

from forms import TodoForm
from sqlite_models import todos_sql

app = Flask(__name__)
app.config["SECRET_KEY"] = "nininini"



@app.route("/todos/", methods=["GET", "POST"])
def todos_list():
    form = TodoForm()
    error = ""
    todos_sql.create_connection()
    if request.method == "POST":
        if form.validate_on_submit():
            todos_sql.create(form.data)
        return redirect(url_for("todos_list"))

    return render_template("todos.html", form=form, todos=todos_sql.all(), error=error)


@app.route("/todos/<int:todo_id>/", methods=["GET", "POST"])
def todo_details(todo_id):
    todos_sql.create_connection()
    todoql = todos_sql.get(todo_id)
    form = TodoForm(data=todoql)
    if request.method == "POST":
        if form.validate_on_submit():
            todos_sql.update(todo_id, form.data)
        return redirect(url_for("todos_list"))
    return render_template("todo.html", form=form, todo_id=todo_id)


if __name__ == "__main__":
    app.run(debug=True)