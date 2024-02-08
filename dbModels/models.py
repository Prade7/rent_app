from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from start import app,db

class User(db.Model):
    __tablename__ = 'login_details'
    id = db.Column(db.Integer,primary_key = True)
    user_name = db.Column(db.String(25),nullable=False)
    email = db.Column(db.String(50),nullable = False)
    password = db.Column(db.String(50),nullable = False)
    properties = db.relationship('PropertyDetail', backref='user', lazy=True)

class PropertyDetail(db.Model):
    __tablename__ = "property_details"
    user_id = db.Column(db.Integer,db.ForeignKey("login_details.id"))
    property_name =db.Column(db.String(20),nullable= False)
    property_id = db.Column(db.Integer,primary_key = True)
    rooms = db.relationship('Rooms', backref='property_detail', lazy=True)

class Rooms(db.Model):
    __tablename__ = "rooms_details"
    property_room_id = db.Column(db.Integer, db.ForeignKey("property_details.property_id"))
    room_no = db.Column(db.Integer,nullable =True)
    floor = db.Column(db.Integer, nullable =True)
    room_id = db.Column(db.Integer, primary_key = True)
    sharableType = db.Column(db.String(10),nullable = True)
    persons = db.relationship('Persons', backref='room', lazy=True)
    user_id_details = db.Column(db.Integer, db.ForeignKey('login_details.id'))

class Persons(db.Model):
    __tablename__ = "person_details"
    person_id = db.Column(db.Integer,primary_key=True)
    person_name = db.Column(db.String(25))
    age = db.Column(db.Integer)
    address = db.Column(db.String(200))
    phone_number = db.Column(db.String(20))
    person_email = db.Column(db.String(25),nullable=True)
    aadhar_number = db.Column(db.String(25),nullable=True)
    # day = db.Column(db.Integer,nullable = False)
    image = db.Column(db.LargeBinary, nullable=True)
    next_remainder_date = db.Column(db.Date,nullable= True)
    monthly_payment_amount = db.Column(db.String(20),nullable =True)
    due_month = db.Column(db.String(20),nullable= True)
    parentName = db.Column(db.String(20),nullable=True)
    deposit_amount = db.Column(db.String(20),nullable=True)
    advanceAmount = db.Column(db.String(20),nullable=True)
    persons_room = db.Column(db.Integer,db.ForeignKey("rooms_details.room_id"))
    user_id_details = db.Column(db.Integer, db.ForeignKey('login_details.id'))

class Payments(db.Model):
    __table_name__ = "payments"
    payment_id = db.Column(db.Integer,primary_key = True)
    user_id_details = db.Column(db.Integer, db.ForeignKey('login_details.id'))
    persons_room_payments = db.Column(db.Integer,db.ForeignKey("rooms_details.room_no"))
    person_id = db.Column(db.Integer,db.ForeignKey("person_details.person_id"))
    paid_date = db.Column(db.Date,nullable =True)
    paid_month = db.Column(db.String(10),nullable =True)
    paid_amount = db.Column(db.String(20),nullable =True)
    payment_due_date = db.Column(db.Date)
    paid = db.Column(db.Boolean, nullable = True)
    paid_person_name = db.Column(db.String(20),nullable = True)
    due_month = db.Column(db.String(20))
    person = db.relationship('Persons', backref='payments')
    room = db.relationship('Rooms', backref='payments')

with app.app_context():
    db.create_all()











