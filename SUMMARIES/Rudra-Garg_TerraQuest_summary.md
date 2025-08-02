```markdown
# Repository Summary: Rudra-Garg/TerraQuest

1.  **Project Goal & Core Functionality:**
    *   The project is a geography guessing game ("GeoGuessr" in `package.json` name, "TerraQuest" in `index.html` title and `README.md`) that uses Google Street View. The goal is to explore locations and pinpoint them on a map.
    *   Key Features: Interactive Street View experience, Real-time map interaction, Score system, User Authentication, Leaderboard system, Responsive design, Multiplayer Support.

2.  **Technology Stack:**
    *   **Languages:** JavaScript/JSX/Vue.js.
    *   **Frameworks/Libraries:** Vue 3, Vite, Pinia, Tailwind CSS, Leaflet, Google Maps API, `vue-router`.
    *   **Key Dependencies:** Axios for API requests, Google Maps API for Street View, backend API via `VITE_BACKEND_URL`.
    *   **Infrastructure/Ops:** GitHub Pages for hosting, GitHub Actions for CI/CD, environment variables (`VITE_GOOGLE_MAPS_API_KEY`, `VITE_BACKEND_URL`).

3.  **Repository Structure Overview (Based on inferred structure):**
    *   `src/`: Contains the main application code.
    *   `public/`: Contains static assets (e.g., `vite.svg`, `vue.svg`).
    *   `.github/`: Contains GitHub Actions workflow files.
    *   `src/components/`: Contains reusable Vue components (e.g., `MapDisplay.vue`, `StreetViewDisplay.vue`).
    *   `src/views/`: Contains page components (e.g., `HomeView.vue`, `GameView.vue`, `LoginView.vue`).
    *   `src/stores/`: Contains Pinia state management stores (e.g., `AuthStore.js`, `GameStore.js`, `MultiplayerStore.js`).
    *   `src/services/`: Contains API services (e.g., `authService.js`, `gameService.js`).
    *   `src/router/`: Contains Vue Router configuration (`index.js`).
    *   `src/assets/`: Contains static assets.
    *   Test directories/files are not apparent.

4.  **Key Files & Entry Points:**
    *   Configuration Files: `package.json`, `vite.config.js`, `tailwind.config.js`.
    *   Application Entry Points: `index.html`, `src/main.js`, `src/App.vue`.
    *   Build/Deployment Files: `.github/workflows/deploy.yml`.
    *   Key Application Logic Files: `src/App.vue`, `src/components/MapDisplay.vue`, `src/components/StreetViewDisplay.vue`, `src/router/index.js`, `src/stores/AuthStore.js`, `src/stores/GameStore.js`, `src/services/authService.js`, `src/services/gameService.js`.
    *   Main Documentation File: `README.md` (contains project description, features, setup instructions, and build tools).

5.  **Development & Usage Hints (Inferred):**
    *   **Setup/Installation:** `npm install` or `npm ci` (from `deploy.yml`).
    *   **Running:** `npm run dev`.
    *   **Building:** `npm run build`. Output directory: `dist/`.
    *   **Deployment:** GitHub Actions deploying `dist/` to GitHub Pages (based on `.github/workflows/deploy.yml`). Requires secrets: `GOOGLE_MAPS_API_KEY`, `BACKEND_URL`.
    *   **Testing:** Linting/testing mechanisms are not explicitly specified.

6.  **Notable Patterns & Conventions (Inferred):**
    *   Vue components with composition API (`<script setup>`).
    *   Pinia for state management.
    *   Component-based architecture.
    *   Tailwind CSS utility classes.
    *   Vite build tool.
    *   GitHub Actions for CI/CD.
    *   Use of environment variables (`VITE_` prefix).
    *   Separate API service files.
    *   Router guards for authentication.

7.  **Overall Impression & Potential Use Case:**
    A web frontend for a geography guessing game utilizing Vue/Vite/Pinia/Tailwind CSS and Google Maps API. Includes user authentication, session management, multiplayer functionality, and depends on a separate backend API for game logic and data persistence, and Google Maps API for location and map rendering.
```