#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 15:49:20 2020

@author: Ronin Gomez
"""

# FLASK Tutorial 4 -- We show the bare bones code to get an app up and running

# imports
import os                 # os is used to get environment variables IP & PORT
from flask import Flask   # Flask is the web app that we will customize
from flask import render_template
from flask import request
from flask import redirect, url_for 
from database import db

app = Flask(__name__)     # create an app

notes = {1 : {'title' : 'First note', 'text': 'This is my first note', 'date': '10-1-2020'},
             2: {'title' : 'Second note', 'text' : 'This is my second note', 'date' : '10-2-2020'},
             3: {'title' : 'Third note', 'text' : 'This is my third note', 'date': '10-3-2020'} 
             }

# @app.route is a decorator. It gives the function "index" special powers.
# In this case it makes it so anyone going to "your-url/" makes this function
# get called. What it returns is what is shown as the web page
@app.route('/')
@app.route('/index')
def index():
    a_user = {'name': 'Ronin', 'email':'mogli@uncc.edu'}
    return render_template('index.html', user = a_user)

@app.route('/users/<username>')
def get_user(username):
    return "The user is " + str(username)

@app.route('/notes')
def get_notes():
    a_user = {'name': 'Ronin', 'email':'mogli@uncc.edu'}
    
    return render_template('notes.html', notes = notes, user = a_user)

@app.route('/notes/<note_id>')
def get_note(note_id):
    a_user = {'name': 'Ronin', 'email':'mogli@uncc.edu'}
    
    notes = {1 : {'title' : 'First note', 'text': 'This is my first note', 'date': '10-1-2020'},
                   2 : {'title' : 'Second note', 'text' : 'This is my second note', 'date' : '10-2-2020'},
                   3: {'title' : 'Third note', 'text' : 'This is my third note', 'date': '10-3-2020'}
                   }
    return render_template('note.html', note = notes[int(note_id)], user = a_user)

@app.route('/notes/new', methods = ['GET', 'POST'])
def new_note():
    a_user = {'name': 'Ronin', 'email':'mogli@uncc.edu'}
    
    #check method used for request
    if request.method == 'POST':
        #get title data
        title = request.form['title']
        #get note data
        text = request.form['noteText']
        #create data stamp
        from datetime import date
        today = date.today()
        # format date mm/dd/yyyy
        today = today.strftime("%m-%d-%Y")
        #get the last ID used and increment by 1
        id = len(notes)+1
        #create new note entry
        notes[id] = {'title': title, 'text': text, 'date' : today}
        
        return redirect(url_for('get_notes', name = a_user))
    
    else:
        return render_template('new.html', user = a_user)

app.run(host=os.getenv('IP', '127.0.0.1'),port=int(os.getenv('PORT', 5000)),debug=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask_note_app.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False

#  Bind SQLAlchemy db object to this Flask app
db.init_app(app)

# Setup models
with app.app_context():
    db.create_all()   # run under the app context

# To see the web page in your web browser, go to the url,
#   http://127.0.0.1:5000

# Note that we are running with "debug=True", so if you make changes and save it
# the server will automatically update. This is great for development but is a
# security risk for production.


