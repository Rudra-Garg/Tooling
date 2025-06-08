#!/usr/bin/env python3
import os
import subprocess
import argparse

def list_git_files(repo_path):
    """List all files tracked by git in a repository."""
    os.chdir(repo_path)
    result = subprocess.run(['git', 'ls-files'], 
                           stdout=subprocess.PIPE, 
                           text=True, 
                           check=True)
    return result.stdout.splitlines()

def extract_git_contents(repo_path, output_file):
    """Extract all git-tracked files' names and contents to a text file."""
    files = list_git_files(repo_path)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for file_path in files:
            try:
                # Skip binary files, large files, or files that can't be read as text
                if os.path.getsize(os.path.join(repo_path, file_path)) > 1024 * 1024:  # Skip files > 1MB
                    f.write(f"\nFilename: {file_path}\n")
                    f.write("Content: [File too large to display]\n\n")
                    continue
                    
                # Try to read the file
                with open(os.path.join(repo_path, file_path), 'r', encoding='utf-8') as file:
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
    parser = argparse.ArgumentParser(description='Extract all files from a git repository')
    parser.add_argument('repo_path', help='Path to the git repository')
    parser.add_argument('--output', '-o', default='repo_contents.txt', 
                        help='Output file (default: repo_contents.txt)')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.repo_path):
        print(f"Error: Repository path '{args.repo_path}' does not exist")
        exit(1)
        
    if not os.path.exists(os.path.join(args.repo_path, '.git')):
        print(f"Error: '{args.repo_path}' is not a git repository")
        exit(1)
    
    print(f"Extracting files from {args.repo_path}...")
    extract_git_contents(args.repo_path, args.output)
    print(f"Done! Results saved to {args.output}")