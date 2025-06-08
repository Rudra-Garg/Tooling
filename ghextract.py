#!/usr/bin/env python3
import os
import subprocess
import argparse
import tempfile
import shutil
import re

def clone_repo(repo_url, temp_dir):
    """Clone the GitHub repository to a temporary directory."""
    print(f"Cloning {repo_url} into {temp_dir}...")
    subprocess.run(['git', 'clone', '--depth', '1', repo_url, temp_dir], check=True)

def get_repo_name(repo_url):
    """Extract repo name from the GitHub URL."""
    return re.sub(r'\.git$', '', repo_url.strip().split('/')[-1])

def list_git_files(repo_path):
    """List all files tracked by git in a repository."""
    result = subprocess.run(['git', '-C', repo_path, 'ls-files'],
                            stdout=subprocess.PIPE,
                            text=True,
                            check=True)
    return result.stdout.splitlines()

def extract_git_contents(repo_path, output_file):
    """Extract all git-tracked files' names and contents to a text file."""
    files = list_git_files(repo_path)

    with open(output_file, 'w', encoding='utf-8') as f:
        for file_path in files:
            full_path = os.path.join(repo_path, file_path)
            try:
                if os.path.getsize(full_path) > 1024 * 1024:  # Skip large files
                    f.write(f"\nFilename: {file_path}\n")
                    f.write("Content: [File too large to display]\n\n")
                    continue

                with open(full_path, 'r', encoding='utf-8') as file:
                    content = file.read()

                f.write(f"\nFilename: {file_path}\n")
                f.write("Content:\n")
                f.write(content)
                f.write("\n\n" + "="*80 + "\n")
            except UnicodeDecodeError:
                f.write(f"\nFilename: {file_path}\n")
                f.write("Content: [Binary file - cannot display content]\n\n")
            except Exception as e:
                f.write(f"\nFilename: {file_path}\n")
                f.write(f"Error reading file: {str(e)}\n\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract contents from a GitHub repo URL')
    parser.add_argument('repo_url', help='GitHub repository URL')
    parser.add_argument('--output', '-o', help='Optional output filename')

    args = parser.parse_args()
    repo_name = get_repo_name(args.repo_url)
    output_file = args.output or f"{repo_name}_contents.txt"

    original_cwd = os.getcwd()

    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            clone_repo(args.repo_url, temp_dir)
            extract_git_contents(temp_dir, output_file)
            print(f"\n✅ Done! Results saved to '{output_file}'")
        except subprocess.CalledProcessError as e:
            print(f"\n❌ Error cloning repo: {e}")
        finally:
            os.chdir(original_cwd)  # Ensure we are not inside temp_dir during cleanup
