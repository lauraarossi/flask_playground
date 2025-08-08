# Pet Buttons Functionality Documentation

This document explains how the multi-pet selection system works across the Flask backend, HTML templates, and JavaScript frontend. The application now features a modular architecture with comprehensive type hints and enhanced documentation.

## Overview

The pet buttons system allows users to:
1. Select how many pets they have (1-5)
2. Dynamically generate buttons for each pet
3. Click on a pet button to add information for that specific pet
4. Track which pets have already been added
5. Maintain owner information across multiple pet submissions

## Architecture Flow

```
User selects number of pets → Dropdown triggers JavaScript → 
Buttons generated dynamically → User clicks pet button → 
Pet form appears → User submits → Flask processes → 
Session tracks progress → Repeat for remaining pets
```

## 1. Flask Backend (Modular Structure)

**Note**: This application uses a modular structure with separate model and form files:
- **Main Application**: `app.py` - Routes and application logic
- **Models**: `models/pet_owner_model.py` and `models/pet_model.py` - Database models
- **Forms**: `forms/pet_owner_form.py` - Form definitions

### Form Definition
**File: `forms/pet_owner_form.py` (lines 18-65)**
```python
class PetOwnerForm(FlaskForm):
    """
    Pet Owner Form for collecting owner and pet information.
    
    This form handles both owner information (required) and pet information
    (optional). The pet information fields are only validated when a pet
    is being added to the database.
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
    
    # Number of pets selection (Required)
    num_pets: SelectField = SelectField(
        "Number of Pets",
        choices=[
            (0, "Select number of pets..."),
            (1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5"),
        ],
        coerce=int,
        default=0,
        validators=[DataRequired(message="Please select the number of pets")],
        description="Number of pets to register"
    )
    
    # Pet Information Fields (Optional - only validated when adding pets)
    pet_type: SelectField = SelectField(
        "Pet Type",
        choices=[("", "Select pet type..."), ("cat", "Cat"), ("dog", "Dog")],
        validators=[Optional()],
        description="Type of pet (cat or dog)"
    )
    # ... additional pet fields with type hints
```

### Database Models
**File: `models/pet_owner_model.py` (lines 25-35)**
```python
def create_pet_owner_model(db: 'SQLAlchemy') -> type:
    """
    Create PetOwner model with the provided database instance.
    
    This factory function creates a PetOwner model class that is properly
    bound to the Flask-SQLAlchemy database instance.
    """
    class PetOwner(db.Model):
        """
        PetOwner database model representing pet owners.
        
        This model stores information about pet owners including their
        personal details and maintains a one-to-many relationship with
        the Pet model.
        """
        
        __tablename__ = 'pet_owner'
        
        # Primary key
        id: int = db.Column(db.Integer, primary_key=True)
        
        # Owner information fields
        name: str = db.Column(db.String(100), nullable=False)
        email: str = db.Column(db.String(120), nullable=False)
        phone: str = db.Column(db.String(20), nullable=False)
        postal_code: str = db.Column(db.String(10), nullable=False)
        
        # Relationship to pets
        pets: List['Pet'] = db.relationship(
            "Pet", 
            backref="owner", 
            lazy=True,
            cascade="all, delete-orphan"
        )
```

**File: `models/pet_model.py` (lines 25-40)**
```python
def create_pet_model(db: 'SQLAlchemy') -> type:
    """
    Create Pet model with the provided database instance.
    
    This factory function creates a Pet model class that is properly
    bound to the Flask-SQLAlchemy database instance.
    """
    class Pet(db.Model):
        """
        Pet database model representing individual pets.
        
        This model stores information about individual pets including
        their physical characteristics, living environment, and owner
        relationship.
        """
        
        __tablename__ = 'pet'
        
        # Primary key
        id: int = db.Column(db.Integer, primary_key=True)
        
        # Pet information fields
        pet_type: str = db.Column(db.String(10), nullable=False)  # 'cat' or 'dog'
        sex: str = db.Column(db.String(10), nullable=False)  # 'male' or 'female'
        age: int = db.Column(db.Integer, nullable=False)
        location_type: str = db.Column(db.String(10), nullable=False)  # 'city' or 'rural'
        microchipped: bool = db.Column(db.Boolean, default=False)
        
        # Sequential number for multi-pet households
        pet_number: int = db.Column(db.Integer, nullable=False)
        
        # Foreign key to PetOwner
        owner_id: int = db.Column(
            db.Integer, 
            db.ForeignKey("pet_owner.id"), 
            nullable=False
        )
```

### Session Management
**File: `app.py` (lines 25-31)**
```python
def index() -> Union[str, Any]:
    """
    Main form page for pet registration.
    
    Handles both GET and POST requests:
    - GET: Displays the pet registration form
    - POST: Processes form submission and saves data to database
    
    The form supports multi-pet registration with session management
    to maintain owner information across multiple pet submissions.
    """
    form: PetOwnerForm = PetOwnerForm()

    # Initialize session data if not exists
    if "owner_data" not in session:
        session["owner_data"] = {}
    if "added_pets" not in session:
        session["added_pets"] = []
    if "total_pets" not in session:
        session["total_pets"] = 0
```

