# Flask Pet Registration Application

A Flask web application for registering pet owners and their pets with a dynamic multi-pet interface. The application features a modular architecture with separate models and forms, session management for multi-pet submissions, and a responsive UI with pet selection buttons.

## 🚀 Features

### Core Functionality
- **Multi-Pet Registration**: Add multiple pets (1-5) for a single owner
- **Dynamic Pet Buttons**: Interactive buttons for selecting which pet to add
- **Session Management**: Maintains owner data across multiple pet submissions
- **Progress Tracking**: Visual indicators showing which pets have been added
- **Form Validation**: Comprehensive client and server-side validation
- **Database Storage**: SQLite database with proper relationships

### Technical Features
- **Modular Architecture**: Separated models, forms, and application logic
- **Type Hints**: Full type annotation throughout the codebase
- **Comprehensive Documentation**: Detailed docstrings and comments
- **Responsive Design**: Modern UI with magenta accent color scheme
- **Error Handling**: Robust error handling with user-friendly messages

## 📁 Project Structure

```
flask_playground/
├── app.py                          # Main Flask application (routes and logic)
├── models/                         # Database models directory
│   ├── __init__.py                # Package initialization
│   ├── pet_owner_model.py         # PetOwner database model
│   └── pet_model.py               # Pet database model
├── forms/                          # Forms directory
│   ├── __init__.py                # Package initialization
│   └── pet_owner_form.py          # PetOwnerForm definition
├── templates/                      # HTML templates
│   ├── base.html                  # Base template with common layout
│   ├── index.html                 # Main form page
│   └── view_data.html             # Data display page
├── static/                         # Static assets
│   ├── css/
│   │   └── style.css              # Application styling
│   └── js/
│       └── pet-form.js            # Client-side JavaScript
├── instance/                       # Database files
│   └── pets.db                    # SQLite database
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── PET_BUTTONS_DOCUMENTATION.md   # Detailed pet buttons documentation
└── MODULAR_STRUCTURE_SUMMARY.md   # Modular architecture overview
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.9.6 or higher
- Anaconda (recommended) or pip

### Environment Setup
```bash
# Create and activate conda environment
conda create -n flask-demo python=3.9.6
conda activate flask-demo

# Install dependencies
pip install -r requirements.txt
```

### Database Setup
```bash
# Run the application (database will be created automatically)
python app.py
```

## 🎯 Usage

### Starting the Application
```bash
python app.py
```
The application will be available at `http://127.0.0.1:5000`

### Adding Pet Data
1. **Fill Owner Information**: Enter name, email, phone, and postal code
2. **Select Number of Pets**: Choose how many pets to register (1-5)
3. **Click Pet Buttons**: Dynamic buttons appear for each pet
4. **Add Pet Details**: Fill in pet information (type, sex, age, location, microchipped)
5. **Submit**: Pet data is saved to database
6. **Repeat**: Continue for remaining pets
7. **View Data**: Check `/view_data` to see all submissions

### Features in Action
- **Session Persistence**: Owner information is preserved across pet submissions
- **Progress Tracking**: Visual feedback shows which pets have been added
- **Duplicate Prevention**: Cannot add the same pet twice
- **Form Validation**: Ensures all required fields are completed
- **Reset Functionality**: Clear session to start fresh

## 🗄️ Database Schema

### PetOwner Table
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | Integer | Primary Key | Auto-incrementing ID |
| name | String(100) | Not Null | Owner's full name |
| email | String(120) | Not Null | Owner's email address |
| phone | String(20) | Not Null | Owner's phone number |
| postal_code | String(10) | Not Null | Owner's postal code |
| created_at | DateTime | Default UTC | Record creation timestamp |
| pets | Relationship | One-to-Many | Associated pets |

