import os
import secrets
import parser
from PIL import Image
#import cv2
#import numpy as np
#from skimage import io
from io import BytesIO
import cloudinary
import cloudinary.uploader
import cloudinary.api
from datetime import datetime
from flask import render_template, url_for, flash, redirect, request, abort, session
from storefinder import app, db, bcrypt
from storefinder.forms import *
from storefinder.models import User, Store
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/')
@app.route('/home')
def home():
	return render_template('home.html')


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
    "Beauty Parlour": InfoForm,
    "Car Mechanic": CarMechanicForm,
    "Community Centre": CommunityCentreForm,
    "Clothing": BasicStoreForm,
    "Furniture": FurnitureForm,
    "Gas Station": InfoForm,
    "Grocery": BasicStoreForm,
    "Gym": CommunityCentreForm,
    "Hair Salon": InfoForm,
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



@app.route('/new/2', methods=["GET", "POST"])
@login_required
def new_2():
    form = form_class_map[session['category']]()
    if session['category'] == "":
        return redirect(url_for('home'))
    if form.validate_on_submit():
        store_content = ""
        for field in form:
            if isinstance(field.data, str):
                if field.data.strip() == "":
                    continue
            if field.label.text == 'CSRF Token' or field.label.text == "Add" or field.label.text == 'Add a link for the logo of the company/facility/amenity, with a white or transparent background.':
                continue
            data = field.data
            if field.type == "BooleanField":
                data = "Yes" if field.data else "No"
            elif isinstance(field.data, int):
                data = str(field.data)
            elif isinstance(field.data, list):
                if field.data == []:
                    continue
                data = ''
                for elem in field.data:
                    data += '<div class="chip">' + elem + '</div>'
            url = form.image_link.data
            response = requests.get(url)
            dirname = os.path.dirname(__file__)
            Image1 = Image.open(os.path.join(dirname, 'static/background.jpg'))
            Image1 = Image1.convert("RGBA")

            Image1copy = Image1.copy()
            Image2 = Image.open(BytesIO(response.content))
            Image2 = Image2.convert("RGBA")

            Image2copy = Image2.copy()
            base = 450
            if Image2copy.height < Image2copy.width:
                wpercent = (base / float(Image2copy.size[0]))
                hsize = int((float(Image2copy.size[1]) * float(wpercent)))
                Image2copy = Image2copy.resize((base, hsize))
                Image1copy.paste(Image2copy, (25, 250 - (Image2copy.height // 2)), Image2copy)

            else:
                hpercent = (base / float(Image2copy.size[1]))
                wsize = int((float(Image2copy.size[0]) * float(hpercent)))
                Image2copy = Image2copy.resize((wsize, base))
                Image1copy.paste(Image2copy, (250 - (Image2copy.width // 2), 25), Image2copy)

            # paste image giving dimensions
            # Image1copy.save("hi.png")
            cloudinary.config(
                cloud_name="dnwczwamg",
                api_key="778543234586879",
                api_secret="S1OSxuJqxBkpDSkwbxBoTLVgiw0"
            )
            imgByteArr = BytesIO()
            Image1copy.save(imgByteArr, format='PNG')
            imgByteArr = imgByteArr.getvalue()
            try:
                filename = Store.query.all()[-1].id + 1
            except:
                filename = 1

            cloudinary.uploader.upload(imgByteArr, public_id=filename)

            store_content += "<b>" + field.label.text + "</b><br><p>" + "".join([data]) + "</p>"


        print(store_content)
        store = Store(company_name=form.name.data, content=store_content, author=current_user, date=datetime.strptime(form.date.data, "%b %d, %Y"), category=session['category'], checked=False, image_file=str(filename) + ".png")
        db.session.add(store)
        db.session.commit()
        flash("Your store posting has been sent to the moderators for approval.", "success")
        return redirect(url_for("home"))


    return render_template("new_2.html", form=form, category=session['category'])




@app.route('/store/<int:id>')
def specific_store(id):
    store = Store.query.get_or_404(id)
    return render_template('specific_store.html', content=store.content, image=store.image_file)
