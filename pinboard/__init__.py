import os
from flask import Flask

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        DATABASE=os.path.join(app.instance_path, "pinboard.sqlite")
    )

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from pinboard import db
    db.init_app(app)

    from pinboard import board
    app.register_blueprint(board.bp)
    app.register_blueprint(board.bp, url_prefix="/board")

    return app