### Form Processing Logic
**File: `app.py` (lines 33-125)**
```python
if form.validate_on_submit():
    try:
        # Get the current pet number from the form
        current_pet_number: str = request.form.get("current_pet_number", "1")

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
```

## 2. HTML Template (templates/index.html)

### Template Structure
**File: `templates/index.html` (lines 15-45)**
```html
<!-- Owner Information Section -->
<div class="form-section">
    <h2>👤 Owner Information</h2>
    <!-- Owner form fields -->
    <div class="form-group">
        {{ form.num_pets.label }}
        {{ form.num_pets(class="form-control", id="numPets") }}
    </div>
</div>

<!-- Pet Buttons Section (initially hidden) -->
<div class="form-section" id="petButtonsSection" style="display: none;">
    <h2>🐕🐈 Select Pet to Add</h2>
    <div id="petButtons" class="pet-buttons">
        <!-- Pet buttons generated here by JavaScript -->
    </div>
</div>

<!-- Pet Information Section (initially hidden) -->
<div class="form-section" id="petInfoSection" style="display: none;">
    <h2>🐕🐈 Pet Information</h2>
    <div class="current-pet-info">
        <p>Currently adding: <strong id="currentPetText">Pet 1</strong></p>
    </div>
    
    <!-- Hidden input to track current pet number -->
    <input type="hidden" id="currentPetNumber" name="current_pet_number" value="1">
    
    <!-- Pet form fields -->
    <div class="form-group">
        {{ form.pet_type.label }}
        {{ form.pet_type(class="form-control") }}
    </div>
    <!-- ... other pet fields ... -->
</div>
```

### Data Passing to JavaScript
**File: `templates/index.html` (lines 95-102)**
```html
<!-- Pass Flask variables to JavaScript -->
<script>
    window.addedPets = {{ added_pets|tojson|safe }};
    window.totalPets = {{ total_pets }};
</script>

<!-- Include external JavaScript -->
<script src="{{ url_for('static', filename='js/pet-form.js') }}"></script>
```

## 3. JavaScript (static/js/pet-form.js)

### Initialization
**File: `static/js/pet-form.js` (lines 1-15)**
```javascript
document.addEventListener('DOMContentLoaded', function() {
    // Get DOM elements
    const numPetsSelect = document.getElementById('numPets');
    const petButtonsSection = document.getElementById('petButtonsSection');
    const petButtons = document.getElementById('petButtons');
    const petInfoSection = document.getElementById('petInfoSection');
    const currentPetText = document.getElementById('currentPetText');
    const currentPetNumber = document.getElementById('currentPetNumber');
    const petForm = document.getElementById('petForm');
    let selectedPetNumber = null;
    
    // Get data from Flask
    const addedPets = window.addedPets || [];
    const totalPets = window.totalPets || 0;
```

### Dropdown Change Handler
**File: `static/js/pet-form.js` (lines 17-55)**
```javascript
numPetsSelect.addEventListener('change', function() {
    const selectedValue = parseInt(this.value);
    
    if (selectedValue === 0) {
        // Hide sections when no pets selected
        petButtonsSection.style.display = 'none';
        petInfoSection.style.display = 'none';
        petButtons.innerHTML = '';
        selectedPetNumber = null;
    } else {
        // Show pet buttons section
        petButtonsSection.style.display = 'block';
        petInfoSection.style.display = 'none';
        
        // Generate pet buttons dynamically
        petButtons.innerHTML = '';
        for (let i = 1; i <= selectedValue; i++) {
            const button = document.createElement('button');
            button.type = 'button';
            button.className = 'pet-button';
            button.textContent = `Pet ${i}`;
            button.dataset.petNumber = i;
            
            // Mark already added pets
            if (addedPets.includes(i)) {
                button.classList.add('added');
                button.textContent = `Pet ${i} ✓`;
                button.disabled = true;
            }
            
            // Add click handler
            button.addEventListener('click', function() {
                if (addedPets.includes(i)) return; // Prevent re-adding
                
                // Update UI
                document.querySelectorAll('.pet-button').forEach(btn => {
                    btn.classList.remove('selected');
                });
                this.classList.add('selected');
                
                // Show pet form
                petInfoSection.style.display = 'block';
                
                // Update current pet info
                const petNumber = this.dataset.petNumber;
                currentPetText.textContent = `Pet ${petNumber}`;
                currentPetNumber.value = petNumber;
                selectedPetNumber = parseInt(petNumber);
            });
            
            petButtons.appendChild(button);
        }
    }
});
```

