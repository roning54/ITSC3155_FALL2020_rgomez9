#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 13:37:22 2020

@author: Ronin Gomez
"""

from database import db

class Note(db.Model):
    id = db.Column("id", db.Integer, primary_key = True)
    title = db.Column("title", db.String(200))
    text = db.Column("text", db.String(100))
    date = db.Column("date", db.String(50))
    #can create a foreign key; referencing the id variable in the User class, so that is why it is lowercase u
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    
    def __init__(self, title, text, date, user_id):
        self.title = title
        self.text = text
        self.date = date
        self.user_id = user_id
        
class User(db.Model):
    id = db.Column("id", db.Integer, primary_key = True)
    first_name = db.Column("first_name", db.String(100))
    last_name = db.Column("last_name", db.String(100))
    email = db.Column("email", db.String(100))
    password = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    #backref: a simple way to also declare a new property on the User class
    #lazy: defines when SQLAlchemy will load the data from the database
    # -- When set to True it means that SQLAlchemy will load the data as necessay in one go
    note = db.relationship("Note", backref = 'user', lazy=True)

    
    def __init__(self, name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.registered_on = datetime.date.today()