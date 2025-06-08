#!/usr/bin/env python3
import os
import subprocess
import argparse
import dotenv
from google import genai
from google.genai import types

dotenv.load_dotenv()

# ─────────────── Paths & Config ───────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.getcwd()  # Changed to current working directory
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GEMINI_MODEL = "gemini-2.0-flash"

# ─────────────── Color Codes ───────────────
RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
CYAN = "\033[36m"

# ─────────────── Helpers ───────────────
def list_git_files(repo_path):
    """List all files tracked by git in a repository."""
    original_dir = os.getcwd()
    try:
        os.chdir(repo_path)
        result = subprocess.run(
            ['git', 'ls-files'], 
            stdout=subprocess.PIPE, 
            text=True, 
            check=True
        )
        return result.stdout.splitlines()
    finally:
        os.chdir(original_dir)

def extract_contents(repo_path):
    """Extract all git-tracked files' contents into a formatted string."""
    files = list_git_files(repo_path)
    parts = []
    
    for file_path in files:
        full_path = os.path.join(repo_path, file_path)
        parts.append(f"\nFilename: {file_path}\nContent:\n")
        
        try:
            # Skip binary files, large files, or files that can't be read as text
            if os.path.getsize(full_path) > 1_048_576:  # Skip files > 1MB
                parts.append("[File too large to display]\n")
                continue
                
            # Try to read the file
            with open(full_path, 'r', encoding='utf-8', errors='strict') as file:
                content = file.read()
                parts.append(content)
                
            parts.append("\n\n" + "=" * 80 + "\n")
        except UnicodeDecodeError:
            parts.append("[Binary file - cannot display content]\n")
        except Exception as e:
            parts.append(f"[Error reading file: {str(e)}]\n")
    
    return "".join(parts)

def get_repo_info(repo_path):
    """Extract owner and repo name from the git remote URL."""
    original_dir = os.getcwd()
    try:
        os.chdir(repo_path)
        result = subprocess.run(
            ['git', 'remote', 'get-url', 'origin'], 
            stdout=subprocess.PIPE, 
            text=True, 
            check=True
        )
        remote_url = result.stdout.strip()
        
        # Parse the remote URL to extract owner and repo name
        # Handles both HTTPS and SSH formats
        if remote_url.startswith('https://'):
            parts = remote_url.split('/')
            owner = parts[-2]
            repo_name = parts[-1].replace('.git', '')
        else:  # SSH format: git@github.com:owner/repo.git
            parts = remote_url.split(':')[-1].split('/')
            owner = parts[-2] if len(parts) > 1 else None
            repo_name = parts[-1].replace('.git', '')
            
        return owner, repo_name
    except subprocess.CalledProcessError:
        # If no remote URL exists, use directory name as repo name
        repo_name = os.path.basename(os.path.abspath(repo_path))
        return "local", repo_name
    finally:
        os.chdir(original_dir)

