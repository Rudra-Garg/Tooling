# Developer Tools Collection

A comprehensive collection of command-line tools for developers, featuring AI-powered code analysis, repository management, and Minecraft mod utilities.

## 🚀 Tools Overview

### 🤖 AI & Analysis Tools

#### `ai` - AI-Powered Assistant
Ask questions to Google's Gemini AI directly from the command line.

**Usage:**
```bash
ai "What is the capital of France?"
ai "Explain how JavaScript closures work"
```

**Features:**
- Color-coded markdown formatting in terminal
- Loading animations for better UX
- Supports complex technical questions

#### `summarize` - Repository Summarizer
Generate comprehensive AI-powered summaries of local Git repositories.

**Usage:**
```bash
summarize C:\Projects\my-repo
summarize . --extract-only  # Extract files without summarizing
```

**Features:**
- Analyzes all Git-tracked files
- Generates structured technical summaries
- Identifies technology stack, patterns, and architecture
- Output saved as markdown files

### 📦 GitHub Repository Tools

#### `ghextract` - Single Repository Extractor
Extract contents from any GitHub repository URL.

**Usage:**
```bash
ghextract https://github.com/username/repo.git
ghextract https://github.com/username/repo.git -o custom_output.txt
```

**Features:**
- Clones repository temporarily
- Extracts all Git-tracked files
- Handles binary files gracefully
- Auto-generates output filename

#### `ghextractall` - Bulk Repository Extractor
Extract contents from all your GitHub repositories at once.

**Usage:**
```bash
ghextractall
```

**Features:**
- Fetches all public and private repositories
- Supports custom branch configurations
- Ignore lists for filtering repositories
- Concurrent processing for speed
- Creates organized output in `CONTENTS/` directory

#### `ghsummarize` - Bulk Repository Summarizer
Generate AI summaries for all your GitHub repositories.

**Usage:**
```bash
ghsummarize
```

**Features:**
- Processes all your GitHub repositories
- AI-powered technical summaries
- Structured analysis of tech stack and architecture
- Output saved in `SUMMARIES/` directory

### 🎮 Gaming Tools

#### `minecraft_mod_updater` - Minecraft Mod Manager
Automatically update Minecraft mods to their latest versions using Modrinth.

**Usage:**
```bash
minecraft_mod_updater
minecraft_mod_updater --minecraft-version 1.20.1 --loader fabric
```

**Features:**
- Supports Fabric and Forge mods
- Automatic mod detection and updating
- Backup system for safety
- Interactive batch interface
- Modrinth platform integration

### 🔧 Utility Tools

#### `extract` - Local Repository Extractor
Extract contents from local Git repositories.

**Usage:**
```bash
extract C:\Projects\my-repo
extract /path/to/repo --output contents.txt
```

## 📋 Prerequisites

### Required Environment Variables
Create a `.env` file in the tools directory with:

```env
GEMINI_API_KEY=your_gemini_api_key_here
GITHUB_TOKEN=your_github_token_here
```

### Dependencies
- **Python 3.7+** with the following packages:
  - `google-generativeai`
  - `python-dotenv`
  - `requests`
- **Git** installed and accessible from command line

### API Keys Setup

#### Gemini API Key
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Add to your `.env` file

#### GitHub Token
1. Go to GitHub Settings > Developer settings > Personal access tokens
2. Generate a new token with `repo` permissions
3. Add to your `.env` file

## 🚀 Installation

1. Clone or download this repository to your desired location (e.g., `C:\Tools`)
2. Add the tools directory to your system PATH
3. Install Python dependencies:
   ```bash
   pip install google-generativeai python-dotenv requests
   ```
4. Set up your `.env` file with required API keys

## ⚙️ Configuration Files

### `.ignore` - Repository Ignore List
List repositories to skip during bulk operations:
```
my-private-repo
test-repository
archived-project
```

### `.ownerignore` - Owner Ignore List
Skip repositories from specific users/organizations:
```
spammer-user
test-org
```

### `.branch` - Custom Branch Configuration
Specify custom branches for repositories:
```
owner/repo main
another-owner/special-repo development
```

## 📁 Output Structure

```
Tools/
├── CONTENTS/           # Extracted repository contents
│   ├── owner_repo_contents.txt
│   └── ...
├── SUMMARIES/          # AI-generated summaries
│   ├── owner_repo_summary.md
│   └── ...
├── .env               # Environment variables
├── .ignore            # Repository ignore list
├── .ownerignore       # Owner ignore list
└── .branch            # Branch configurations
```

## 🎯 Use Cases

- **Code Analysis**: Quickly understand unfamiliar codebases
- **Portfolio Management**: Generate summaries of all your projects
- **Research**: Extract and analyze open-source projects
- **Documentation**: Auto-generate technical documentation
- **Gaming**: Keep Minecraft mods up-to-date effortlessly
- **AI Assistance**: Get quick answers to technical questions

## 🔍 Features

- **AI-Powered Analysis**: Leverages Google's Gemini for intelligent code understanding
- **Batch Processing**: Handle multiple repositories efficiently
- **Flexible Configuration**: Customize behavior with ignore lists and branch settings
- **Safety Features**: Backup systems and error handling
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Terminal UI**: Color-coded output and progress indicators

## 🛠️ Technical Details

- **Language**: Python 3
- **AI Model**: Google Gemini 2.0 Flash
- **APIs**: GitHub REST API, Modrinth API
- **File Handling**: UTF-8 encoding with binary file detection
- **Concurrency**: ThreadPoolExecutor for parallel processing
- **Error Handling**: Graceful handling of network issues and file errors

## 📝 Examples

### Generate a repository summary
```bash
# Summarize current directory
summarize .

# Summarize specific repository
summarize C:\Projects\my-react-app
```

### Extract repository contents
```bash
# From GitHub URL
ghextract https://github.com/facebook/react.git

# From local repository
extract C:\Projects\my-app -o app-contents.txt
```

### Update Minecraft mods
```bash
# Interactive mode
minecraft_mod_updater

# Specific version
minecraft_mod_updater --minecraft-version 1.20.1 --loader fabric --no-backup
```

### Ask AI questions
```bash
ai "How do I implement a binary search tree in Python?"
ai "Explain the differences between React hooks"
```

## 🤝 Contributing

Feel free to submit issues, feature requests, or pull requests to improve these tools.

## 📄 License

This project is open source and available under the MIT License.

---

*Happy coding! 🚀*