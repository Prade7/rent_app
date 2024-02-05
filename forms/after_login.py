from flask import Blueprint, render_template ,redirect,url_for,request
from dbModels.models import PropertyDetail,db,Rooms,Persons,Payments
from .login_signup import login_signup,session
from dateutil.relativedelta import relativedelta
from datetime import datetime,timedelta
from sqlalchemy import and_
from sqlalchemy import and_, or_
from sqlalchemy.orm import joinedload
from sqlalchemy import desc
from apscheduler.schedulers.background import BackgroundScheduler




after_login = Blueprint("after_login",__name__)

def get_upcoming_date(day: int) -> str:
    today = datetime.today()
    if day > today.day:
        next_date = today.replace(day=day)
    else:
        if today.month == 12:
            next_date = today.replace(year=today.year+1, month=1, day=day)
        else:
            next_date = today.replace(month=today.month+1, day=day)
    return next_date



def get_same_day_next_month(day: int) -> datetime:
    today = datetime.today()
    next_month = today + relativedelta(months=1)
    try:
        return next_month.replace(day=day)
    except ValueError:
        # This handles the edge case where the next month has fewer days.
        # It returns the last day of the next month.
        return (next_month + relativedelta(months=1, day=1)) - relativedelta(days=1)

# Test the function
# print(get_same_day_next_month(31))



# # Test the function
# print(get_upcoming_date(29))  # Output: 29.01.2024
# print(get_upcoming_date(1))   # Output: 01.02.2024

@after_login.route("/addProperties",methods=["GET","POST"])
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
        properties_with_counts = []
        for property in property_details:
            room_count = len(property.rooms)
            person_count = sum(len(room.persons) for room in property.rooms)
            properties_with_counts.append((property, room_count, person_count))
        return render_template("after_logged.html",list_items = properties_with_counts)

    # return render_template("after_logged.html")


@after_login.route("/addPropertyDetails",methods=["GET","POST"])
def addingPropertyDetail():
    print("form data ",request.form)
    if(request.method=="POST"):
        property_id = request.args.get("property_id")
        print("post property_id",property_id)
        if(property_id):
            session["property_id"] =property_id 
        id = request.form.get("item_id")
        floorNo = request.form.get("floor-number",False)
        roomNo = request.form.get("room-number")
        sharable_type = request.form.get("room-sharing")
        add_rooms = Rooms(room_no = roomNo,floor =floorNo,property_room_id =session["property_id"] ,user_id_details=session["id"],sharableType = sharable_type )
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
        aadharNumber = request.form.get("person-aadhar-number")
        paymentAmount = request.form.get("person-payment-amount")
        paymentEmail = request.form.get("person-email")
        day_to_remind = int(request.form.get("person-day-to-remind"))
        # current_date = datetime.now().date()
        nextReminderDate = get_upcoming_date(day_to_remind)
        # nextReminderDate = datetime.strptime(nextReminderDate, '%d.%m.%Y').date()
        add_person = Persons(person_name =personName,age = personAge,aadhar_number = aadharNumber,monthly_payment_amount = paymentAmount,address =personAddress,phone_number =personPhone,user_id_details = session["id"],persons_room=session["room"],next_remainder_date = nextReminderDate, day = day_to_remind,person_email = paymentEmail)
        db.session.add(add_person)
        db.session.commit()
        # payment = Payments(payer_Id = session["id"])
        # db.session.add(payment)
        # db.session.commit()
        return redirect(url_for("after_login.personDetails"))

@after_login.route("/paid",methods=["POST","GET"])
def paid():
    if(request.method == "POST"):
        payment_id = request.form.get("paid-payment-id")
        print(payment_id,"paid payment  Id")
        current_date = datetime.today().date()
        print(current_date)
        paid_month = current_date.strftime('%b%Y').lower()
        monthly_payment_amount = str(request.form.get("paid-amount"))
        person_room_no = request.form.get("person-room-no")
        paid =Payments.query.filter_by(payment_id = payment_id).first()
        paid.paid_date = current_date
        paid.paid_amount = monthly_payment_amount
        paid.paid_month = paid_month
        paid.paid = True
        paid.paid_person_name = request.form.get("paid-person-name")
        db.session.commit()
        paid_person_id = request.form.get("paid-person-id")
        # person = Persons.query.filter_by(person_id = paid_person_id)
        # person.next_

        return redirect("/home")

