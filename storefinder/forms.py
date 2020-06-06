from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectMultipleField, DateField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from wtforms.fields.html5 import URLField
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

class BasicInfoForm(FlaskForm):
	category = SelectField('Category', choices=category_list, validators=[DataRequired()])
	submit = SubmitField('Next')


class InfoForm(FlaskForm):
	name = StringField('Name of facility/amenity/business', validators=[DataRequired()])
	phone_number = IntegerField('Phone number', validators=[DataRequired()])
	website = URLField('Website', validators=[DataRequired()])


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
	social_distancing_rules = TextAreaField('What social distancing rules do customers have to follow?')


class CarMechanicForm(InfoForm):
	social_distancing_rules = TextAreaField('What social distancing rules do customers have to follow?')
	method_of_business = SelectMultipleField('How are they conducting business?', choices=[('In-location', 'In-location'),
																						   ('Home repair', 'Home repair')],
																							validators=[DataRequired()])


class CommunityCentreForm(InfoForm):
	social_distancing_rules = TextAreaField('What social distancing rules do visitors have to follow?')
	restrictions = TextAreaField('What are the restricted activities/places?', validators=[DataRequired()])


class ClinicServicesForm(InfoForm):
	social_distancing_rules = TextAreaField('What social distancing rules do visitors/patients have to follow?')
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
	assembly = BooleanField('Do they offer porch/home assembly?')


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






