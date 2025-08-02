```markdown
# Repository Summary: Rudra-Garg/TerraQuest-Backend

1.  **Project Goal & Core Functionality:**
    *   This project is a backend API server for a GeoGuessr clone game named "TerraQuest". It handles user authentication, game management (starting and finishing games), and potentially multiplayer functionalities, using a PostgreSQL database.
    *   Key features:
        *   User registration and authentication (JWT-based).
        *   Single-player game session management: fetching random locations and saving game results.
        *   Multiplayer game management (creating, joining games, getting game state) via WebSockets.

2.  **Technology Stack:**
    *   **Languages:** Go.
    *   **Frameworks/Libraries:** Gin (web framework), GORM (ORM), `golang-jwt/jwt` (JWT), `go-playground/validator` (input validation), `joho/godotenv` (environment variables), `swaggo` (Swagger documentation), `gorilla/websocket` (WebSockets), `gin-contrib/cors` (CORS).
    *   **Key Dependencies:** PostgreSQL (database), Google Maps Street View Metadata API (for locations), JWT for auth.
    *   **Infrastructure/Ops:** Dockerfile present.

3.  **Repository Structure Overview (Based on inferred structure):**
    *   `cmd/`: Contains the main application entry point (`server/main.go`).
    *   `internal/`: Contains application logic.
        *   `database/`: Database connection and migration logic.
        *   `handlers/`: API handler functions.
        *   `middleware/`: Middleware functions (e.g., authentication).
        *   `models/`: Data models for the application.
        *   `utils/`: Utility functions (e.g., token generation).
    *   `docs/`: Swagger API documentation related files.
    *   `scripts/`: Scripts to populate location data.

4.  **Key Files & Entry Points:**
    *   Configuration files: `go.mod`, `go.sum`, `.gitignore`, Dockerfile, various `.json` and `.yaml` files in `docs/`
    *   Application entry point: `cmd/server/main.go`
    *   Build/deployment-related files: Dockerfile
    *   Key application logic files:
        *   `internal/database/database.go`: Database connection setup.
        *   `internal/handlers/auth_handler.go`: Registration and login handlers.
        *   `internal/handlers/game_handler.go`: Single-player game handlers.
        *   `internal/handlers/multiplayer_handler.go`: Multiplayer game handlers and WebSocket handler.
        *   `internal/middleware/auth.go`: Authentication middleware.
        *   `internal/utils/token.go`: JWT token generation and validation.
        *   `scripts/populate_locations.go`: Script for populating location data in the database.
    *   Documentation files: `docs/docs.go`, `docs/swagger.json`, `docs/swagger.yaml`

5.  **Development & Usage Hints (Inferred):**
    *   **Setup/Installation:** `go mod download` or equivalent, configure environment variables.
    *   **Running:** `go run cmd/server/main.go`.
    *   **Building:** `go build cmd/server/main.go`.
    *   **Deployment:** A Dockerfile is present, suggesting containerized deployment.
    *   **Testing:** No specific testing mechanisms are apparent beyond linting by default.
    *   *Constraint:* There is not enough information available to comment on setting up CI/CD pipelines.

6.  **Notable Patterns & Conventions (Inferred):**
    *   REST API structure using Gin framework.
    *   Database interaction using GORM ORM.
    *   JWT-based authentication.
    *   Input validation using `go-playground/validator`.
    *   Environment variable configuration using `godotenv`.
    *   API documentation using Swagger.
    *   Use of a non-default logging level by using an environment variable `GORM_LOG_LEVEL`.

7.  **Overall Impression & Potential Use Case:**
    *   A backend API server built with Go for the "TerraQuest" GeoGuessr clone game, providing user authentication, game management, and multiplayer support through WebSockets, backed by a PostgreSQL database and leveraging the Google Maps Street View API.
```