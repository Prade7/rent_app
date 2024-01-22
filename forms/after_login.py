from flask import Blueprint, render_template ,redirect,url_for,request
from dbModels.models import PropertyDetail,db,Rooms,Persons
from .login_signup import login_signup,session


after_login = Blueprint("after_login",__name__)



@after_login.route("/logged",methods=["GET","POST"])
def after_login_function():
    # session.permanent =True
    print("form data ",request.form)
    if(request.method=="POST"):
        propertyName = request.form.get("propertyName")
        add_property_details = PropertyDetail(property_name = propertyName,user_id = session["id"])
        db.session.add(add_property_details)
        db.session.commit()
        return redirect(url_for("after_login.after_login_function"))
    else:
        property_details = PropertyDetail.query.filter_by(user_id = session["id"]).order_by(PropertyDetail.property_id).all()
        for items in property_details:
            print(items, "aeradrr")
        # print(items.rooms)
        return render_template("after_logged.html",list_items = property_details)
    print(session)

    # return render_template("after_logged.html")


@after_login.route("/addPropertyDetails",methods=["GET","POST"])
def addingPropertyDetail():
    print("form data ",request.form)
    if(request.method=="POST"):
        property_id = request.form.get("property_id")
        print("post property_id",property_id)
        if(property_id):
            session["property_id"] =property_id 
        id = request.form.get("item_id")
        floorNo = request.form.get("floor-number",False)
        roomNo = request.form.get("room-number")
        add_rooms = Rooms(room_no = roomNo,floor =floorNo,property_room_id =session["property_id"] ,user_id_details=session["id"] )
        db.session.add(add_rooms)
        db.session.commit()
        return redirect(url_for("after_login.addingPropertyDetail"))
    else:
        id = request.args.get("property_id")
        print(id,"Get request id")
        if(id):
            session["property_id"] = id
        print(session["property_id"],"-- session property id")
        print(session["id"],"-- session id")
        room_list  = Rooms.query.filter_by(property_room_id = session["property_id"],user_id_details = session["id"])
        
        # room_list = Rooms.query.all()
        print(room_list)
        for item in room_list:
            print(item.property_room_id,"property room id")
            print(item.room_no," room no")
            print(item.floor," floor no")
            print(item.room_id," room Id")
            print(item.user_id_details, "user room")
            

        for  itm in room_list:
            print(itm.property_room_id,"fjiwueui")
        print(room_list)
        return render_template("propertyDetails.html",room_list = room_list)

@after_login.route("/addPersonDetails",methods=["GET","POST"])
def personDetails():
    room_id = request.args.get("room_id")
    if(room_id):
        session["room"] = room_id
    if(request.method == "GET"):
        person_details = Persons.query.filter_by(user_id_details = session["id"],persons_room=session["room"])

        return render_template("roomDetails.html",person_details=person_details)
    else:
        personName = request.form.get("person-name")
        personAge = request.form.get("person-age")
        personAddress = request.form.get("person-address")
        personPhone = request.form.get("person-phone-number")

        add_person = Persons(person_name =personName,age = personAge,address =personAddress,phone_number =personPhone,user_id_details = session["id"],persons_room=session["room"])
        db.session.add(add_person)
        db.session.commit()
        return redirect(url_for("after_login.personDetails"))