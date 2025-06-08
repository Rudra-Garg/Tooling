#!/usr/bin/env python3
# filepath: c:\Tools\ghextractall.py
import os
import re
import tempfile
import subprocess
import requests
import dotenv

dotenv.load_dotenv()

# ─────────────── Paths & Config ───────────────
SCRIPT_DIR        = os.path.dirname(os.path.abspath(__file__))
IGNORE_FILE       = os.path.join(SCRIPT_DIR, ".ignore")
OWNER_IGNORE_FILE = os.path.join(SCRIPT_DIR, ".ownerignore")
BRANCH_FILE       = os.path.join(SCRIPT_DIR, ".branch")

GITHUB_TOKEN      = os.environ["GITHUB_TOKEN"]

OUTPUT_DIR        = os.path.join(SCRIPT_DIR, "CONTENTS")

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
        parts.append(f"\nFilename: {f}\n")
        parts.append("Content:\n")
        try:
            if os.path.getsize(full) > 1_048_576:
                parts.append("[File too large to display]\n\n")
                continue
            text = open(full, encoding="utf-8", errors="strict").read()
            parts.append(text)
            parts.append("\n\n" + "="*80 + "\n")
        except (UnicodeDecodeError, PermissionError):
            parts.append("[Binary file - cannot display content]\n\n")
    return "".join(parts)

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

                out_file = os.path.join(
                    OUTPUT_DIR,
                    f"{owner}_{repo_name}_contents.txt"
                )
                with open(out_file, "w", encoding="utf-8") as fo:
                    fo.write(contents)

            print(f"{GREEN}✅{RESET}")
        except subprocess.TimeoutExpired:
            print(f"{RED}❌ Clone timeout{RESET}")
        except subprocess.CalledProcessError:
            print(f"{RED}❌ Git error{RESET}")
        except Exception as e:
            print(f"{RED}❌ {e}{RESET}")

    print(f"\n{BOLD}All done! Repository contents in: {OUTPUT_DIR}{RESET}")

if __name__ == "__main__":
    main()