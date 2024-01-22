from flask import Flask,render_template,url_for,request,redirect,session
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
import os
from start import app,db
# from dbModels.models import User
from forms.login_signup import login_signup
from forms.after_login import after_login

# @app.route("/",methods=["GET","POST"])
# def login():
#     if(not session):
#         return render_template("login.html")
#     else:
#         return redirect(url_for("after_login"))

# @app.route("/list")
# def list_users():
#     print(user.query.all())
#     return "iucricviuri"

# def check_already_exist(email_id):
#     check_user = user.query.filter_by(email= email_id).first()
#     if(check_user):
#         return check_user
#     else:
#         return False

# @app.route("/signUp",methods=["GET","POST"])
# def signUp():
#     if(session):
#         return redirect(url_for("after_login"))

#     if(request.method=="POST"):
#         user_name = request.form.get("user-name")
#         signup_email = request.form.get("signup-email")
#         signup_password = request.form.get("signup-password")
#         print(user_name)
#         print(signup_email)
#         exist = check_already_exist(signup_email)
#         if(exist):
#             session["user_name"] = user_name
#             session["email_id"] = signup_email
#             session["password"] = signup_password
#             session["id"] = exist.id
#             return redirect(url_for("logged_in"))
#         else:
#             create_user = user(user_name= user_name,email=signup_email,password=signup_password)
#             db.session.add(create_user)
#             db.session.commit()
#             session["user_name"] = user_name
#             session["email_id"] = signup_email
#             session["password"] = signup_password
#             exist = check_already_exist(signup_email)
#             session["id"] = exist.id
#             return redirect(url_for("after_login"))
#     else:
#         return render_template("sign_up.html")


# @app.route('/login',methods =["GET","POST"])
# def logged_in():
#     email = request.form.get("login-email")
#     password = request.form.get("login-password")
#     print(email)
#     print(password)
#     exist = check_already_exist(email)
#     if(not exist):
#         print(exist)
#         return redirect(url_for("signUp"))
#     else:
#         session["user_name"] = exist.user_name
#         session["email_id"] = exist.email
#         session["password"] = exist.password
#         session["id"] = exist.id
#         print(exist.email)
#         print(exist.password)
#         return redirect(url_for("after_login"))

# @app.route("/logged",methods=["GET","POST"])
# def after_login():
#     session.permanent =True
#     return "wenciwenj"


# @app.route("/logout")
# def logout():
#     if(session):
#         print(session,"session data")
#         session.clear()
#         print(session,"after session pop")
#     return redirect(url_for("login"))


app.register_blueprint(login_signup)
app.register_blueprint(after_login)


if(__name__=="__main__"):
    app.run(debug=True)
    with app.app_context():
        db.create_all()