from flask import Flask,render_template,url_for,request,redirect,session
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
import os

app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
app.config["TRACK_MODIFICATION"] = False
app.secret_key ="uiucuh8574t87582&Y$*&Y$&#"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(days=10)


db = SQLAlchemy(app)


# def start_the_run():
#     with app.app_context():
#         db.create_all()
#     return app


# app = start_the_run()


# if(__name__=="__main__"):
#     app.run(debug=True)
#     with app.app_context():
#         db.create_all()