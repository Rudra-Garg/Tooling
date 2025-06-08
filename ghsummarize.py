#!/usr/bin/env python3
import os
import re
import tempfile
import subprocess
import requests
import dotenv

from google import genai
from google.genai import types

dotenv.load_dotenv()

# ─────────────── Paths & Config ───────────────
SCRIPT_DIR        = os.path.dirname(os.path.abspath(__file__))
IGNORE_FILE       = os.path.join(SCRIPT_DIR, ".ignore")
OWNER_IGNORE_FILE = os.path.join(SCRIPT_DIR, ".ownerignore")
BRANCH_FILE       = os.path.join(SCRIPT_DIR, ".branch")

GITHUB_TOKEN      = os.environ["GITHUB_TOKEN"]
GEMINI_API_KEY    = os.environ["GEMINI_API_KEY"]
GEMINI_MODEL      = "gemini-2.0-flash"

OUTPUT_DIR        = os.path.join(SCRIPT_DIR, "SUMMARIES")

# ─────────────── Colour Codes ───────────────
RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
CYAN = "\033[36m"

# ─────────────── Helpers ───────────────
def load_branch_config(path):
    """Read repo-to-branch mappings from given file (format: owner/repo branch)."""
    branch_map = {}
    if not os.path.isfile(path):
        return branch_map
    
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            
            parts = line.split(None, 1)
            if len(parts) == 2:
                repo_key, branch = parts
                branch_map[repo_key] = branch
    
    return branch_map

def load_ignore_list(path):
    """Read one‑item per line exclusions from given file (ignores blank/#)."""
    if not os.path.isfile(path):
        return set()
    with open(path, "r", encoding="utf-8") as f:
        return {line.strip() for line in f if line.strip() and not line.startswith("#")}

def get_all_repos():
    """Fetch all repos (public + private) via GitHub API with pagination."""
    url     = "https://api.github.com/user/repos"
    params  = {"per_page": 100, "type": "all"}
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    repos   = []

    while url:
        resp = requests.get(url, headers=headers, params=params)
        resp.raise_for_status()
        repos.extend(resp.json())
        url    = resp.links.get("next", {}).get("url")
        params = None

    return repos

def get_repo_name(repo_url):
    """Extract repo name from its URL."""
    return re.sub(r'\.git$', '', repo_url.rstrip("/").split("/")[-1])

def clone_repo(repo_url, dest, branch=None):
    """Clone the repo and checkout specific branch if provided."""
    if branch:
        try:
            # Try to clone with specific branch
            subprocess.run(
                ["git", "clone", "--depth", "1", "--branch", branch, repo_url, dest],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE,
                timeout=60
            )
        except subprocess.CalledProcessError as e:
            # If specific branch clone fails, fall back to default branch
            print(f"\n{YELLOW}Branch '{branch}' not found, falling back to default branch...{RESET}", end=" ", flush=True)
            subprocess.run(
                ["git", "clone", "--depth", "1", repo_url, dest],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=60
            )
    else:
        # Standard clone of default branch
        subprocess.run(
            ["git", "clone", "--depth", "1", repo_url, dest],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=60
        )

def list_git_files(repo_path):
    """List all tracked files in the repo."""
    result = subprocess.run(
        ["git", "-C", repo_path, "ls-files"],
        stdout=subprocess.PIPE,
        text=True,
        check=True
    )
    return result.stdout.splitlines()

def extract_contents(repo_path):
    """Concatenate all tracked files into one big text (skips >1MB/binary)."""
    parts = []
    for f in list_git_files(repo_path):
        full = os.path.join(repo_path, f)
        parts.append(f"\n--- {f} ---\n")
        try:
            if os.path.getsize(full) > 1_048_576:
                parts.append("[SKIPPED: too large]\n")
                continue
            text = open(full, encoding="utf-8", errors="strict").read()
            parts.append(text + "\n")
        except (UnicodeDecodeError, PermissionError):
            parts.append("[SKIPPED: binary or unreadable]\n")
    return "".join(parts)

