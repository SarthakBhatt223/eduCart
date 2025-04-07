# EduCart - Scientific Calculator with User Authentication

EduCart is a feature-rich scientific calculator application with secure user authentication, built using Python and Tkinter. It provides both basic and advanced mathematical operations in an intuitive interface.

## Features

- 🔒 Secure user login/signup system with JSON-based storage
- 🧮 Full-featured scientific calculator with:
  - Basic arithmetic operations
  - Trigonometric functions (sin, cos, tan)
  - Logarithmic functions (log, ln)
  - Square roots and exponents
  - Constants (π, e)
  - Factorial calculations
- 🌙 Dark/Light theme toggle
- 🖥️ Responsive and modern UI with custom styling
- 🔄 User-friendly navigation between login and calculator screens
- 🔄 Password change functionality

## Installation

### For End Users (Windows)
Download the ready-to-use installer:
1. Go to [Releases page](https://github.com/SarthakBhatt223/eduCart/releases)
2. Download the latest `setup.exe`
3. Run the installer and follow the prompts
4. Launch EduCart from your desktop or start menu

### For Developers
Prerequisites:
- Python 3.6 or higher
- Git (optional)

# Clone the repository (or download ZIP)
git clone https://github.com/SarthakBhatt223/eduCart.git

# Navigate to project folder
cd eduCart

# Install dependencies (though tkinter comes with Python)
pip install -r requirements.txt  # if you have additional dependencies

# Run the application
python main.py


Usage Guide
Account Management
Action	Steps
New User	1. Click "Sign Up"
2. Choose username
3. Set password
Existing User	1. Enter credentials
2. Click "Login"
Calculator Operations
Button	Function	Example Input	Result
√	Square root	9 √	3
^	Power	2 ^ 3	8
!	Factorial	5 !	120
π	Pi constant	π	3.14159...
🌙	Toggle theme	Click	Switches mode
Pro Tip: Use parentheses () to control operation order: (2+3)*4 = 20