### Form Validation
**File: `static/js/pet-form.js` (lines 57-85)**
```javascript
petForm.addEventListener('submit', function(e) {
    const selectedValue = parseInt(numPetsSelect.value);
    
    // Validate dropdown selection
    if (selectedValue === 0) {
        e.preventDefault();
        alert('Please select the number of pets first.');
        return false;
    }
    
    // Validate pet selection
    if (selectedPetNumber === null) {
        e.preventDefault();
        alert('Please select a pet to add information for.');
        return false;
    }
    
    // Prevent duplicate submissions
    if (addedPets.includes(selectedPetNumber)) {
        e.preventDefault();
        alert('This pet has already been added. Please select a different pet.');
        return false;
    }
    
    // Validate pet information completeness
    const petType = document.querySelector('select[name="pet_type"]').value;
    const sex = document.querySelector('select[name="sex"]').value;
    const age = document.querySelector('input[name="age"]').value;
    const locationType = document.querySelector('select[name="location_type"]').value;
    
    if (!petType || !sex || age === '' || !locationType) {
        e.preventDefault();
        alert('Please complete all pet information fields before submitting.');
        return false;
    }
});
```

## 4. CSS Styling (static/css/style.css)

### Pet Button Styles
**File: `static/css/style.css` (lines 120-155)**
```css
.pet-buttons {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-top: 15px;
}

.pet-button {
    background-color: #ff00ff;
    color: white;
    padding: 12px 20px;
    border: none;
    border-radius: 5px;
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

.pet-button:hover {
    background-color: #d400d4;
}

.pet-button.selected {
    background-color: #d400d4;
    box-shadow: 0 0 5px rgba(255, 0, 255, 0.5);
}

.pet-button.added {
    background-color: #4caf50;
    cursor: not-allowed;
    opacity: 0.8;
}

.pet-button.added:hover {
    background-color: #4caf50;
}

.pet-button:disabled {
    cursor: not-allowed;
    opacity: 0.6;
}
```

### Progress Indicator
**File: `static/css/style.css` (lines 157-165)**
```css
.progress-info {
    background-color: #e8f5e8;
    border: 2px solid #4caf50;
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 20px;
    text-align: center;
}
```

## 5. Data Flow Summary

1. **User selects number of pets** → Dropdown triggers JavaScript
2. **JavaScript generates buttons** → One button per pet (1-5)
3. **User clicks pet button** → Pet form appears with current pet indicator
4. **User fills pet information** → Form validation ensures completeness
5. **User submits form** → Flask processes and saves to database
6. **Flask updates session** → Tracks which pets have been added
7. **Form resets** → Owner info preserved, pet form cleared
8. **Process repeats** → Until all pets are added
9. **Session cleared** → Ready for new submission

## 6. Key Features

### Enhanced Type Safety
- **Full Type Hints**: Complete type annotation throughout all Python files
- **Type Checking**: Static type checking with mypy
- **IDE Support**: Better autocomplete and error detection
- **Runtime Safety**: Prevents type-related errors

### Improved Documentation
- **Comprehensive Docstrings**: Detailed documentation for all functions and classes
- **Usage Examples**: Clear examples of how to use each component
- **Modular Structure**: Clear separation of concerns with dedicated files
- **Professional Standards**: Follows Python best practices

### Session Management
- **Owner Data Persistence**: Maintains owner information across multiple pet submissions
- **Pet Progress Tracking**: Shows which pets have been added
- **Duplicate Prevention**: Prevents adding the same pet twice
- **Visual Feedback**: Different styles for added vs. available pets
- **Form Validation**: Ensures all required fields are completed
- **Database Integration**: Each pet gets a unique pet_number in the database

## 7. Error Handling

### Client-side Validation
- **JavaScript Validation**: Prevents invalid submissions
- **User Feedback**: Clear error messages and success confirmations
- **Form Completeness**: Ensures all required fields are filled

### Server-side Validation
- **Flask Form Validation**: Validates form data and session state
- **Database Error Handling**: Proper error handling for database operations
- **Exception Handling**: Comprehensive error logging and user feedback
- **Type Safety**: Type hints help prevent runtime errors

### Enhanced Error Messages
- **Detailed Validation**: Specific error messages for each field
- **User-friendly Language**: Clear, actionable error messages
- **Progress Tracking**: Shows current status and next steps

## 8. Development Tools

### Type Checking
```bash
# Run type checking
mypy app.py models/ forms/

# Run with strict mode
mypy --strict app.py
```

### Code Quality
```bash
# Format code with black
black app.py models/ forms/

# Sort imports
isort app.py models/ forms/

# Run linter
flake8 app.py models/ forms/
```

### Testing
```bash
# Run tests
pytest

# Run Flask-specific tests
pytest-flask
```

## 9. Modular Architecture Benefits

### Code Organization
- **Separation of Concerns**: Models, forms, and routes in separate files
- **Maintainability**: Easier to locate and modify specific functionality
- **Reusability**: Components can be imported and used elsewhere
- **Testing**: Individual components can be tested in isolation

### Type Safety
- **Static Type Checking**: Catches errors before runtime
- **Better IDE Support**: Enhanced autocomplete and error detection
- **Documentation**: Type hints serve as inline documentation
- **Refactoring**: Safer code changes with type checking

### Professional Standards
- **Modern Python**: Uses latest Python type hinting features
- **Best Practices**: Follows Flask and SQLAlchemy conventions
- **Development Tools**: Comprehensive tooling for quality assurance
- **Documentation**: Professional-grade documentation standards

---

**Summary**: The pet buttons functionality has been enhanced with a modular architecture, comprehensive type hints, and professional development tooling, making it more maintainable, type-safe, and well-documented.