def summarize_with_gemini(owner, repo_name, text):
    """Send a prompt to Gemini and stream back the summary."""
    client = genai.Client(api_key=GEMINI_API_KEY)
    prompt = f"""
**Role:** Expert Software Engineer

**Task:** Analyze the provided repository contents for "{owner}/{repo_name}" and generate a concise, structured, and technical summary suitable for another developer quickly understanding the project's purpose, structure, and key characteristics.

**Input Context:** The input contains a concatenation of multiple file contents from the repository. Each file's content is preceded by a line starting with `Filename: ` and followed by `Content:`. Files are separated by lines of `================================================================================`. Some files might be marked as binary or too large to display. A `tree.txt` file providing a directory structure may also be included.

**Output Format:** Generate a summary in Markdown format, covering the following sections precisely:

---

# Repository Summary: {owner}/{repo_name}

1.  **Project Goal & Core Functionality:**
    *   Succinctly state the primary purpose of this project based on file names (e.g., `PortalChessGame.jsx`, `CustomChessEngine.js`), `package.json` (`name`), `index.html` (`title`), and any relevant README content. What problem does it solve or what does it enable?
    *   List 1-3 key features evident from component names, dependencies, or configuration (e.g., Portal Chess gameplay, Firebase Auth, Realtime Database interaction, Profile Management, CI/CD via GitHub Actions).

2.  **Technology Stack:**
    *   **Languages:** Primary programming languages detected (likely JavaScript/JSX based on file extensions).
    *   **Frameworks/Libraries:** Major frameworks/libraries identified from `package.json` dependencies (e.g., React, Vite, Firebase, Tailwind CSS, `chess.js`, `react-chessboard`, `peerjs`, `framer-motion`).
    *   **Key Dependencies:** Mention critical backend services suggested by imports or config (e.g., Firebase Auth, Firebase Realtime Database) and potentially P2P communication (PeerJS). Note any interaction with a separate backend API (look for `BACKEND_URL` usage).
    *   **Infrastructure/Ops:** Note tools like Docker (if `Dockerfile` present), CI/CD platforms (GitHub Actions based on `.github/workflows/`), and hosting platforms (Firebase Hosting based on `firebase.json` and workflows).

3.  **Repository Structure Overview (Based on `tree.txt` if available, otherwise inferred):**
    *   Describe the purpose of the main top-level directories (`src/`, `public/`, `.github/`).
    *   Describe the purpose of key `src/` subdirectories (e.g., `components/`, `contexts/`, `firebase/`, `hooks/`, `utils/`).
    *   Mention where the core application code likely resides (e.g., `src/App.jsx`, `src/components/game/`).
    *   Mention where static assets are stored (`public/`).
    *   Explicitly state if test directories/files are apparent or absent.

4.  **Key Files & Entry Points:**
    *   Identify crucial configuration files (`package.json`, `vite.config.js`, `firebase.json`, `.firebaserc`, `tailwind.config.js`, `eslint.config.js`).
    *   Identify application entry points (`index.html`, `src/main.jsx`, `src/App.jsx`).
    *   Point out build/deployment-related files (`.github/workflows/*.yml`, `firebase.json`).
    *   Mention key application logic files (e.g., `src/components/game/PortalChessGame.jsx`, `src/components/game/CustomChessEngine.js`, `src/firebase/config.js`, `src/contexts/AuthContext.jsx`, `src/config.js`).
    *   Mention the main documentation file (`README.md`, note if its content is minimal/generic).

5.  **Development & Usage Hints (Inferred):**
    *   **Setup/Installation:** Infer setup steps from `package.json` scripts and workflow files (e.g., `npm ci` or `npm install`).
    *   **Running:** Infer run command from `package.json` scripts (e.g., `npm run dev`).
    *   **Building:** Infer build command from `package.json` scripts and workflows (e.g., `npm run build`). Note the output directory (`dist/` based on `vite.config.js`).
    *   **Deployment:** Describe deployment process inferred from workflows (e.g., GitHub Actions deploying `dist/` to Firebase Hosting). Mention required secrets/env vars (e.g., `VITE_FIREBASE_*`, `VITE_BACKEND_URL`).
    *   **Testing:** Mention linting (`npm run lint`). State if other testing mechanisms are suggested or absent.
    *   *Constraint:* State clearly if information is not directly found in the provided input.

6.  **Notable Patterns & Conventions (Inferred):**
    *   Mention observed patterns: React functional components with Hooks, component-based architecture, context API for state (`AuthContext`), utility/helper functions (`src/utils/`), custom hooks (`src/hooks/`), Firebase for BaaS, Tailwind CSS utility classes, Vite build tool, GitHub Actions CI/CD, use of environment variables (`.env` in `.gitignore`, `VITE_` prefix), potential P2P communication (PeerJS). Dependence on an external backend API.
    *   *Constraint:* Only report patterns strongly suggested by file names, configurations, or code snippets.

7.  **Overall Impression & Potential Use Case:**
    *   A brief concluding sentence summarizing the project type (e.g., "A web frontend for a custom 'Portal Chess' game") and its key characteristics (e.g., "Utilizes React/Vite/Firebase, includes authentication, real-time features, CI/CD, and depends on a separate backend API.").

---

**Instructions for the AI:**
*   Adhere strictly to the requested Markdown format and sections.
*   Base your analysis *solely* on the provided input, parsing the `Filename:` and `Content:` structure.
*   Do *not* attempt to interpret binary file contents; acknowledge their presence if listed.
*   If information for a specific point is missing or unclear in input, explicitly state that (e.g., "Test setup not specified.").
*   Prioritize information from key files like `package.json`, `vite.config.js`, `firebase.json`, `.github/workflows/`, `src/App.jsx`, `src/components/game/CustomChessEngine.js`, `src/config.js`, and `tree.txt` when available.
*   Synthesize information across multiple files (e.g., connect `package.json` scripts with workflow steps).
*   Maintain a neutral, technical tone.

Here is the input:
{text}
"""
    contents = [
        types.Content(
            role="user",
            parts=[types.Part(text=prompt)]
        )
    ]
    cfg = types.GenerateContentConfig(response_mime_type="text/plain")
    summary_chunks = client.models.generate_content_stream(
        model=GEMINI_MODEL,
        contents=contents,
        config=cfg
    )
    return "".join(chunk.text for chunk in summary_chunks)


