from flask import Flask, Blueprint, render_template,session,redirect,url_for,request
from dbModels.models import User,db,PropertyDetail,Rooms,Persons
from sqlalchemy import func


login_signup = Blueprint('login_signup', __name__)



@login_signup.route("/",methods=["GET","POST"])
def login():
    if(not session):
        return render_template("login.html")
    else:
        return redirect(url_for("after_login.Home"))

# @login_signup.route("/list")
# def list_users():
#     print(User.query.all())
#     return "iucricviuri"

def check_already_exist(email_id):
    check_user = User.query.filter_by(email= email_id).first()
    if(check_user):
        return check_user
    else:
        return False

@login_signup.route("/signUp",methods=["GET","POST"])
def signUp():
    if(session):
        return redirect(url_for("after_login.Home"))

    if(request.method=="POST"):
        user_name = request.form.get("user-name")
        signup_email = request.form.get("signup-email")
        signup_password = request.form.get("signup-password")
        print(user_name)
        print(signup_email)
        exist = check_already_exist(signup_email)
        if(exist):
            session["user_name"] = user_name
            session["email_id"] = signup_email
            session["password"] = signup_password
            session["id"] = exist.id
            return redirect(url_for("login_signup.Home"))
        else:
            create_user = User(user_name= user_name,email=signup_email,password=signup_password)
            db.session.add(create_user)
            db.session.commit()
            session["user_name"] = user_name
            session["email_id"] = signup_email
            session["password"] = signup_password
            exist = check_already_exist(signup_email)
            session["id"] = exist.id
            return redirect(url_for("after_login.Home"))
    else:
        return render_template("sign_up.html")


@login_signup.route('/login',methods =["GET","POST"])
def logged_in():
    email = request.form.get("login-email")
    password = request.form.get("login-password")
    print(email)
    print(password)
    exist = check_already_exist(email)
    if(not exist):
        print(exist)
        return redirect(url_for("login_signup.signUp"))
    else:
        session["user_name"] = exist.user_name
        session["email_id"] = exist.email
        session["password"] = exist.password
        session["id"] = exist.id
        print(exist.email)
        print(exist.password)
        return redirect(url_for("after_login.after_login_function"))




@login_signup.route("/logout")
def logout():
    if(session):
        print(session,"session data")
        session.clear()
        print(session,"after session pop")
    return redirect(url_for("login_signup.login"))



@login_signup.route("/dashboard")
def dashboard():
    user_id = session["id"]
    # Count of properties
    property_count = db.session.query(func.count(PropertyDetail.property_id)).filter(PropertyDetail.user_id == user_id).scalar()

    # Count of rooms
    room_count = db.session.query(func.count(Rooms.room_id)).filter(Rooms.user_id_details == user_id).scalar()

    # Count of persons
    person_count = db.session.query(func.count(Persons.person_id)).filter(Persons.user_id_details == user_id).scalar()

    print(f"User with id {user_id} has {property_count} properties, {room_count} rooms, and {person_count} persons.")
    return render_template("dashboard.html",user_id = user_id,property_count = property_count ,room_count=room_count,person_count = person_count,usr_name = session["user_name"])







