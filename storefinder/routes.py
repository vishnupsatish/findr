import os
import secrets
import parser
from flask import render_template, url_for, flash, redirect, request, abort, session
from storefinder import app, db, bcrypt
from storefinder.forms import *
from storefinder.models import User, Store
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/')
@app.route('/home')
def home():
	return "Hello world"


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/new', methods=["GET", "POST"])
@login_required
def new():
    form = BasicInfoForm()

    if form.validate_on_submit():
        session['category'] = form.category.data
        return redirect(url_for('new_2'))

    return render_template('new.html', title="New", form=form)

form_class_map = {
    "Arts and Crafts": BasicStoreForm,
    "Beauty Parlour": BasicInfoForm,
    "Car Mechanic": CarMechanicForm,
    "Community Centre": CommunityCentreForm,
    "Clothing": BasicStoreForm,
    "Furniture": FurnitureForm,
    "Gas Station": BasicInfoForm,
    "Grocery": BasicStoreForm,
    "Gym": CommunityCentreForm,
    "Hair Salon": BasicInfoForm,
    "Hospital": HospitalForm,
    "Household Services": HouseholdServicesForm,
    "Kids Activities": ActivityForm,
    "Legal Services": LegalForm,
    "Mall": MallForm,
    "Medical Services (dentist, walk-in)": ClinicServicesForm,
    "Parks": ParkForm,
    "Pharmacy": BasicStoreForm,
    "Restaurant": BasicStoreForm,
    "School": SchoolForm,
    "Sports and Recreation": CommunityCentreForm,
    "Technology": BasicStoreForm

}


@app.route('/new/2', methods=["GET"])
@login_required
def new_2():
    if session['category'] == "":
        return redirect(url_for('home'))
    form = form_class_map[session['category']]()
    return render_template('new_2.html', title="New", form=form)