@after_login.route("/editDelete", methods=["POST","GET"])
def edit_delete_person():
    person_details = {}
    person_id = request.args.get("personId_clicked")
    session["person_id"] = person_id
    if(request.method == "GET"):
        print("name ",request.args.get("person_name"))
        print(request.args.get("payment-amount"))
        print(person_id)
        # print(request.form.get("person-address"))
        person_details["name"] = request.args.get("person_name")
        person_details["age"] = request.args.get("person-age")
        person_details["address"] = request.args.get("person-address")
        person_details["payment_amount"] = request.args.get("payment-amount")
        person_details["next_payment_date"] = request.args.get("next-payment-date")
        person_details["aadhar_number"] = request.args.get("person-aadhar")
        person_details["phone_number"] = request.args.get("person-number")
        person_details["day"] = request.args.get("day")
        person_details["email"] =request.args.get("person-email")
        if(request.args.get("home")):
            session["redirect_to_home"] = True
        return render_template("editRoom.html",person_details = person_details)
        
    else:
        person =Persons.query.filter_by(person_id =session["person_id"], user_id_details = session["id"]).first()
        print(request.form.get("person-day-to-remind"))
        print(session["person_id"], " is the person id ")
        print("post requst name ",request.form.get("person-name"))
        person.person_name = request.form.get("person-name")
        person.age = request.form.get("person-age")
        person.address = request.form.get("person-address")
        person.phone_number = request.form.get("person-phone-number")
        person.person_email = request.form.get("person-email")
        person.aadhar_number = request.form.get("person-aadhar-number")
        person.day = request.form.get("person-day-to-remind")
        nextReminderDate = get_upcoming_date(int(request.form.get("person-day-to-remind")))
        # nextReminderDate = datetime.strptime(nextReminderDate, '%d.%m.%Y').date()
        person.next_remainder_date = nextReminderDate
        person.monthly_payment_amount = request.form.get("person-payment-amount")
        db.session.commit()
        if(session["redirect_to_home"]==True):
            session["redirect_to_home"] = False
            return redirect(url_for("after_login.Home"))
        else:
            return redirect(url_for("after_login.personDetails"))

@after_login.route("/delete",methods=["POST"])
def delete_person():
    if(request.method =="POST"):
        Persons.query.filter_by(person_id = request.form.get("personId_clicked")).delete()
        db.session.commit()
        payments_to_delete = Payments.query.filter(Payments.person_id == request.form.get("personId_clicked"), Payments.paid == False)
        payments_to_delete.delete()
        db.session.commit()
        return redirect(url_for("after_login.personDetails"))

@after_login.route("/home",methods=["GET","POST"])
def Home():
    
# query the database
    persons = db.session.query(Persons).options(joinedload(Persons.room).joinedload(Rooms.property_detail)).filter_by(user_id_details = session["id"])

    for person in persons:
        print(f"Name: {person.person_name}, Room No: {person.room.room_no}, Property: {person.room.property_detail.property_name}")

    # unpaid_payments = db.session.query(Payments).options(joinedload('person'), joinedload('room'), joinedload('room.property_detail')).filter(Payments.paid == False).all()

    # For each unpaid payment, print the person's name, room number, and property name
    # for payment in unpaid_payments:
    #     print(f"Person Name: {payment.person.person_name}, Room No: {payment.room.room_no}, Property Name: {payment.room.property_detail.property_name}")


    unpaid_payments = db.session.query(Persons, Rooms, PropertyDetail, Payments).\
    join(Rooms, Persons.persons_room == Rooms.room_id).\
    join(PropertyDetail, Rooms.property_room_id == PropertyDetail.property_id).\
    join(Payments, Persons.person_id == Payments.person_id).\
    filter(Payments.paid == False, Payments.user_id_details == session["id"]).all()

    for person, room, property_detail, payment in unpaid_payments:
        print(f"Person ID: {person.person_id}, Name: {person.person_name}, Phone Number: {person.phone_number}")
        print(f"Room Number: {room.room_no}")
        print(f"Property Name: {property_detail.property_name}")
        print(f"Monthly Payment Amount: {person.monthly_payment_amount}")
        print(f"Due Month: {payment.due_month}\n")


    return render_template("home.html",all_persons= persons , unpaid_payments = unpaid_payments)






