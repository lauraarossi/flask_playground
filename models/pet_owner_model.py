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

Usage:
    from models.pet_owner_model import create_pet_owner_model
    PetOwner = create_pet_owner_model(db)
"""

from datetime import datetime, timezone
from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from flask_sqlalchemy import SQLAlchemy
    from .pet_model import Pet


def create_pet_owner_model(db: "SQLAlchemy") -> type:
    """
    Create PetOwner model with the provided database instance.

    This factory function creates a PetOwner model class that is properly
    bound to the Flask-SQLAlchemy database instance. The model includes
    all necessary fields for storing pet owner information and establishes
    a one-to-many relationship with the Pet model.

    Parameters
    ----------
    db : SQLAlchemy
        Flask-SQLAlchemy database instance

    Returns
    -------
    type
        PetOwner model class with proper database binding

    Examples
    --------
    >>> from flask_sqlalchemy import SQLAlchemy
    >>> db = SQLAlchemy(app)
    >>> PetOwner = create_pet_owner_model(db)
    >>> owner = PetOwner(name="John Doe", email="john@example.com")
    """

    class PetOwner(db.Model):
        """
        PetOwner database model representing pet owners.

        This model stores information about pet owners including their
        personal details and maintains a one-to-many relationship with
        the Pet model. Each owner can have multiple pets associated
        with their account.

        Attributes
        ----------
        id : int
            Primary key identifier
        name : str
            Owner's full name (required)
        email : str
            Owner's email address (required)
        phone : str
            Owner's phone number (required)
        postal_code : str
            Owner's postal code (required)
        created_at : datetime
            Timestamp when record was created
        pets : List[Pet]
            Relationship to associated Pet objects
        """

        __tablename__ = "pet_owner"

        # Primary key
        id = db.Column(db.Integer, primary_key=True)

        # Owner information fields
        name = db.Column(db.String(100), nullable=False)
        email = db.Column(db.String(120), nullable=False)
        phone = db.Column(db.String(20), nullable=False)
        postal_code = db.Column(db.String(10), nullable=False)

        # Timestamp
        created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

        # Relationship to pets
        pets = db.relationship(
            "Pet", backref="owner", lazy=True, cascade="all, delete-orphan"
        )

        def __repr__(self) -> str:
            """
            String representation of the PetOwner object.

            Returns
            -------
            str
                String representation with id, name, and email
            """
            return f"<PetOwner(id={self.id}, name='{self.name}', email='{self.email}')>"

        def to_dict(self) -> dict:
            """
            Convert PetOwner object to dictionary representation.

            Returns
            -------
            dict
                Dictionary containing owner information with keys:
                - id: Owner ID
                - name: Owner's name
                - email: Owner's email
                - phone: Owner's phone
                - postal_code: Owner's postal code
                - created_at: ISO formatted timestamp
                - pets_count: Number of pets owned
            """
            return {
                "id": self.id,
                "name": self.name,
                "email": self.email,
                "phone": self.phone,
                "postal_code": self.postal_code,
                "created_at": self.created_at.isoformat() if self.created_at else None,
                "pets_count": len(self.pets),
            }

        @property
        def pets_count(self) -> int:
            """
            Get the number of pets associated with this owner.

            Returns
            -------
            int
                Number of pets owned by this person
            """
            return len(self.pets)

        def has_pets(self) -> bool:
            """
            Check if the owner has any pets.

            Returns
            -------
            bool
                True if owner has pets, False otherwise
            """
            return len(self.pets) > 0

    return PetOwner
