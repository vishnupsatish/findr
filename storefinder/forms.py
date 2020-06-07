import requests
from flask_wtf import FlaskForm
from flask_login import current_user
from flask import Markup
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectMultipleField, DateField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from wtforms.widgets import HTMLString
from wtforms.fields.html5 import URLField, IntegerField, SearchField
from storefinder.models import User


category_list = [("Arts and Crafts", "Arts and Crafts"),
				("Beauty Parlour", "Beauty Parlour"),
				("Car Mechanic", "Car Mechanic"),
				("Clothing", "Clothing"),
				("Community Centre", "Community Centre"),
				("Furniture", "Furniture"),
				("Gas Station", "Gas Station"),
				("Grocery", "Grocery"),
				("Gym", "Gym"),
				("Hair Salon", "Hair Salon"),
				("Hospital", "Hospital"),
				("Household Services", "Household Services"),
				("Kids Activities", "Kids Activities"),
				("Legal Services", "Legal Services"),
				("Mall", "Mall"),
				("Medical Services (dentist, walk-in)", "Medical Services (dentist, walk-in)"),
				("Parks", "Parks"),
				("Pharmacy", "Pharmacy"),
				("Restaurant", "Restaurant"),
				("School", "School"),
				("Sports and Recreation", "Sports and Recreation"),
				("Technology", "Technology")]

