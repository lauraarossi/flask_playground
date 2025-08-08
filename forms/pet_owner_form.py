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

Usage:
    from forms.pet_owner_form import PetOwnerForm
    form = PetOwnerForm()
"""

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, NumberRange, Optional
from typing import Any, Dict, List, Tuple, Union


class PetOwnerForm(FlaskForm):
    """
    Pet Owner Form for collecting owner and pet information.
    
    This form handles both owner information (required) and pet information
    (optional). The pet information fields are only validated when a pet
    is being added to the database. The form includes comprehensive
    validation for all fields with user-friendly error messages.
    
    Attributes:
        name: Owner's full name field
        email: Owner's email address field
        phone: Owner's phone number field
        postal_code: Owner's postal code field
        num_pets: Number of pets selection field
        pet_type: Pet type selection field (optional)
        sex: Pet sex selection field (optional)
        age: Pet age input field (optional)
        location_type: Pet living area selection field (optional)
        microchipped: Pet microchip status checkbox (optional)
        submit: Form submission button
    """
    
    # Owner Information Fields (Required)
    name: StringField = StringField(
        "Name", 
        validators=[
            DataRequired(message="Name is required"),
            Length(min=2, max=100, message="Name must be between 2 and 100 characters")
        ],
        description="Owner's full name"
    )
    
    email: StringField = StringField(
        "Email", 
        validators=[
            DataRequired(message="Email is required"),
            Email(message="Please enter a valid email address")
        ],
        description="Owner's email address"
    )
    
    phone: StringField = StringField(
        "Phone", 
        validators=[
            DataRequired(message="Phone number is required"),
            Length(min=10, max=20, message="Phone number must be between 10 and 20 characters")
        ],
        description="Owner's phone number"
    )
    
    postal_code: StringField = StringField(
        "Postal Code", 
        validators=[
            DataRequired(message="Postal code is required"),
            Length(min=3, max=10, message="Postal code must be between 3 and 10 characters")
        ],
        description="Owner's postal code"
    )
    
    # Number of pets selection (Required)
    num_pets: SelectField = SelectField(
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
        validators=[
            DataRequired(message="Please select the number of pets")
        ],
        description="Number of pets to register"
    )

    # Pet Information Fields (Optional - only validated when adding pets)
    pet_type: SelectField = SelectField(
        "Pet Type",
        choices=[
            ("", "Select pet type..."), 
            ("cat", "Cat"), 
            ("dog", "Dog")
        ],
        validators=[Optional()],
        description="Type of pet (cat or dog)"
    )
    
    sex: SelectField = SelectField(
        "Sex",
        choices=[
            ("", "Select sex..."), 
            ("male", "Male"), 
            ("female", "Female")
        ],
        validators=[Optional()],
        description="Pet's sex (male or female)"
    )
    
    age: IntegerField = IntegerField(
        "Age (years)", 
        validators=[
            Optional(),
            NumberRange(min=0, max=30, message="Age must be between 0 and 30 years")
        ],
        description="Pet's age in years"
    )
    
    location_type: SelectField = SelectField(
        "Living Area",
        choices=[
            ("", "Select living area..."), 
            ("city", "City"), 
            ("rural", "Rural")
        ],
        validators=[Optional()],
        description="Pet's living environment"
    )
    
    microchipped: BooleanField = BooleanField(
        "Microchipped",
        description="Whether the pet is microchipped"
    )

    submit: SubmitField = SubmitField(
        "Submit",
        description="Submit the form"
    )
    
    def validate_pet_information(self) -> bool:
        """
        Validate that all pet information fields are completed when adding a pet.
        
        This method is called when the form is submitted to ensure that
        if pet information is being provided, all required pet fields
        are filled out completely.
        
        Returns:
            True if pet information is valid or not provided, False otherwise
        """
        # If any pet field is filled, all must be filled
        pet_fields = [self.pet_type.data, self.sex.data, self.age.data, self.location_type.data]
        
        # Check if any pet field has data
        has_pet_data = any(field for field in pet_fields if field is not None and field != "")
        
        if has_pet_data:
            # If any pet field is filled, all must be filled
            if not all(field for field in pet_fields if field is not None and field != ""):
                self.pet_type.errors.append("Please complete all pet information fields")
                return False
        
        return True
    
    def get_owner_data(self) -> Dict[str, Any]:
        """
        Get owner information as a dictionary.
        
        Returns:
            Dictionary containing owner information
        """
        return {
            'name': self.name.data,
            'email': self.email.data,
            'phone': self.phone.data,
            'postal_code': self.postal_code.data,
            'num_pets': self.num_pets.data
        }
    
    def get_pet_data(self) -> Dict[str, Any]:
        """
        Get pet information as a dictionary.
        
        Returns:
            Dictionary containing pet information, or empty dict if no pet data
        """
        if not self.validate_pet_information():
            return {}
        
        return {
            'pet_type': self.pet_type.data,
            'sex': self.sex.data,
            'age': self.age.data,
            'location_type': self.location_type.data,
            'microchipped': self.microchipped.data
        }
    
    def has_pet_information(self) -> bool:
        """
        Check if the form contains pet information.
        
        Returns:
            True if any pet field has data, False otherwise
        """
        pet_fields = [self.pet_type.data, self.sex.data, self.age.data, self.location_type.data]
        return any(field for field in pet_fields if field is not None and field != "")
    
    def is_complete(self) -> bool:
        """
        Check if the form is complete and ready for submission.
        
        Returns:
            True if form is complete, False otherwise
        """
        # Check if owner information is complete
        owner_fields = [self.name.data, self.email.data, self.phone.data, self.postal_code.data]
        if not all(field for field in owner_fields):
            return False
        
        # Check if number of pets is selected
        if self.num_pets.data == 0:
            return False
        
        # If pet information is provided, it must be complete
        if self.has_pet_information():
            return self.validate_pet_information()
        
        return True
