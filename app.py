# Import necessary modules
import os
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from sqlalchemy.orm import validates
from algorithim import *

# Set the base directory
basedir = os.path.abspath(os.path.dirname(__file__))

# Create a Flask app instance
app = Flask(__name__)

# Configure the app's database settings
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create a SQLAlchemy instance
db = SQLAlchemy(app)

# Variable
space = [1, 1, 1, 1]    # Spots left for ['f1', 'f2, 'f3', 'f4']

# Define a Member database model using SQLAlchemy
class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    MBTI = db.Column(db.String(4), nullable=False)
    family = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())

    def __repr__(self):
        return f'<Member {self.firstname}>'
    
    @validates('MBTI')
    def validate_MBTI(self, key, value):
        valid_types = ['ISTJ', 'ISFJ', 'INFJ', 'INTJ', 'ISTP', 'ISFP',
                       'INFP', 'INTP', 'ESTP', 'ESFP', 'ENFP', 'ENTP',
                       'ESTJ', 'ESFJ', 'ENFJ', 'ENTJ']
        if value not in valid_types:
            raise ValueError(f'{value} is not a valid MBTI type')
        return value

# Define the app's routes and corresponding view functions
@app.route('/')
def index():
    members = Member.query.all()
    return render_template('index.html', members=members)

@app.route('/<int:member_id>/')
def member(member_id):
    member = Member.query.get_or_404(member_id)
    return render_template('member.html', member=member)

@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        MBTI = request.form['MBTI']

        f1members = Member.query.filter_by(family='f1').all()
        f1member_list = []
        for f1member in f1members:
            f1member_list.append(MBTIconverter(f1member.MBTI))
        f2members = Member.query.filter_by(family='f2').all()
        f2member_list = []
        for f2member in f2members:
            f2member_list.append(MBTIconverter(f2member.MBTI))
        f3members = Member.query.filter_by(family='f3').all()
        f3member_list = []
        for f3member in f3members:
            f3member_list.append(MBTIconverter(f3member.MBTI))
        f4members = Member.query.filter_by(family='f4').all()
        f4member_list = []
        for f4member in f4members:
            f4member_list.append(MBTIconverter(f4member.MBTI))
        families = [f1member_list, f2member_list, f3member_list, f4member_list]

        family = selection(MBTI, families, space)
        print(space)

        member = Member(firstname=firstname,
                          lastname=lastname,
                          MBTI=MBTI,
                          family=family)
        db.session.add(member)
        db.session.commit()

        return redirect(url_for('index'))
    
    return render_template('create.html')

@app.route('/newcreate/', methods=('GET', 'POST'))
def newcreate():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        MBTI = request.form['MBTI']
        family = request.form['family']
        member = Member(firstname=firstname,
                          lastname=lastname,
                          MBTI=MBTI,
                          family=family)
        db.session.add(member)
        db.session.commit()

        return redirect(url_for('index'))
    
    return render_template('newcreate.html')

@app.route('/<int:member_id>/edit/', methods=('GET', 'POST'))
def edit(member_id):
    member = Member.query.get_or_404(member_id)

    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        MBTI = request.form['MBTI']
        family = request.form['family']

        member.firstname = firstname
        member.lastname = lastname
        member.MBTI = MBTI
        member.family = family

        db.session.add(member)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('edit.html', member=member)

@app.post('/<int:member_id>/delete/')
def delete(member_id):
    member = Member.query.get_or_404(member_id)
    db.session.delete(member)
    db.session.commit()
    return redirect(url_for('index'))