@after_login.route("/paymentHistory",methods=["GET"])
def payment_history():
    if(request.method == "GET"):
        paymentHistory = Payments.query.filter_by(paid = True, user_id_details = session["id"])
        for payment in paymentHistory:
            print(payment.payment_id)
            print(payment.user_id_details)
            print(payment.persons_room_payments)
            print(payment.paid_amount)
            print(payment.paid_date)
            print(payment.paid)
        # print(paymentHistory)
        return "egggretrt"
                
        # persons_paid_on_next_remainder_date = Persons.query.join(Payments, and_(
        # Persons.user_id_details == Payments.user_id_details,
        # Persons.next_remainder_date == Payments.paid_date,
        # Persons.user_id_details == session["id"])).all()


@after_login.route("/allPayment",methods=["GET"])
def payment():
    all_payments = Payments.query.all()
    for ele in all_payments:
        print(ele.person_id,"person id")
        person =Persons.query.filter_by( person_id = ele.person_id)
        for i in person:
            print(i.person_name," person name")
    print(all_payments)
    return "dfnkeuwnu"




# assuming upcoming_date is in the format "YYYY-MM-DD"

@after_login.route("/updatePayments",methods=["GET"])
def check_and_update_payments():
    today = datetime.today().date()
    persons = Persons.query.filter_by(user_id_details = session["id"])
    for person in persons:
        upcoming_date= person.next_remainder_date
        print("next remainder date ", upcoming_date , type(upcoming_date))
        # upcoming_date = datetime.strptime(upcoming_date_str, "%d.%m.%Y")
        if (upcoming_date - today).days <= 7:
            print((upcoming_date-today).days)
            print("payment user id details ",person.user_id_details)
            print("person id ",person.person_id)
            print("upcoming date ", upcoming_date)
            # Check if there is an existing record
            existing_payment = Payments.query.filter_by(user_id_details=person.user_id_details, person_id=person.person_id, payment_due_date=upcoming_date, due_month = person.due_month).first()
            # If there is no existing record, create a new one
            if existing_payment is None:
                payment = Payments(user_id_details=person.user_id_details, person_id=person.person_id, due_month=upcoming_date.strftime("%b%y"), paid =False, persons_room_payments = person.persons_room,payment_due_date = person.next_remainder_date )
                print(payment.user_id_details)
                print(payment.person_id)
                person.due_month = upcoming_date.strftime("%b%y")
                person.next_remainder_date = get_same_day_next_month(person.day)
                print("after payment insert")
                db.session.add(payment)
    db.session.commit()
    return "updated"


# @after_login.route("/updatePayments",methods=["GET"])
# def check_and_update_payments():
#     today = datetime.today()
#     persons = Persons.query.all()  # Assuming Persons is your model for persons table
#     for person in persons:
#         upcoming_date = get_upcoming_date(person.day)
#         print(upcoming_date)
#         upcoming_date = datetime.strptime(upcoming_date, "%d.%m.%Y")
#         if (upcoming_date - today).days == 5:
#             print((upcoming_date-today).days)
#             payment = Payments(user_id_details=person.user_id_details, person_id=person.person_id, due_month=upcoming_date.strftime("%b%y"), paid =False, persons_room_payments = person.persons_room,payment_due_date = person.next_remainder_date )
#             print(payment.user_id_details)
#             print(payment.person_id)
#             persId = payment.person_id
#             db.session.add(payment)
#     db.session.commit()
#     # prs=Persons.query.filter_by(person_id=persId).first()
#     # print(prs.person_name)
#     return "updated"



# scheduler = BackgroundScheduler()
# scheduler.add_job(func=check_and_update_payments, trigger="cron", hour=5)
# scheduler.start()





