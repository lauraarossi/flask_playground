"""
Pet Database Model

This file contains the Pet model class which represents individual pets in the database.
It defines the database schema for storing pet information including type, sex, age,
location type, microchipped status, and pet number. The model establishes a many-to-one
relationship with the PetOwner model through the owner_id foreign key.

Fields:
- id: Primary key (auto-incrementing integer)
- pet_type: Type of pet ('cat' or 'dog', required, max 10 characters)
- sex: Pet's sex ('male' or 'female', required, max 10 characters)
- age: Pet's age in years (required integer)
- location_type: Living area ('city' or 'rural', required, max 10 characters)
- microchipped: Whether the pet is microchipped (boolean, default False)
- pet_number: Sequential number of the pet for multi-pet households (required integer)
- owner_id: Foreign key to PetOwner model (required integer)
- created_at: Timestamp when the record was created (auto-set)
"""

from datetime import datetime


def create_pet_model(db):
    """Create Pet model with the provided db instance"""

    class Pet(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        pet_type = db.Column(db.String(10), nullable=False)  # 'cat' or 'dog'
        sex = db.Column(db.String(10), nullable=False)  # 'male' or 'female'
        age = db.Column(db.Integer, nullable=False)
        location_type = db.Column(db.String(10), nullable=False)  # 'city' or 'rural'
        microchipped = db.Column(db.Boolean, default=False)
        pet_number = db.Column(
            db.Integer, nullable=False
        )  # Sequential number for multi-pet households
        owner_id = db.Column(db.Integer, db.ForeignKey("pet_owner.id"), nullable=False)
        created_at = db.Column(db.DateTime, default=datetime.utcnow)

    return Pet
