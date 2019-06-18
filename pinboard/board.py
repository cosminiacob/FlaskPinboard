from flask import Blueprint, render_template, request, redirect, url_for
from pinboard.db import get_db

bp = Blueprint("board", __name__)

@bp.route("/")
def list():
    db = get_db()

    posts = db.execute("SELECT * FROM post ORDER BY created DESC").fetchall()

    return render_template("board/list.html", posts=posts)

@bp.route("/add", methods=("GET", "POST"))
def add():
    if request.method == "GET":
        return render_template("board/add.html")
    else:
        title = request.form["title"]
        description = request.form["description"]
        color = request.form["color"]

        db = get_db()
        db.execute(
            "INSERT INTO post (title, description, color) VALUES (?, ?, ?)",
            (title, description, color)
        )
        db.commit()

        return redirect(url_for("board.list"))