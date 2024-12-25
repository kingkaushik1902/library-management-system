<<<<<<< HEAD
# library-management-system
A Flask-based Library Management System for managing books and members
=======

# Library Management System

A Flask-based web application for managing books and members in a library. The project includes user authentication, CRUD operations for books and members, and pagination, all wrapped in a responsive UI built with Bootstrap.

---

## **Features**
- **User Management**:
  - Register new users with email and password.
  - Log in and log out securely.
  - Delete user accounts with a confirmation prompt.
- **Books Management**:
  - Add, edit, delete, and view books.
  - Search books by title.
  - Filter books by language level.
  - Pagination for browsing books.
- **Members Management**:
  - Add, edit, delete, and view members.
  - Search members by name or email.
  - Pagination for browsing members.
- **Responsive UI**:
  - Mobile-friendly and modern interface using Bootstrap.
- **Database Integration**:
  - SQLite database to store users, books, authors, and members.

---

## **Technologies Used**
- **Backend**: Flask (Python)
- **Database**: SQLite
- **Frontend**: HTML, CSS, JavaScript (Bootstrap)
- **Authentication**: Session-based login with password hashing.

---

## **Setup and Installation**

### **1. Clone the Repository**
```bash
git clone https://github.com/your-repo/library-management-system.git
cd library-management-system
```

### **2. Set Up a Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # For Linux/macOS
venv\Scripts\activate     # For Windows
```

### **3. Install Dependencies**
```bash
pip install flask werkzeug
```

### **4. Initialize the Database**
Run the following Python script to create the database and tables:
```bash
python -c "from models import init_db; init_db()"
```

### **5. Start the Application**
Run the Flask app:
```bash
python app.py
```

The application will be available at:
```
http://127.0.0.1:5000/
```

---

## **Project Structure**
```
library-management-system/
├── app.py                  # Main application file
├── models.py               # Database models and initialization
├── templates/              # HTML templates
│   ├── base.html           # Base layout
│   ├── index.html          # Homepage
│   ├── books.html          # Books listing page
│   ├── members.html        # Members listing page
│   ├── login.html          # Login page
│   ├── register.html       # Registration page
│   ├── edit_book.html      # Edit book page
│   ├── edit_member.html    # Edit member page
├── static/                 # Static files (CSS, JS)
├── README.md               # Project documentation
└── library.db              # SQLite database (auto-created)
```

---

## **Usage**

### **1. User Management**
- **Register**: Users can create accounts with a username and email.
- **Login**: Authenticate using their credentials.
- **Delete Account**: Users can delete their accounts after confirming a prompt.

### **2. Books Management**
- Add new books with a title, author, and language level.
- Edit book details.
- Delete books with a confirmation prompt.
- Search and filter books with pagination.

### **3. Members Management**
- Add new members with a name and email.
- Edit member details.
- Delete members with a confirmation prompt.
- Search members by name or email with pagination.

---

## **Key Functionalities**

### **1. Responsive UI**
The application uses Bootstrap to provide a mobile-friendly and visually appealing interface.

### **2. Confirmation Prompts**
JavaScript `confirm()` dialogs are implemented for account and member deletion to prevent accidental actions.

### **3. Session Management**
- Users remain logged in across sessions until they log out.
- Deleting a logged-in user's account automatically logs them out.

---

## **Development Process**

### **1. Backend**
- Created database models for `Books`, `Members`, and `Users`.
- Implemented Flask routes for CRUD operations and user authentication.

### **2. Frontend**
- Designed HTML templates with Bootstrap for a responsive UI.
- Added JavaScript confirmation dialogs for delete actions.

### **3. Error Handling**
- Implemented error handling for invalid inputs, database constraints, and missing data.

### **4. Testing**
- Manually tested all features, including:
  - User registration, login, and deletion.
  - Adding, editing, and deleting books and members.
  - Pagination and search functionality.

---

## **Future Enhancements**
- Add role-based access (e.g., admin vs. regular users).
- Implement advanced search and sorting for books and members.
- Add password recovery functionality.
- Migrate to a more scalable database like PostgreSQL.

---

## **License**
This project is licensed under the MIT License.
>>>>>>> 3ecbca3 (Initial commit for Library Management System)
