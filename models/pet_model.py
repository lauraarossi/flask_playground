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

Usage:
    from models.pet_model import create_pet_model
    Pet = create_pet_model(db)
"""

from datetime import datetime
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from flask_sqlalchemy import SQLAlchemy
    from .pet_owner_model import PetOwner


def create_pet_model(db: "SQLAlchemy") -> type:
    """
    Create Pet model with the provided database instance.

    This factory function creates a Pet model class that is properly
    bound to the Flask-SQLAlchemy database instance. The model includes
    all necessary fields for storing pet information and establishes
    a many-to-one relationship with the PetOwner model.

    Parameters
    ----------
    db : SQLAlchemy
        Flask-SQLAlchemy database instance

    Returns
    -------
    type
        Pet model class with proper database binding

    Examples
    --------
    >>> from flask_sqlalchemy import SQLAlchemy
    >>> db = SQLAlchemy(app)
    >>> Pet = create_pet_model(db)
    >>> pet = Pet(pet_type="dog", sex="male", age=3, owner_id=1)
    """

    class Pet(db.Model):
        """
        Pet database model representing individual pets.

        This model stores information about individual pets including
        their physical characteristics, living environment, and owner
        relationship. Each pet is associated with exactly one owner
        through a foreign key relationship.

        Attributes
        ----------
        id : int
            Primary key identifier
        pet_type : str
            Type of pet (cat or dog)
        sex : str
            Pet's sex (male or female)
        age : int
            Pet's age in years
        location_type : str
            Living environment (city or rural)
        microchipped : bool
            Whether pet has microchip
        pet_number : int
            Sequential number for multi-pet households
        owner_id : int
            Foreign key to PetOwner
        created_at : datetime
            Timestamp when record was created
        """

        __tablename__ = "pet"

        # Primary key
        id = db.Column(db.Integer, primary_key=True)

        # Pet information fields
        pet_type = db.Column(db.String(10), nullable=False)  # 'cat' or 'dog'
        sex = db.Column(db.String(10), nullable=False)  # 'male' or 'female'
        age = db.Column(db.Integer, nullable=False)
        location_type = db.Column(db.String(10), nullable=False)  # 'city' or 'rural'
        microchipped = db.Column(db.Boolean, default=False)

        # Sequential number for multi-pet households
        pet_number = db.Column(db.Integer, nullable=False)

        # Foreign key to PetOwner
        owner_id = db.Column(db.Integer, db.ForeignKey("pet_owner.id"), nullable=False)

        # Timestamp
        created_at = db.Column(db.DateTime, default=datetime.utcnow)

        def __repr__(self) -> str:
            """
            String representation of the Pet object.

            Returns
            -------
            str
                String representation with id, type, age, and owner_id
            """
            return f"<Pet(id={self.id}, type='{self.pet_type}', age={self.age}, owner_id={self.owner_id})>"

        def to_dict(self) -> dict:
            """
            Convert Pet object to dictionary representation.

            Returns
            -------
            dict
                Dictionary containing pet information with keys:
                - id: Pet ID
                - pet_type: Type of pet
                - sex: Pet's sex
                - age: Pet's age
                - location_type: Living environment
                - microchipped: Microchip status
                - pet_number: Sequential number
                - owner_id: Owner's ID
                - created_at: ISO formatted timestamp
            """
            return {
                "id": self.id,
                "pet_type": self.pet_type,
                "sex": self.sex,
                "age": self.age,
                "location_type": self.location_type,
                "microchipped": self.microchipped,
                "pet_number": self.pet_number,
                "owner_id": self.owner_id,
                "created_at": self.created_at.isoformat() if self.created_at else None,
            }

        @property
        def is_adult(self) -> bool:
            """
            Check if the pet is an adult (1 year or older).

            Returns
            -------
            bool
                True if pet is 1 year or older, False otherwise
            """
            return self.age >= 1

        @property
        def is_senior(self) -> bool:
            """
            Check if the pet is a senior (7 years or older).

            Returns
            -------
            bool
                True if pet is 7 years or older, False otherwise
            """
            return self.age >= 7

        @property
        def age_category(self) -> str:
            """
            Get the age category of the pet.

            Returns
            -------
            str
                Age category string: 'puppy/kitten', 'adult', or 'senior'
            """
            if self.age < 1:
                return "puppy/kitten"
            elif self.age < 7:
                return "adult"
            else:
                return "senior"

        def get_display_name(self) -> str:
            """
            Get a display name for the pet.

            Returns
            -------
            str
                Formatted string with pet type and number
            """
            return f"{self.pet_type.title()} #{self.pet_number}"

        def is_microchipped(self) -> bool:
            """
            Check if the pet is microchipped.

            Returns
            -------
            bool
                True if pet is microchipped, False otherwise
            """
            return self.microchipped

        def get_location_display(self) -> str:
            """
            Get a human-readable location description.

            Returns
            -------
            str
                Formatted location string
            """
            return f"{self.location_type.title()} area"

    return Pet
