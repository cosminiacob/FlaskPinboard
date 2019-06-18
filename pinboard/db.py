import click
import sqlite3
from flask import current_app
from flask.cli import with_appcontext

def get_db():
    db = sqlite3.connect(
        current_app.config["DATABASE"]
    )
    db.row_factory = sqlite3.Row
    return db

def init_db():
    db = get_db()
    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))

@click.command("init-db")
@with_appcontext
def init_db_command():
    init_db()
    click.echo("DB initialized")

def init_app(app):
    app.cli.add_command(init_db_command)