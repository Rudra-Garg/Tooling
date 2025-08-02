```markdown
# Repository Summary: Rudra-Garg/portal-gambit-frontend

1.  **Project Goal & Core Functionality:**
    *   The project is a web frontend for playing "Portal Gambit," a variation of chess that incorporates portal mechanics. The primary purpose is to provide an interactive online platform for users to engage in this unique chess variant.
    *   Key features include:
        *   Portal Chess gameplay with custom chess engine.
        *   User authentication and profile management via Firebase.
        *   Real-time gameplay and chat features.

2.  **Technology Stack:**
    *   **Languages:** JavaScript/JSX.
    *   **Frameworks/Libraries:** React, Vite, Tailwind CSS, `chess.js`, `react-chessboard`, `framer-motion`, `peerjs`, `lucide-react`.
    *   **Key Dependencies:** Firebase Auth, Firebase Realtime Database. External Backend API via `VITE_BACKEND_URL`. P2P communication with `peerjs`.
    *   **Infrastructure/Ops:** Firebase Hosting (deployment), GitHub Actions (CI/CD).

3.  **Repository Structure Overview (Based on `tree.txt` if available, otherwise inferred):**
    *   `src/`: Contains the main application source code, including React components, contexts, hooks, and utility functions.
    *   `public/`: Holds static assets such as images, favicons, and potentially other static files.
    *   `.github/`: Contains GitHub Actions workflow configuration files.
    *   Key `src/` subdirectories:
        *   `components/`: React components, including game components (`PortalChessGame.jsx`, `CustomChessBoard.jsx`), UI elements, and auth components.
        *   `contexts/`: React context for authentication (`AuthContext.jsx`).
        *   `firebase/`: Firebase configuration (`config.js`).
        *   `hooks/`: Custom React hooks for managing game state and logic (e.g., game actions, game state, archiving).
        *   `utils/`: Utility functions (e.g., `profileUtils.js`, `animations.js`).
    *   Core application code likely resides in `src/App.jsx` and `src/components/game/`.
    *   Static assets are stored in `public/`.
    *   Test directories/files are absent in the provided input.

4.  **Key Files & Entry Points:**
    *   Configuration files: `package.json`, `vite.config.js`, `firebase.json`, `.firebaserc`, `tailwind.config.js`, `eslint.config.js`.
    *   Application entry points: `index.html`, `src/main.jsx`, `src/App.jsx`.
    *   Build/deployment-related files: `.github/workflows/firebase-hosting-merge.yml`, `.github/workflows/firebase-hosting-pull-request.yml`, `firebase.json`.
    *   Key application logic files: `src/components/game/PortalChessGame.jsx`, `src/components/game/CustomChessEngine.js`, `src/firebase/config.js`, `src/contexts/AuthContext.jsx`, `src/config.js`.
    *   The `README.md` file has minimal/generic content.

5.  **Development & Usage Hints (Inferred):**
    *   **Setup/Installation:** Run `npm ci` or `npm install` to install dependencies.
    *   **Running:** Run `npm run dev` to start the development server.
    *   **Building:** Run `npm run build` to create a production build in the `dist/` directory.
    *   **Deployment:**  GitHub Actions workflows deploy the `dist/` directory to Firebase Hosting.  Requires secrets for Firebase and `VITE_` prefixed environment variables (keys, domains, etc.) defined in `.github/workflows/*.yml`. The Github workflow also shows `VITE_BACKEND_URL` as a secret.
    *   **Testing:** Linting is performed using `npm run lint`. Other testing mechanisms are not apparent.

6.  **Notable Patterns & Conventions (Inferred):**
    *   React functional components with Hooks.
    *   Component-based architecture.
    *   Context API for managing authentication state (`AuthContext`).
    *   Utility/helper functions in `src/utils/`.
    *   Custom hooks in `src/hooks/`.
    *   Firebase for BaaS (Authentication and Realtime Database).
    *   Tailwind CSS utility classes for styling.
    *   Vite build tool.
    *   GitHub Actions for CI/CD.
    *   Environment variables using `.env` (present in `.gitignore`) and the `VITE_` prefix.
    *   Potential P2P communication (PeerJS for voice chat).
    *   External backend API dependency for authentication and potentially other services, configured via `VITE_BACKEND_URL`.

7.  **Overall Impression & Potential Use Case:**
    *   A web frontend for a custom "Portal Chess" game that utilizes React/Vite/Firebase, includes authentication, real-time features (gameplay and chat), CI/CD, voice chat and relies on a separate backend API.
```