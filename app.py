from dotenv import load_dotenv
from flask import Flask

from resources.reviews import blp as ReviewBlueprint

def create_app(db_url=None):
    app = Flask(__name__, template_folder='templates')
    load_dotenv()

    app.register_blueprint(ReviewBlueprint)

    return app

