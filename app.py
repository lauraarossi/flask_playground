from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, NumberRange
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pets.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Models
class PetOwner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    postal_code = db.Column(db.String(10), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    pets = db.relationship('Pet', backref='owner', lazy=True)

class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pet_type = db.Column(db.String(10), nullable=False)  # 'cat' or 'dog'
    sex = db.Column(db.String(10), nullable=False)  # 'male' or 'female'
    age = db.Column(db.Integer, nullable=False)
    location_type = db.Column(db.String(10), nullable=False)  # 'city' or 'rural'
    microchipped = db.Column(db.Boolean, default=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('pet_owner.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# WTForm
class PetOwnerForm(FlaskForm):
    # Owner Information
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired(), Length(min=10, max=20)])
    postal_code = StringField('Postal Code', validators=[DataRequired(), Length(min=3, max=10)])
    
    # Pet Information
    pet_type = SelectField('Pet Type', choices=[('cat', 'Cat'), ('dog', 'Dog')], validators=[DataRequired()])
    sex = SelectField('Sex', choices=[('male', 'Male'), ('female', 'Female')], validators=[DataRequired()])
    age = IntegerField('Age (years)', validators=[DataRequired(), NumberRange(min=0, max=30)])
    location_type = SelectField('Living Area', choices=[('city', 'City'), ('rural', 'Rural')], validators=[DataRequired()])
    microchipped = BooleanField('Microchipped')
    
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = PetOwnerForm()
    if form.validate_on_submit():
        try:
            # Create owner
            owner = PetOwner(
                name=form.name.data,
                email=form.email.data,
                phone=form.phone.data,
                postal_code=form.postal_code.data
            )
            db.session.add(owner)
            db.session.flush()  # Get the owner ID
            
            # Create pet
            pet = Pet(
                pet_type=form.pet_type.data,
                sex=form.sex.data,
                age=form.age.data,
                location_type=form.location_type.data,
                microchipped=form.microchipped.data,
                owner_id=owner.id
            )
            db.session.add(pet)
            db.session.commit()
            
            flash('Pet and owner information submitted successfully!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred. Please try again.', 'error')
    
    return render_template('index.html', form=form)

@app.route('/view_data')
def view_data():
    owners = PetOwner.query.all()
    return render_template('view_data.html', owners=owners)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
