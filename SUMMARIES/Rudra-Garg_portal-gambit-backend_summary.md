```markdown
# Repository Summary: Rudra-Garg/portal-gambit-backend

1.  **Project Goal & Core Functionality:**
    *   The project is a RESTful API backend service for a "Portal Gambit" chess variant game, offering user profile management, friend system, game history tracking, and analytics. It uses Firebase Authentication for secure access.
    *   Key features include: User profile management, Friend system, Game history tracking, Firebase Authentication.

2.  **Technology Stack:**
    *   **Languages:** Python.
    *   **Frameworks/Libraries:** FastAPI, Firebase Admin SDK, Uvicorn, Pydantic, Python-dotenv.
    *   **Key Dependencies:** Firebase Authentication, Firebase Admin SDK, FastAPI's CORSMiddleware.
    *   **Infrastructure/Ops:** Docker (Dockerfile present), Cloud Build (cloudbuild.yaml present), Google Cloud Run.

3.  **Repository Structure Overview (Based on explicit content):**
    *   `config/`: Contains configuration files, including Firebase credentials and a script to decode environment variables.
    *   `middleware/`: Contains custom middleware, notably `auth_middleware.py` for Firebase Authentication.
    *   `models/`: Defines data models (e.g., `user_profile.py`, `friend.py`, `game_history.py`) using Pydantic.
    *   `routes/`: Contains API route handlers for profiles, friends, history, analytics, and authentication (e.g., `profile_routes.py`, `friend_routes.py`).
    *   `schemas/`: Defines Pydantic schemas for request and response validation (e.g., `profile_schemas.py`, `friend_schemas.py`).
    *   `services/`: Implements business logic and data access (e.g., `profile_service.py`, `friend_service.py`) using Firebase Firestore.
    *   `utils/`: Contains utility functions, including JWT handling and dependency injection (`jwt_utils.py`, `dependencies.py`).
    *   `.env`: Used to store environment variables. Note: this file is git ignored.
    *   `main.py`: The application entry point.
    *   `tests/`: Contains test files. Test files are separated into api blackbox and integration whitebox tests.

4.  **Key Files & Entry Points:**
    *   Configuration files: `requirements.txt`, `.env`, `cloudbuild.yaml`, `config/firebase_config.json`, `config/firebase_config.py`, `pytest.ini`, `Dockerfile`.
    *   Application entry points: `main.py`.
    *   Build/deployment-related files: `Dockerfile`, `cloudbuild.yaml`, `run.sh`.
    *   Key application logic files:
        *   `routes/*`: define all endpoints.
        *   `middleware/auth_middleware.py`: Firebase Authentication.
        *   `models/*`: defining all models of the system.
        *   `services/*`: business logic, specifically handling data processing and persistance to the database.
        *   `utils/*`: containing utility and dependency injection files.
    *   Documentation: `README.md` (provides overview, features, tech stack, and setup instructions).

5.  **Development & Usage Hints (Inferred):**
    *   **Setup/Installation:** `pip install -r requirements.txt` (inside a virtual environment is recommended).
    *   **Running:** `python main.py` or `uvicorn main:app --reload`.
    *   **Building:** No explicit build step mentioned. The Dockerfile implies a build process when creating the container.
    *   **Deployment:** Google Cloud Run via Cloud Build, defined in `cloudbuild.yaml`. Requires secrets `JWT_SECRET_KEY` and `FIREBASE_CONFIG_STRING` to be configured in Google Cloud Secret Manager.
    *   **Testing:** `pytest` for unit and integration tests. `pylint` is not explicitly used but can be used for linting.
    *   Information about linting not directly found in provided input.

6.  **Notable Patterns & Conventions (Inferred):**
    *   FastAPI framework for API development.
    *   Pydantic for data validation and serialization.
    *   Firebase Admin SDK for backend Firebase interactions (authentication, Firestore).
    *   Dependency injection using FastAPI's `Depends` to inject services into route handlers.
    *   Middleware for authentication and CORS configuration.
    *   RESTful API design with clear separation of concerns (routes, services, models).
    *   Use of asynchronous operations (`async/await`).
    *   Comprehensive test suite covering both unit and integration aspects.
    *   Dockerization for containerized deployment.
    *   Cloud Build for CI/CD.

7.  **Overall Impression & Potential Use Case:**
    *   This is a robust backend API for a "Portal Gambit" chess game, built with FastAPI and Firebase, featuring user management, game history, analytics, authentication, automated deployment and testing.
```