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
from flask import session
from database import db
from models import Note as Note
from models import User as User
from forms import RegisterForm
from forms import LoginForm

app = Flask(__name__)     # create an app

app.config['SECRET_KEY'] = 'SE3155'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask_note_app.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False

#  Bind SQLAlchemy db object to this Flask app
db.init_app(app)

# Setup models
with app.app_context():
    db.create_all()   # run under the app context

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
    if session.get('user'):
        return render_template("index.html", user=session['user'])
    return render_template('index.html')

@app.route('/users/<username>')
def get_user(username):
    return "The user is " + str(username)

@app.route('/notes')
def get_notes():
    #retrieve user from database
    if session.get('user'):
        my_notes = db.session.query(Note).filter_by(user_id=session['user_id']).all()

        return render_template('notes.html', notes=my_notes, user=session['user'])
    else:
        return redirect(url_for('login'))

@app.route('/notes/<note_id>')
def get_note(note_id):
    a_user = db.session.query(User).filter_by(email='mogli@uncc.edu').one()
    my_note = db.session.query(Note).filter_by(id=note_id)
    
    
    return render_template('note.html', note = my_note, user = a_user)

@app.route('/notes/new', methods = ['GET', 'POST'])
def new_note():
    if session.get('user'):
    
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
            new_record = Note(title, text, today, session['user_id'])
            db.session.add(new_record)
            db.session.commit()
            
            return redirect(url_for('get_notes'))

        else:
            return render_template('new.html', user=session['user'])
    
    else:
        return render_template(url_for('login'))

@app.route('/notes/edit/<note_id>', methods = ['GET', 'POST'])
def update_note(note_id):

    #check if a user is saved in session
    if session.get('user'):
        if request.method == 'POST':
            #get title data
            title = request.form['title']
            #get note data
            text = request.form['noteText']
            note = db.session.query(Note).filter_by(id=note_id).one()
            #update note data
            note.title = title
            note.text = text
            #update note in DB
            db.session.add(note)
            db.session.commit()

            return redirect(url_for('get_notes'))
        
        else:
            # GET request - show new note form to edit note

            #retrieve note from database
            my_note = db.session.query(Note).filter_by(id=note_id).one()

            return render_template('new.html', note=my_note, user=session['user'])
    else:
        return redirect(url_for('login'))

@app.route('/notes/delete/<note_id>', methods=['POST'])
def delete_note(note_id):
    if session.get('user'):
        my_note = db.session.query(Note).filter_by(id=node_id).one()
        db.session.delete(my_note)
        db.session.commit()

        return redirect(url_for('get_notes'))
    
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['POST', 'GET'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        the_user = db.session.query(User).filter_by(email=request.form['email']).one()

        if bcrypt.checkpw(request.form['password'].encode('utf-8'), the_user.password):
            session['user'] = the_user.first_name
            sessio['user_id'] = the_user.id

            return redirect(url_for('get_notes'))
        
        login_form.password.errors=["Incorrect username or password."]
        return render_template("login.html", form=login_form)
    
    else:
        return render_template("login.html", form=login_form)

@app.route('/register', methods= ['POST', 'GET'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():

        password_hash = bcrypt.hashpw(
            request.form['password'].encode('utf-8'), bcrypt.gensalt())
        first_name = request.form['firstname']
        last_name = request.form['lastname']
        new_record = User(first_name, last_name, request.form['email'], password_hash)
        db.session.add(new_record)
        db.session.commit()

        session['user'] = first_name
        the_user = db.session.query(User).filter_by(email = request.form['email']).one()
        session['user_id'] = the_user.id
        
        return redirect(url_for('get_notes'))
    return render_template('register.html', form=form)

app.run(host=os.getenv('IP', '127.0.0.1'),port=int(os.getenv('PORT', 5000)),debug=True)



# To see the web page in your web browser, go to the url,
#   http://127.0.0.1:5000

# Note that we are running with "debug=True", so if you make changes and save it
# the server will automatically update. This is great for development but is a
# security risk for production.


