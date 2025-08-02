# Repository Summary: Rudra-Garg/Ventory_T2

1.  **Project Goal & Core Functionality:**
    *   The project is a Certificate Manager that allows for the creation and searching of certificates stored in Google Cloud Storage.
    *   Key features: Certificate creation via a web form, certificate storage in Google Cloud Storage, certificate search by name, email, or ID.

2.  **Technology Stack:**
    *   **Languages:** Python (Flask), HTML, CSS, JavaScript
    *   **Frameworks/Libraries:** Flask, OpenCV (`cv2`), Pillow, img2pdf, Firebase Admin SDK
    *   **Key Dependencies:** Google Cloud Storage, Firebase Firestore
    *   **Infrastructure/Ops:** No Dockerfile is present in the provided input.

3.  **Repository Structure Overview (Based on inferred structure):**
    *   The repository likely contains the following top-level directories: the main application file (`app.py`), a `static/` directory for static assets, a `templates/` directory for HTML templates, and potentially directories for certificate outputs (`output_pdfs/`) and temporary files (`temporary/`).
    *   `static/` likely holds CSS files (`static/css/`), JavaScript files (`static/script.js`), and image assets (`static/logo.png`).
    *   `templates/` likely holds HTML templates for the admin interface (`templates/index.html`) and certificate display (`templates/certificate.html`).
    *   The core application logic resides in `app.py`.
    *   The location of static assets is `static/`.
    *   Test directories/files are not apparent.

4.  **Key Files & Entry Points:**
    *   Configuration files: `requirements.txt`, `firebase_config.py`.
    *   Application entry points: `app.py` (Flask application).
    *   Build/deployment related files: Not directly present in provided input.
    *   Key application logic files: `app.py` (routes, certificate generation), `firebase_config.py` (Firebase initialization).
    *   Main documentation file: `README.md`

5.  **Development & Usage Hints (Inferred):**
    *   **Setup/Installation:** `pip install requirements.txt`
    *   **Running:** `python app.py`
    *   **Building:** Not specified.
    *   **Deployment:** Not specified. Requires Firebase project configuration to be updated in `firebase_config.py`. Authentication key for API access is printed at application startup.
    *   **Testing:** Linting or other testing mechanisms are not suggested.

6.  **Notable Patterns & Conventions (Inferred):**
    *   Flask web application, REST API endpoints for creating and searching certificates, Firebase for database and storage, use of OpenCV and Pillow for image manipulation, templating engine for rendering HTML, front-end form handling with JavaScript.

7.  **Overall Impression & Potential Use Case:**
    *   A web application for managing digital certificates, leveraging Flask as a backend framework, Firebase for BaaS (database and storage), and a client-side JavaScript for interacting with the backend. The application depends on Google Cloud Storage for certificate persistence.
