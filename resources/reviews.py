import os
import openai
from dotenv import load_dotenv

from flask import request, render_template
from flask_smorest import Blueprint

from utilities import *

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

blp = Blueprint(
    "reviews", __name__, description="Reviews for Excellenz", template_folder="templates", static_folder="static"
)


@blp.route('/', methods=['GET', 'POST'])
def index():
    result = ""
    customization = "Auto-Improve"
    if request.method == 'POST':
        review = request.form.get('review')
        customization = request.form.get('customization')
        changed_review = gpt_improved_reviews(review, customization)
        result = f"{changed_review}"

    return render_template('index.html', result=result, selected_option=f"{customization}")
