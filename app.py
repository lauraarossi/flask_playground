from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
import os

# Import model creation functions and form
from models.pet_owner_model import create_pet_owner_model
from models.pet_model import create_pet_model
from forms.pet_owner_form import PetOwnerForm

app = Flask(__name__)
app.config["SECRET_KEY"] = "your-secret-key-here"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///pets.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize database with the app
db = SQLAlchemy(app)

# Create models with the database instance
PetOwner = create_pet_owner_model(db)
Pet = create_pet_model(db)


@app.route("/", methods=["GET", "POST"])
def index():
    form = PetOwnerForm()

    # Initialize session data if not exists
    if "owner_data" not in session:
        session["owner_data"] = {}
    if "added_pets" not in session:
        session["added_pets"] = []
    if "total_pets" not in session:
        session["total_pets"] = 0

    if form.validate_on_submit():
        try:
            # Get the current pet number from the form
            current_pet_number = request.form.get("current_pet_number", 1)

            # If this is the first submission, save owner data to session
            if not session["owner_data"]:
                session["owner_data"] = {
                    "name": form.name.data,
                    "email": form.email.data,
                    "phone": form.phone.data,
                    "postal_code": form.postal_code.data,
                }
                session["total_pets"] = form.num_pets.data

            # Validate that pet information is provided when a pet is selected
            if (
                form.pet_type.data
                and form.sex.data
                and form.age.data is not None
                and form.location_type.data is not None
            ):
                # Check if this pet has already been added
                if int(current_pet_number) in session["added_pets"]:
                    flash(
                        f"Pet {current_pet_number} has already been added. Please select a different pet.",
                        "error",
                    )
                    return render_template("index.html", form=form)

                # Create owner (only on first pet)
                if not session["added_pets"]:
                    owner = PetOwner(
                        name=session["owner_data"]["name"],
                        email=session["owner_data"]["email"],
                        phone=session["owner_data"]["phone"],
                        postal_code=session["owner_data"]["postal_code"],
                    )
                    db.session.add(owner)
                    db.session.flush()  # Get the owner ID
                    session["owner_id"] = owner.id
                else:
                    # Get existing owner
                    owner = PetOwner.query.get(session["owner_id"])

                # Create pet
                pet = Pet(
                    pet_type=form.pet_type.data,
                    sex=form.sex.data,
                    age=form.age.data,
                    location_type=form.location_type.data,
                    microchipped=form.microchipped.data,
                    pet_number=int(current_pet_number),
                    owner_id=owner.id,
                )
                db.session.add(pet)
                db.session.commit()

                # Add to session tracking
                session["added_pets"].append(int(current_pet_number))

                flash(
                    f"Pet {current_pet_number} added successfully! ({len(session['added_pets'])} of {session['total_pets']} pets added)",
                    "success",
                )

                # Check if all pets have been added
                if len(session["added_pets"]) == session["total_pets"]:
                    flash(
                        "All pets have been added! You can view all data or start a new submission.",
                        "success",
                    )
                    # Clear session data
                    session.pop("owner_data", None)
                    session.pop("added_pets", None)
                    session.pop("total_pets", None)
                    session.pop("owner_id", None)
                    return redirect(url_for("index"))

                return render_template("index.html", form=form)
            else:
                # Pet information is incomplete
                flash(
                    "Please complete all pet information fields before submitting.",
                    "error",
                )
                return render_template("index.html", form=form)

        except Exception as e:
            db.session.rollback()
            import traceback

            print(f"Error details: {str(e)}")
            print(f"Traceback: {traceback.format_exc()}")
            flash(f"An error occurred: {str(e)}. Please try again.", "error")
    elif form.errors:
        # Form validation failed - provide detailed error messages
        error_messages = []
        for field, errors in form.errors.items():
            field_name = (
                getattr(form, field).label.text
                if hasattr(form, field) and hasattr(getattr(form, field), "label")
                else field
            )
            for error in errors:
                error_messages.append(f"{field_name}: {error}")

        if error_messages:
            flash(
                "Please fix the following errors: " + "; ".join(error_messages), "error"
            )

    # Pre-populate form with session data if available
    if session["owner_data"]:
        form.name.data = session["owner_data"].get("name", "")
        form.email.data = session["owner_data"].get("email", "")
        form.phone.data = session["owner_data"].get("phone", "")
        form.postal_code.data = session["owner_data"].get("postal_code", "")
        form.num_pets.data = session["total_pets"]

    return render_template(
        "index.html",
        form=form,
        added_pets=session.get("added_pets", []),
        total_pets=session.get("total_pets", 0),
    )


@app.route("/view_data")
def view_data():
    owners = PetOwner.query.all()
    return render_template("view_data.html", owners=owners)


@app.route("/reset")
def reset():
    """Reset session data to start fresh"""
    session.clear()
    flash("Session reset. You can start a new submission.", "success")
    # return redirect(url_for("index"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