class RegistrationForm(FlaskForm):
	username = StringField('Username',
						   validators=[DataRequired(), Length(min=2, max=20)])
	email = StringField('Email',
						validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password',
									 validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Sign Up')

	def validate_username(self, username):
		try:
			user = User.query.filter_by(username=username.data)[0]
		except:
			return
		raise ValidationError("That username is taken. Please choose a different one.")

	def validate_email(self, email):
		try:
			user = User.query.filter_by(email=email.data)[0]
		except:
			return
		raise ValidationError("That email is taken. Please choose a different one.")


class LoginForm(FlaskForm):
	email = StringField('Email',
						validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Login')


class InlineButtonWidget(object):
    html = """
    <button %s type="submit">%s</button>
    """

    def __init__(self, label, input_type='submit'):
        self.input_type = input_type
        self.label = label

    def __call__(self, **kwargs):
        param = []
        for key in kwargs:
            param.append(key + "=\"" + kwargs[key] + "\"")
        return HTMLString(self.html % (" ".join(param), self.label))

class ProfileSearchForm(FlaskForm):
    name = SearchField('search', validators=[Length(min=2, max=20)])
    materialize_icon = Markup("<i style=\"line-height: 40px; height: 100%;\" class=\"material-icons\">search</i>")
    font_awesome = Markup(Markup("<i style=\"font-size: 10px; height: 100%; padding-top: 0px;\" class=\"fas fa-search\"></i>"))
    submit = InlineButtonWidget(materialize_icon)

class CategorySearchForm(FlaskForm):
	category = SelectField('Category', choices=category_list, validators=[DataRequired()])
	submit = SubmitField('Search')

class AdminDeleteForm(FlaskForm):
	submit = SubmitField('Delete')


class BasicInfoForm(FlaskForm):
	category = SelectField('Category', choices=category_list, validators=[DataRequired()])
	submit = SubmitField('Next')


class InfoForm(FlaskForm):
	name = StringField('Name of facility/amenity/business', validators=[DataRequired()])
	date = StringField('When did this facility/amenity/business open?', validators=[DataRequired()])
	phone_number = IntegerField('Phone number', validators=[DataRequired()])
	website = URLField('Website', validators=[DataRequired()])
	source = StringField('Where did you get this information? (Websites, URLs, etc.)', validators=[DataRequired()])
	image_link = URLField('Add a link for the logo of the company/facility/amenity, with a white or transparent background.', validators=[DataRequired()])
	submit = SubmitField('Add')

	def validate_image_link(self, image_link):
		print(image_link.data)
		image_formats = ("image/png", "image/jpeg", "image/jpg")
		r = requests.head(image_link.data)
		if not r.headers["content-type"] in image_formats:
			raise ValidationError("The image link you have provided is not a direct link to an image, in JPG or PNG format.")


class BasicStoreForm(InfoForm):
	social_distancing_rules = TextAreaField('What social distancing rules do customers have to follow?')
	method_of_business = SelectMultipleField('How are they conducting business?', choices=[('Delivery', 'Delivery'),
																						   ('In-store', 'In-store'),
																						   ('In-store pickup', 'In-store pickup'),
																						   ('Curbside pickup', 'Curbside pickup')],
																							validators=[DataRequired()])
	in_store_pickup = TextAreaField('How does the in-store pickup work?')
	curbside_delivery = TextAreaField('How does the curbside pickup work?')


class HospitalForm(InfoForm):
	social_distancing_rules = TextAreaField('What social distancing rules do customers have to follow?', validators=[DataRequired()])


class CarMechanicForm(InfoForm):
	social_distancing_rules = TextAreaField('What social distancing rules do customers have to follow?', validators=[DataRequired()])
	method_of_business = SelectMultipleField('How are they conducting business?', choices=[('In-location', 'In-location'),
																						   ('Home repair', 'Home repair')],
																							validators=[DataRequired()])


class CommunityCentreForm(InfoForm):
	social_distancing_rules = TextAreaField('What social distancing rules do visitors have to follow?', validators=[DataRequired()])
	restrictions = TextAreaField('What are the restricted activities/places?', validators=[DataRequired()])


class ClinicServicesForm(InfoForm):
	social_distancing_rules = TextAreaField('What social distancing rules do visitors/patients have to follow?', validators=[DataRequired()])
	type_of_clinic = SelectMultipleField('What type of clinic is this?', choices=[('Dentist', 'Dentist'),
																						   ('Optometrist', 'Optometrist'),
																						   ('Walk-in Clinic', 'Walk-in Clinic')],
											 												validators=[DataRequired()])
	method_of_business = SelectMultipleField('How are they conducting business?', choices=[('In-facility', 'In-facility'),
																						   ('Online', 'Online'),
																						   ('Phone', 'Phone')],
											 												validators=[DataRequired()])

	appointments = TextAreaField('How do you book appointments?', validators=[DataRequired()])

household_categories = [('Electrican', 'Electrican'),
						('Lawn/Garden', 'Lawn/Garden'),
						('Plumber', 'Plumber')]

class HouseholdServicesForm(InfoForm):
	household_category = SelectField(choices=household_categories, validators=[DataRequired()])
	appointments = TextAreaField('How do you book appointments?', validators=[DataRequired()])


class FurnitureForm(BasicStoreForm):
	assembly = BooleanField('Porch/home assembly')


class ParkForm(InfoForm):
	social_distancing_rules = TextAreaField('What social distancing rules do visitors have to follow?', validators=[DataRequired()])
	restrictions = TextAreaField('What are the restricted activities/places?', validators=[DataRequired()])


class SchoolForm(InfoForm):
	method_of_business = SelectMultipleField('How are the schools operating?', choices=[('Online', 'Online'),
																						   ('In-person', 'In-person')],
																							validators=[DataRequired()])

class LegalForm(InfoForm):
	method_of_business = SelectMultipleField('How is the law office operating?', choices=[('Online', 'Online'),
																						   ('In-person', 'In-person')],
																							validators=[DataRequired()])


class ActivityForm(InfoForm):
	method_of_business = SelectMultipleField('How is the activity operating?', choices=[('Online', 'Online'),
																						   ('In-person', 'In-person')],
																							validators=[DataRequired()])


class MallForm(InfoForm):
	social_distancing_rules = TextAreaField('What social distancing rules do visitors have to follow?', validators=[DataRequired()])