def summarize_with_gemini(owner, repo_name, text):
    """Send a prompt to Gemini and stream back the summary."""
    if not GEMINI_API_KEY:
        print(f"{RED}Error: GEMINI_API_KEY environment variable not set{RESET}")
        return "Error: GEMINI_API_KEY not set. Please set this environment variable with your API key."
    
    client = genai.Client(api_key=GEMINI_API_KEY)
    prompt = f"""
**Role:** Expert Software Engineer

**Task:** Analyze the provided repository contents for "{owner}/{repo_name}" and generate a concise, structured, and technical summary suitable for another developer quickly understanding the project's purpose, structure, and key characteristics.

**Input Context:** The input contains a concatenation of multiple file contents from the repository. Each file's content is preceded by a line starting with `Filename: ` and followed by `Content:`. Files are separated by lines of `================================================================================`. Some files might be marked as binary or too large to display. A `tree.txt` file providing a directory structure may also be included.

**Output Format:** Generate a summary in Markdown format, covering the following sections precisely:

---

# Repository Summary: {owner}/{repo_name}

1.  **Project Goal & Core Functionality:**
    *   Succinctly state the primary purpose of this project based on file names, `package.json` (`name`), `index.html` (`title`), and any relevant README content. What problem does it solve or what does it enable?
    *   List 1-3 key features evident from component names, dependencies, or configuration.

2.  **Technology Stack:**
    *   **Languages:** Primary programming languages detected.
    *   **Frameworks/Libraries:** Major frameworks/libraries identified from dependencies.
    *   **Key Dependencies:** Mention critical backend services suggested by imports or config.
    *   **Infrastructure/Ops:** Note tools like Docker, CI/CD platforms, and hosting platforms.

3.  **Repository Structure Overview (Based on `tree.txt` if available, otherwise inferred):**
    *   Describe the purpose of the main top-level directories.
    *   Describe the purpose of key subdirectories.
    *   Mention where the core application code likely resides.
    *   Mention where static assets are stored.
    *   Explicitly state if test directories/files are apparent or absent.

4.  **Key Files & Entry Points:**
    *   Identify crucial configuration files.
    *   Identify application entry points.
    *   Point out build/deployment-related files.
    *   Mention key application logic files.
    *   Mention the main documentation file.

5.  **Development & Usage Hints (Inferred):**
    *   **Setup/Installation:** Infer setup steps from scripts and workflow files.
    *   **Running:** Infer run command from scripts.
    *   **Building:** Infer build command from scripts and workflows.
    *   **Deployment:** Describe deployment process inferred from workflows.
    *   **Testing:** Mention testing mechanisms.
    *   State clearly if information is not directly found in the provided input.

6.  **Notable Patterns & Conventions (Inferred):**
    *   Mention observed patterns and conventions.
    *   Only report patterns strongly suggested by file names, configurations, or code snippets.

7.  **Overall Impression & Potential Use Case:**
    *   A brief concluding sentence summarizing the project type and its key characteristics.

---

**Instructions for the AI:**
*   Adhere strictly to the requested Markdown format and sections.
*   Base your analysis *solely* on the provided input.
*   Do *not* attempt to interpret binary file contents; acknowledge their presence if listed.
*   If information for a specific point is missing or unclear in input, explicitly state that.
*   Prioritize information from key files when available.
*   Synthesize information across multiple files.
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
    try:
        summary_chunks = client.models.generate_content_stream(
            model=GEMINI_MODEL,
            contents=contents,
            config=cfg
        )
        return "".join(chunk.text for chunk in summary_chunks)
    except Exception as e:
        print(f"{RED}Error calling Gemini API: {e}{RESET}")
        return f"Error generating summary: {e}"

def main():
    parser = argparse.ArgumentParser(description='Extract and summarize a git repository')
    parser.add_argument('repo_path', help='Path to the git repository')
    parser.add_argument('--output', '-o', help='Output file (default: auto-generated based on repo name)')
    parser.add_argument('--extract-only', '-e', action='store_true', help='Only extract contents without summarizing')
    
    args = parser.parse_args()
    
    # Validate repository path
    if not os.path.exists(args.repo_path):
        print(f"{RED}Error: Repository path '{args.repo_path}' does not exist{RESET}")
        exit(1)
        
    if not os.path.exists(os.path.join(args.repo_path, '.git')):
        print(f"{RED}Error: '{args.repo_path}' is not a git repository{RESET}")
        exit(1)
    
    # Create output directory if needed
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Get repository info
    owner, repo_name = get_repo_info(args.repo_path)
    
    # Determine output file path
    if args.output:
        output_file = args.output
    else:
        if args.extract_only:
            output_file = f"{owner}_{repo_name}_contents.txt"
        else:
            output_file = os.path.join(OUTPUT_DIR, f"{owner}_{repo_name}_summary.md")
    
    print(f"{CYAN}Extracting files from {args.repo_path}...{RESET}")
    contents = extract_contents(args.repo_path)
    
    if args.extract_only:
        # Save extracted contents to file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(contents)
        print(f"{GREEN}Done! Repository contents saved to {output_file}{RESET}")
    else:
        # Summarize and save
        print(f"{CYAN}Summarizing repository {owner}/{repo_name}...{RESET}")
        summary = summarize_with_gemini(owner, repo_name, contents)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(summary)
        
        print(f"{GREEN}Done! Summary saved to {output_file}{RESET}")

if __name__ == "__main__":
    main()