# ─────────────── Main ───────────────
def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    repo_ignore_set   = load_ignore_list(IGNORE_FILE)
    owner_ignore_set  = load_ignore_list(OWNER_IGNORE_FILE)
    branch_config     = load_branch_config(BRANCH_FILE)

    repos = get_all_repos()
    print(f"{CYAN}Found {len(repos)} repos — skipping {len(repo_ignore_set)} by name and {len(owner_ignore_set)} by owner.{RESET}")
    print(f"{CYAN}Using {len(branch_config)} branch specifications from {BRANCH_FILE}.{RESET}\n")

    for repo in repos:
        owner    = repo["owner"]["login"]
        repo_url = repo["clone_url"]
        repo_name= get_repo_name(repo_url)
        repo_key = f"{owner}/{repo_name}"

        if owner in owner_ignore_set:
            print(f"{YELLOW}→ {repo_key}  (skipped via .ownerignore){RESET}")
            continue
        if repo_name in repo_ignore_set:
            print(f"{YELLOW}→ {repo_key}  (skipped via .ignore){RESET}")
            continue

        # Get specific branch for this repo if defined
        branch = branch_config.get(repo_key)
        branch_info = f" (branch: {branch})" if branch else ""
        
        print(f"{CYAN}→ {repo_key}{branch_info}…{RESET}", end=" ", flush=True)
        try:
            with tempfile.TemporaryDirectory() as td:
                clone_repo(repo_url, td, branch)
                contents = extract_contents(td)
                summary  = summarize_with_gemini(owner, repo_name, contents)

                out_file = os.path.join(
                    OUTPUT_DIR,
                    f"{owner}_{repo_name}_summary.md"
                )
                with open(out_file, "w", encoding="utf-8") as fo:
                    fo.write(summary)

            print(f"{GREEN}✅{RESET}")
        except subprocess.TimeoutExpired:
            print(f"{RED}❌ Clone timeout{RESET}")
        except subprocess.CalledProcessError:
            print(f"{RED}❌ Git error{RESET}")
        except Exception as e:
            print(f"{RED}❌ {e}{RESET}")

    print(f"\n{BOLD}All done! Summaries in: {OUTPUT_DIR}{RESET}")

if __name__ == "__main__":
    main()
