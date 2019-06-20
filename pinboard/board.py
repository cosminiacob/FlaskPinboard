from flask import Blueprint, render_template, request, redirect, url_for
from pinboard.db import get_db
from datetime import datetime
import json

bp = Blueprint("board", __name__)

#routes
@bp.route("/", methods=("GET", "POST"))
def list():
    ip = request.remote_addr
    if request.method == "POST":
        post_id = request.form["post_id"]
        like_post(post_id,ip)
    posts = get_posts(True)
    return render_template("board/list.html", posts=posts, ip=ip)

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
        

        

# functions
def like_post(post_id,ip):
    db = get_db()
    cursor = db.cursor()
    query = "SELECT id from likes WHERE post_id='{0}' and user_ip='{1}'"
    likes = cursor.execute(query.format(post_id, ip)).fetchall()
    if len(likes) == 0:
        db.execute(
        "INSERT INTO likes (post_id, user_ip) VALUES (?, ?)",
        (post_id, ip)
        )
        db.commit()
 
    
    

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def get_posts(to_json = False):
    db = get_db()

    if to_json:
        db.row_factory = dict_factory

    cursor = db.cursor()

    query = "SELECT rowid, id, title, description, color, created, (SELECT COUNT(id) from likes WHERE post_id=post.id) as likes,(SELECT COUNT(id) from likes ) as total_likes FROM post ORDER BY created DESC"
    rows = cursor.execute(query).fetchall()
    sorted = sorting(rows)
    return sorted

def sorting(posts):
    if len(posts) > 0:
        total_posts = len(posts)
        total_likes =  posts[0]["total_likes"] 
        
        date_format = "%Y-%m-%d %H:%M:%S"
        max_date = posts[0]["created"]
        max_timestamp = datetime.strptime(max_date, date_format).timestamp()
        
        for post in posts:
            post_age = max_timestamp - datetime.strptime(post["created"], date_format).timestamp() / 3600
            post_likes = post["likes"]
            if post_age == 0 :
                post_age=1
            post["popularity"] = post_likes / post_age
        posts_sorted = sorted(posts, key=lambda post: post["popularity"], reverse=True)
        return posts_sorted
    else:
        return posts