@after_login.route("/unpaid",methods=["GET"])
def unpaid():
    unpaid_payments = db.session.query(Payments).options(joinedload('person'), joinedload('room'), joinedload('room.property_detail')).filter(Payments.paid == False, Payments.user_id_details == session["id"]).all()

    # For each unpaid payment, print the person's name, room number, and property name
    for payment in unpaid_payments:
        print(f"Person Name: {payment.person.person_name}, Room No: {payment.room.room_no}, Property Name: {payment.room.property_detail.property_name}")
    return "grngrenui"


@after_login.route("/paymentsTable")
def paymentsTable():
    payment = Payments.query.all()

    for p in payment:
        print(f"Payment ID: {p.payment_id}")
        print(f"User ID Details: {p.user_id_details}")
        print(f"Persons Room Payments: {p.persons_room_payments}")
        print(f"Person ID: {p.person_id}")
        print(f"Paid Date: {p.paid_date}")
        print(f"Paid Month: {p.paid_month}")
        print(f"Paid Amount: {p.paid_amount}")
        print(f"Payment Due Date: {p.payment_due_date}")
        print(f"Paid: {p.paid}")
        print(f"Paid Person Name: {p.paid_person_name}")
        print(f"Due Month: {p.due_month}")
        print("-----")

    return "uhefilueu"

@after_login.route("/paid_members")
def paidMembers():
    paid_members  = Persons.query.filter_by(user_details_id = session["id"], paid =True)
    return render_template("paid_members.html", paid_members =paid_members)




@after_login.route('/payments_based_on_month', methods=['GET', 'POST'])
def get_payments():
    payments = []
    if request.method == 'POST':
        # Get start_date and end_date from the form data
        start_date = datetime.strptime(request.form.get('start_date'), '%Y-%m-%d').date()
        end_date = datetime.strptime(request.form.get('end_date'), '%Y-%m-%d').date()

        # Query the database
        payments = Payments.query.filter(
            Payments.paid_date.between(start_date, end_date),
            Payments.paid == True , Payments.user_id_details == session["id"]
        ).all()

    # Render the results in a template
    return render_template('payments_completed.html', payments=payments)

@after_login.route("/p")
def p():
    persons = Persons.query.all()
    today = datetime.today().date()
    for person in persons:
        # upcoming_date = get_upcoming_date(person.day) 
        # upcoming_date = datetime.strptime(upcoming_date, "%d.%m.%Y")
        upcoming_date = person.next_remainder_date
        print(upcoming_date)
        if (upcoming_date - today).days <= 7:
            # print((upcoming_date-today).days)
            # print("payment user id details ",person.user_id_details)
            # print("person id ",person.person_id)
            # print("upcoming date ", upcoming_date)
            # Check if there is an existing record
            existing_payment = Payments.query.filter_by(user_id_details=person.user_id_details,person_id=person.person_id ,paid =False,payment_due_date = person.next_remainder_date)
            for ele in existing_payment:
                print("payment id ",ele.payment_id)
                print("person id ",ele.person_id)
                print("person room ",ele.persons_room_payments)
                print("payment due date",ele.payment_due_date,"utuet")
                print("-----------------------")
    return "diufeubu"



@after_login.route("/date")
def date():
        # specify the due date you're interested in
    due_date_of_interest = datetime.strptime('2024-02-07', '%Y-%m-%d').date()

    # query the Payments table
    payments_due_on_date = Payments.query.filter(Payments.payment_due_date == due_date_of_interest).all()

    for payment in payments_due_on_date:
        print(f"Payment ID: {payment.payment_id}")
        print(f"User ID Details: {payment.user_id_details}")
        print(f"Persons Room Payments: {payment.persons_room_payments}")
        print(f"Person ID: {payment.person_id}")
        print(f"Paid Date: {payment.paid_date}")
        print(f"Paid Month: {payment.paid_month}")
        print(f"Paid Amount: {payment.paid_amount}")
        print(f"Payment Due Date: {payment.payment_due_date}")
        print(f"Paid: {payment.paid}")
        print(f"Paid Person Name: {payment.paid_person_name}")
        print(f"Due Month: {payment.due_month}")
        print("------")
    return "ghztnf"
