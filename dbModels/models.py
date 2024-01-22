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
    persons = db.relationship('Persons', backref='room', lazy=True)
    user_id_details = db.Column(db.Integer, db.ForeignKey('login_details.id'))

class Persons(db.Model):
    __tablename__ = "person_details"
    person_id = db.Column(db.Integer,primary_key=True)
    person_name = db.Column(db.String(25))
    age = db.Column(db.Integer)
    address = db.Column(db.String(200))
    phone_number = db.Column(db.String(20))
    persons_room = db.Column(db.Integer,db.ForeignKey("rooms_details.room_id"))
    user_id_details = db.Column(db.Integer, db.ForeignKey('login_details.id'))

with app.app_context():
    db.create_all()
