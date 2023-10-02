import openai
from dotenv import dotenv_values
from flask import Flask, render_template, request

import os
from dotenv import load_dotenv

from flask import Flask
from flask_smorest import Api 
from flask_migrate import Migrate

from resources.reviews import blp as ReviewBlueprint


def create_app(db_url=None):
    app = Flask(__name__, template_folder='templates')
    load_dotenv()

    app.register_blueprint(ReviewBlueprint)

    return app





############################
# DOCKER & ALEMBIC COMMANDS
############################


# Docker Command to build docker image: docker build -t store-python-api .
# Docker Command to run docker in the back ground with portforwarding and constant updating: docker run -dp 5005:5000 -w /app -v "$(pwd):/app" store-python-api
# Docker Command to run the docker terminal for the particular container: docker run -it store-api-python /bin/bash


# To activate Alembic in Flask - flask db init
# To create the flask migrations - flask db migrate
# To apply the migrations - flask db upgrade







############################
# OLD CODE
############################

# OPENAI_API_KEY=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

# config = dotenv_values(".env")
# openai.api_key = config["OPENAI_API_KEY"]

# app = Flask(__name__, 
#             template_folder='templates'
# )

# def review_prompt_helper(review: str, customization: str) -> str:
#     response = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {"role": "system", 
#              "content": """
#                     You will receive a review from the user and a customization or style in which to help you model and improve 
#                     the review in.
#                     Evaluate the context from the review provided and provide an improved review in the style and customization
#                     asked by the user.
#                     Do not convey any potentially false information.
#                     Strive to make your review as detailed as possible. 
#                     Respond in precise detail, directly repeating the information that you're referencing from the review provided.
#                     The user will only see your improved review and not the context you've been provided. 
#              """},
#             {"role": "user", 
#              "content": f"""
#                     Improve the following review with the style or customization provided:
#                     Review: {review}
#                     Customization or style provided: {customization}
#                     Desired Output format: A single string object containing the improved review.
#             """}
#         ]
#     )
#     return response["choices"][0]["message"]["content"]


# @app.route('/', methods=['GET', 'POST'])
# def index():
#     result = ""
#     if request.method == 'POST':
#         review = request.form.get('review')
#         customization = request.form.get('customization')
#         changed_review = review_prompt_helper(review, customization)
#         result = f"{customization}: {changed_review}"

#     return render_template('index.html', result=result)


# if __name__ == "__main__":
#     app.run(debug=True)

