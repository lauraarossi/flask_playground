[A sample app to play around with flask and javascript]
# Pet Information Form - Flask App

A Flask web application that collects information about pets and their owners using WTForms and stores the data in a SQLite database.

## Features

- **Pet Information Collection**: Collects data about pets (cat/dog, sex, age, location, microchipped status)
- **Owner Information**: Gathers owner details (name, email, phone, postal code)
- **Form Validation**: Uses WTForms with comprehensive validation
- **Database Storage**: SQLite database with proper relationships
- **Modern UI**: Clean, responsive design with magenta accent color
- **Data Viewing**: View all submitted data in a table format

## Setup Instructions

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**:
   ```bash
   python app.py
   ```

3. **Access the Application**:
   - Open your browser and go to `http://localhost:5000`
   - Fill out the form with pet and owner information
   - Click "Submit" to save the data
   - Use the "View All Data" link to see all submissions

## Database Schema

### PetOwner Table
- `id`: Primary key
- `name`: Owner's name
- `email`: Owner's email address
- `phone`: Owner's phone number
- `postal_code`: Owner's postal code
- `created_at`: Timestamp of submission

### Pet Table
- `id`: Primary key
- `pet_type`: 'cat' or 'dog'
- `sex`: 'male' or 'female'
- `age`: Age in years
- `location_type`: 'city' or 'rural'
- `microchipped`: Boolean (True/False)
- `owner_id`: Foreign key to PetOwner
- `created_at`: Timestamp of submission

## Form Fields

### Owner Information
- **Name**: Required, 2-100 characters
- **Email**: Required, valid email format
- **Phone**: Required, 10-20 characters
- **Postal Code**: Required, 3-10 characters

### Pet Information
- **Pet Type**: Required, select from Cat or Dog
- **Sex**: Required, select from Male or Female
- **Age**: Required, 0-30 years
- **Living Area**: Required, select from City or Rural
- **Microchipped**: Optional checkbox

## Styling

The application features:
- Clean white background
- Magenta (#ff00ff) accent color
- Responsive design
- Modern form styling with focus effects
- Success/error message styling
- Hover effects on interactive elements

## File Structure

```
flask_playground/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── templates/
│   ├── base.html         # Base template with styling
│   ├── index.html        # Main form page
│   └── view_data.html    # Data viewing page
└── pets.db               # SQLite database (created automatically)
```

## Technologies Used

- **Flask**: Web framework
- **Flask-SQLAlchemy**: Database ORM
- **Flask-WTF**: Form handling
- **WTForms**: Form validation
- **SQLite**: Database
- **HTML/CSS**: Frontend styling

