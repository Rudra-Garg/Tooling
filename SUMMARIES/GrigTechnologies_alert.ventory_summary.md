```markdown
# Repository Summary: GrigTechnologies/alert.ventory

1.  **Project Goal & Core Functionality:**
    *   This project is a microservice designed to handle the alert system for Ventory. It manages user authentication via Zoho, email notifications using Temporal workflows, data storage with Supabase, and role-based access control.
    *   Key features include: User Authentication (Zoho OAuth2, JWT), Temporal Workflows for Emails (priority queues, optional verification, scheduled/recurring notifications), and File Storage (Supabase Storage).

2.  **Technology Stack:**
    *   **Languages:** Python (3.12), Bash (for entrypoint script and Dockerfiles)
    *   **Frameworks/Libraries:** FastAPI, Temporal, SQLAlchemy, Alembic, Supabase Python library, PyJWT, Pydantic.
    *   **Key Dependencies:** Zoho OAuth2 for authentication, PostgreSQL for database, Temporal for workflow orchestration, Supabase Storage for file storage, SMTP server for email sending.
    *   **Infrastructure/Ops:** Docker (Dockerfile present), docker-compose, Supabase (including Auth, Storage, Realtime, and Functions), Temporal, Prometheus and Grafana (for monitoring), Logflare (for analytics).

3.  **Repository Structure Overview (Based on `tree.txt`):**
    *   `LICENSE`: Contains the project license (Grig Technologies internal use only).
    *   `README.md`: Main documentation file.
    *   `activities/`: Contains Temporal activity definitions.
    *   `configs/`: Contains application configuration files (DB, JWT, SMTP, roles.json).
    *   `controllers/`: Contains business logic handlers for API routes.
    *   `docker/`: Contains Docker-related files, including Dockerfiles, docker-compose.yml, Prometheus config, and dynamic Temporal config.
    *   `handlers/`: Contains global exception handlers.
    *   `logs/`: Stores runtime log files.
    *   `models/`: Contains SQLAlchemy database models and initialization logic.
    *   `routes/`: Contains FastAPI routers defining API endpoints.
    *   `schemas/`: Contains Pydantic models for API request/response validation.
    *   `tests/`: Contains automated tests.
    *   `utils/`: Contains shared utility functions (JWT, Zoho token helpers).
    *   `workers/`: Contains Temporal worker definitions.
    *   `workflows/`: Contains Temporal workflow definitions.
    * Core application code likely resides in `controllers/`, `models/`, `routes/`, `workflows/`, and `workers/`. Static assets are not apparent in the directory structure.

4.  **Key Files & Entry Points:**
    *   Configuration files: `docker/.env.example`, `docker/docker-compose.yml`, `alembic.ini`, `configs/database.py`, `configs/jwt_config.py`, `configs/smtp_config.py`, `configs/roles_permissions.json`, `docker/prometheus/prometheus.yml`, `docker/dynamicconfig/*.yaml`, `docker/volumes/api/kong.yml`, `docker/volumes/pooler/pooler.exs`.
    *   Application entry points: `run_api.py` (FastAPI server), `run_worker.py` (Temporal workers), `entrypoint.sh` (Docker entrypoint).
    *   Build/Deployment: `Dockerfile`, `docker/docker-compose.yml`.
    *   Key application logic: `controllers/*`, `models/*`, `routes/*`, `workflows/*`, `workers/*`.
    *   Documentation: `README.md` appears detailed.

5.  **Development & Usage Hints (Inferred):**
    *   **Setup/Installation:** Requires Python 3.12+, Docker, access to Temporal/PostgreSQL/Zoho. Setup involves cloning the repository, creating a `.env` file, installing dependencies (`pip install -r requirements.txt`).
    *   **Running:** API server: `python run_api.py` or `uvicorn run_api:app --host 0.0.0.0 --port 8123 --reload`. Temporal workers: `python run_worker.py`. Docker: `docker compose up -d`.
    *   **Building:** `docker buildx build --platform linux/amd64 -t <image_name> --push .` from the project root.
    *   **Deployment:** Docker Compose for local development, Docker for deployment. Requires environment variables for DB, Zoho, SMTP, JWT, etc. `entrypoint.sh` determines service type (API or worker).
    *   **Testing:** Uses `pytest`. Run tests with `pytest` from the root directory. Includes linting and static type checking, though command is not specified.
    *   `Pip-compile` is recommended.

6.  **Notable Patterns & Conventions (Inferred):**
    *   FastAPI application using Pydantic for data validation.
    *   SQLAlchemy for database interaction.
    *   Alembic for database migrations.
    *   JWT for authentication.
    *   Role-Based Access Control (RBAC) implemented in models and controllers.
    *   Temporal workflows and activities for managing asynchronous tasks, especially email sending.
    *   Docker and Docker Compose for containerization and orchestration.
    *   Supabase used for backend services: Storage, Auth and Realtime.
    *   Logging via the `logging` module with rotating file handlers.
    *   Configuration via environment variables.
    *   Service type selection via `SERVICE_TYPE` environment variable.

7.  **Overall Impression & Potential Use Case:**
    *   A Python-based microservice ("alert.ventory") implementing an alert and notification system, leveraging FastAPI, Temporal workflows, Supabase, and Zoho authentication, packaged for deployment with Docker.
```