"""
Pet Owner Database Model

This file contains the PetOwner model class which represents pet owners in the database.
It defines the database schema for storing owner information including name, email,
phone, postal code, and creation timestamp. The model also establishes a one-to-many
relationship with the Pet model through the pets relationship.

Fields:
- id: Primary key (auto-incrementing integer)
- name: Owner's full name (required, max 100 characters)
- email: Owner's email address (required, max 120 characters)
- phone: Owner's phone number (required, max 20 characters)
- postal_code: Owner's postal code (required, max 10 characters)
- created_at: Timestamp when the record was created (auto-set)
- pets: Relationship to Pet model (one-to-many)
"""

from datetime import datetime, timezone


def create_pet_owner_model(db):
    """Create PetOwner model with the provided db instance"""

    class PetOwner(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(100), nullable=False)
        email = db.Column(db.String(120), nullable=False)
        phone = db.Column(db.String(20), nullable=False)
        postal_code = db.Column(db.String(10), nullable=False)
        created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
        pets = db.relationship("Pet", backref="owner", lazy=True)

    return PetOwner
