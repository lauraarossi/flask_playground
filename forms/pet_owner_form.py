"""
Pet Owner Form

This file contains the PetOwnerForm class which defines the web form for collecting
pet owner and pet information. The form uses WTForms and includes validation for all
fields. The form handles both owner information (name, email, phone, postal code,
number of pets) and pet information (type, sex, age, location, microchipped status).

Form Fields:
Owner Information:
- name: Owner's full name (required, 2-100 characters)
- email: Owner's email address (required, valid email format)
- phone: Owner's phone number (required, 10-20 characters)
- postal_code: Owner's postal code (required, 3-10 characters)
- num_pets: Number of pets dropdown (0-5, required)

Pet Information (optional - only filled when adding pet details):
- pet_type: Pet type dropdown ('cat' or 'dog')
- sex: Pet sex dropdown ('male' or 'female')
- age: Pet age in years (0-30, integer)
- location_type: Living area dropdown ('city' or 'rural')
- microchipped: Boolean checkbox for microchip status
- submit: Submit button
"""

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, NumberRange, Optional


class PetOwnerForm(FlaskForm):
    # Owner Information
    name = StringField("Name", validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    phone = StringField("Phone", validators=[DataRequired(), Length(min=10, max=20)])
    postal_code = StringField(
        "Postal Code", validators=[DataRequired(), Length(min=3, max=10)]
    )
    num_pets = SelectField(
        "Number of Pets",
        choices=[
            (0, "Select number of pets..."),
            (1, "1"),
            (2, "2"),
            (3, "3"),
            (4, "4"),
            (5, "5"),
        ],
        coerce=int,
        default=0,
    )

    # Pet Information - Made optional since they might not be filled when form is submitted
    pet_type = SelectField(
        "Pet Type",
        choices=[("", "Select pet type..."), ("cat", "Cat"), ("dog", "Dog")],
        validators=[Optional()],
    )
    sex = SelectField(
        "Sex",
        choices=[("", "Select sex..."), ("male", "Male"), ("female", "Female")],
        validators=[Optional()],
    )
    age = IntegerField(
        "Age (years)", validators=[Optional(), NumberRange(min=0, max=30)]
    )
    location_type = SelectField(
        "Living Area",
        choices=[("", "Select living area..."), ("city", "City"), ("rural", "Rural")],
        validators=[Optional()],
    )
    microchipped = BooleanField("Microchipped")

    submit = SubmitField("Submit")
