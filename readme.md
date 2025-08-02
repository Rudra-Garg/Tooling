# Developer Tools Collection

A comprehensive collection of command-line tools for developers, featuring AI-powered code analysis, repository management, and Minecraft mod utilities.

## 🚀 Tools Overview

This suite of tools is designed to streamline common developer workflows, from understanding new codebases to managing large-scale personal projects.

-----

### 🤖 AI & Analysis Tools

#### `ai` - AI-Powered Assistant

Ask questions to Google's Gemini AI directly from your command line. Get instant answers without leaving the terminal.

  * **Usage:** `ai "What is the capital of France?"`
  * **Features:** Color-coded markdown formatting, loading animations, and support for complex technical questions.

#### `summarize` - Local Repository Summarizer

Generate a comprehensive AI-powered summary for any local Git repository. Ideal for quickly getting up to speed on a new project.

  * **Usage:** `summarize C:\Projects\my-repo`
  * **Features:** Analyzes all Git-tracked files, identifies technology stack and architecture, and saves a structured markdown summary to your **current working directory**.

-----

### 📦 GitHub & Local Repository Tools

#### `ghextract` - Single GitHub Repo Extractor

Clone and extract the contents of any public or private GitHub repository URL into a single text file.

  * **Usage:** `ghextract https://github.com/username/repo.git`
  * **Features:** Creates a temporary clone, handles binary files gracefully, and saves output to `{repo_name}_contents.txt` in your **current working directory**.

#### `ghextractall` - Bulk GitHub Repo Extractor

Fetch and extract the contents of all your accessible GitHub repositories (public and private) at once.

  * **Usage:** `ghextractall`
  * **Features:** Uses your GitHub token to find all repos, supports custom branch configurations, respects ignore lists, and saves neatly organized files to the `CONTENTS/` directory.

#### `ghsummarize` - Bulk GitHub Repo Summarizer

Run `ghextractall` and then send the contents of each repository to Gemini to generate detailed technical summaries for all of them.

  * **Usage:** `ghsummarize`
  * **Features:** Automates the summarization of your entire GitHub portfolio, saving structured markdown analyses to the `SUMMARIES/` directory.

#### `extract` - Local Repository Extractor

Extract the contents of a local Git repository into a single text file. A lightweight utility for local use.

  * **Usage:** `extract C:\Projects\my-repo`
  * **Features:** Fast and simple extraction. Respects a local `.extractignore` file for granular control over what gets included.

-----

### 🎮 Gaming Tools

#### `minecraft_mod_updater` - Minecraft Mod Manager

Automatically scan and update your Minecraft mods (Fabric & Forge) to the latest compatible versions from Modrinth.

  * **Usage:** `minecraft_mod_updater --minecraft-version 1.20.1`
  * **Features:** Automatic mod detection, an interactive batch interface for easy use, and an integrated backup system for safety.

## 📋 Prerequisites

### Required Environment Variables

Create a `.env` file in the main tools directory with the following keys:

```env
GEMINI_API_KEY=your_gemini_api_key_here
GITHUB_TOKEN=your_github_token_here
```

### Dependencies

  * **Python 3.7+**
  * **Git** installed and accessible from the command line.
  * Required Python packages: `pip install google-generativeai python-dotenv requests`

### API Keys Setup

  * **Gemini API Key:** Get one from [Google AI Studio](https://makersuite.google.com/app/apikey).
  * **GitHub Token:** Generate a new personal access token with `repo` permissions in your [GitHub Developer settings](https://github.com/settings/tokens).

## 🚀 Installation

1.  Clone or download this repository to a persistent location (e.g., `C:\Tools`).
2.  Add the tools directory to your system's `PATH` environment variable.
3.  Install the required Python dependencies using the pip command above.
4.  Create and populate your `.env` file as described in the prerequisites.

## ⚙️ Configuration Files

You can control the behavior of the bulk processing scripts using simple text files in the main tools directory.

#### For `ghextractall` & `ghsummarize`:

  * **`.ignore`**: A list of repository names (one per line) to exclude from processing.
    ```
    my-private-repo
    test-repository
    ```
  * **`.ownerignore`**: A list of GitHub usernames or organization names (one per line) whose repositories will be skipped.
    ```
    spammer-user
    test-org
    ```
  * **`.branch`**: Specify non-default branches for specific repositories.
    ```
    owner/repo main
    another-owner/special-repo development
    ```

#### For `extract` (Local Extraction):

  * **`.extractignore`**: Placed inside the target repository you are extracting, this file lists files or patterns to ignore, similar to a `.gitignore`.
    ```
    # Ignore specific files
    secret.txt
    *.log

    # Ignore directories
    node_modules/
    dist/
    ```

## 📁 Output Structure

The output files are generated in logical locations depending on the tool used:

  * **`ghextractall`**: `Tools/CONTENTS/owner_repo_contents.txt`
  * **`ghsummarize`**: `Tools/SUMMARIES/owner_repo_summary.md`
  * **`ghextract`**: Saves `{repo-name}_contents.txt` to your current working directory.
  * **`extract`**: Saves `repo_contents.txt` (or a custom name) to your current working directory.
  * **`summarize`**: Saves `{owner}_{repo-name}_summary.md` to your current working directory.

## 🎯 Use Cases

  * **Code Onboarding**: Quickly understand an unfamiliar codebase with an AI-generated summary.
  * **Portfolio Management**: Generate and maintain up-to-date documentation for all your projects.
  * **Research**: Extract and analyze open-source projects for patterns and technologies.
  * **AI Assistance**: Get quick, formatted answers to technical questions without breaking your workflow.
  * **Gaming**: Keep your Minecraft modpack updated effortlessly.

## 🔍 Features

  * **AI-Powered Analysis**: Leverages Google's Gemini for intelligent code understanding.
  * **Batch Processing**: Handle all your GitHub repositories efficiently in one command.
  * **Flexible Configuration**: Customize behavior with powerful ignore lists and branch settings.
  * **Safety First**: Includes backup systems (`minecraft_mod_updater`) and graceful error handling.
  * **Cross-Platform**: Designed to work on Windows, macOS, and Linux.
  * **Clean Terminal UI**: Color-coded output, progress indicators, and animations for a better user experience.

## 🛠️ Technical Details

  * **Language**: Python 3
  * **AI Model**: Google Gemini 2.0 Flash
  * **APIs**: GitHub REST API, Modrinth API
  * **File Handling**: UTF-8 encoding with robust binary file and error detection.
  * **Concurrency**: Uses `ThreadPoolExecutor` for some parallel processing to improve speed.

## 🤝 Contributing

Feel free to submit issues, feature requests, or pull requests to improve these tools. All contributions are welcome\!

## 📄 License

This project is open source and available under the MIT License.

-----

*Happy coding\! 🚀*