### Pet Table
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | Integer | Primary Key | Auto-incrementing ID |
| pet_type | String(10) | Not Null | 'cat' or 'dog' |
| sex | String(10) | Not Null | 'male' or 'female' |
| age | Integer | Not Null | Age in years (0-30) |
| location_type | String(10) | Not Null | 'city' or 'rural' |
| microchipped | Boolean | Default False | Microchip status |
| pet_number | Integer | Not Null | Sequential pet number |
| owner_id | Integer | Foreign Key | Reference to PetOwner |
| created_at | DateTime | Default UTC | Record creation timestamp |

## 🎨 UI/UX Features

### Design Elements
- **Color Scheme**: Magenta accent (#ff00ff) with white background
- **Responsive Layout**: Works on desktop and mobile devices
- **Interactive Buttons**: Dynamic pet selection buttons
- **Progress Indicators**: Visual feedback for completion status
- **Form Validation**: Real-time validation with clear error messages

### Pet Button States
- **Default**: Magenta background, clickable
- **Selected**: Darker magenta with shadow
- **Added**: Green background with checkmark, disabled
- **Hover Effects**: Smooth color transitions

## 🔧 Technical Architecture

### Modular Structure
- **Models**: Database schema and relationships in `models/` directory
- **Forms**: WTForms definitions in `forms/` directory
- **Routes**: Application logic in `app.py`
- **Templates**: Jinja2 templates in `templates/` directory
- **Static Assets**: CSS and JavaScript in `static/` directory

### Key Components
- **Flask-SQLAlchemy**: Database ORM
- **Flask-WTF**: Form handling and validation
- **WTForms**: Form field definitions and validation
- **Jinja2**: Template engine
- **SQLite**: Lightweight database

### Session Management
- **Owner Data Persistence**: Maintains owner information across submissions
- **Pet Progress Tracking**: Tracks which pets have been added
- **Session Reset**: Clear functionality to start fresh

## 📚 Documentation

### Code Documentation
- **Type Hints**: Full type annotation throughout
- **Docstrings**: Comprehensive function and class documentation
- **Comments**: Inline comments explaining complex logic
- **File Headers**: Multi-line documentation for each module

### User Documentation
- **README.md**: Project overview and setup instructions
- **PET_BUTTONS_DOCUMENTATION.md**: Detailed pet buttons functionality
- **MODULAR_STRUCTURE_SUMMARY.md**: Architecture and organization details

## 🧪 Testing

### Manual Testing Checklist
- [ ] Owner information form validation
- [ ] Pet selection dropdown functionality
- [ ] Dynamic pet button generation
- [ ] Pet form validation and submission
- [ ] Session persistence across submissions
- [ ] Progress tracking and visual feedback
- [ ] Duplicate prevention
- [ ] Database storage and retrieval
- [ ] Error handling and user feedback
- [ ] Reset functionality

### Browser Compatibility
- Chrome (recommended)
- Firefox
- Safari
- Edge

## 🚀 Future Enhancements

### Planned Features
- **User Authentication**: Login system for multiple users
- **Pet Photos**: Image upload functionality
- **Advanced Search**: Filter and search pet data
- **Export Functionality**: CSV/PDF export of pet data
- **Email Notifications**: Confirmation emails
- **API Endpoints**: RESTful API for external integrations

### Technical Improvements
- **Database Migrations**: Alembic for schema versioning
- **Testing Framework**: Unit and integration tests
- **Docker Support**: Containerized deployment
- **Environment Configuration**: Production-ready config management
- **Logging**: Comprehensive application logging

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes with proper documentation
4. Add type hints to new code
5. Test thoroughly
6. Submit a pull request

### Code Standards
- **Type Hints**: All functions must have type annotations
- **Documentation**: Comprehensive docstrings for all functions
- **Comments**: Explain complex logic with inline comments
- **Modular Design**: Follow the existing modular structure
- **Error Handling**: Proper exception handling throughout

## 📄 License

This project is open source and available under the MIT License.

## 📞 Support

For questions or issues:
1. Check the documentation files
2. Review the code comments and docstrings
3. Test the application manually
4. Create an issue with detailed information

---

**Built with Flask, SQLAlchemy, and modern web technologies**

