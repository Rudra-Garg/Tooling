```markdown
# Repository Summary: Rudra-Garg/Attendance-DBMS

1.  **Project Goal & Core Functionality:**
    *   The project aims to provide an attendance management system accessible to students, faculty, and administrators, built with Flask backend and MySQL database.
    *   Key features include: User authentication (login), Attendance recording/tracking, Leave application management, Report generation of defaulters (students with low attendance), Admin panel to manage users/subjects.

2.  **Technology Stack:**
    *   **Languages:** Python.
    *   **Frameworks/Libraries:** Flask, MySQL Connector.
    *   **Key Dependencies:** MySQL database for storing user data, attendance records, and leave applications.
    *   **Infrastructure/Ops:** No explicit mention of Docker or CI/CD.

3.  **Repository Structure Overview (Inferred):**
    *   `app/`: Contains the Flask application's Python code. This likely holds routes, models, and business logic.
    *   `static/`: Stores static assets (CSS, JavaScript, Images) for the web interface.
    *   `templates/`: Stores HTML templates used by Flask to render the web pages.
    *   Test directories/files are absent.

4.  **Key Files & Entry Points:**
    *   Configuration files: `dbmsProject.sql` (MySQL database schema), `requirements.txt` (but content skipped).
    *   Application entry points: `main.py` (Flask app initialization).
    *   Key application logic files:
        *   `app/__init__.py`: Imports blueprints for different modules.
        *   `app/admin.py`: Admin-related routes (add/remove users, subjects).
        *   `app/faculty.py`: Faculty-related routes (mark attendance, view leave requests).
        *   `app/student.py`: Student-related routes (view attendance, submit leave requests).
        *   `app/login.py`: Login functionality.
        *   `app/connection.py`: MySQL database connection configuration.
    *   Documentation file: `README.md` (content likely minimal).

5.  **Development & Usage Hints (Inferred):**
    *   **Setup/Installation:** Install dependencies using `pip install -r requirements.txt` (assuming `requirements.txt` exists).
    *   **Running:** Run the Flask application using `python main.py` or `python main_old` with debug mode enabled (`app.run(debug=True)`).
    *   **Building:** Build process is not explicitly defined. It's likely a manual deployment of the Flask app and associated assets.
    *   **Deployment:** Deployment process is not explicitly defined.
    *   **Testing:** Testing mechanisms are absent.

6.  **Notable Patterns & Conventions (Inferred):**
    *   Flask blueprints for organizing routes (admin, faculty, student, login).
    *   Database interaction through `mysql.connector`.
    *   Templating using Jinja2 (Flask's default).
    *   Static assets served from the `static/` directory.
    *   URL-based userID passing for authentication and authorization.

7.  **Overall Impression & Potential Use Case:**
    *   This is a Flask-based web application for managing student attendance, targeted for use by students, faculty, and administrators. It uses a MySQL database for data persistence and offers features like attendance tracking, leave applications, and user management.
```