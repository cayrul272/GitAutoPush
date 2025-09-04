# AutoPush - Automated Git Repository Management

A Python script that automatically commits and pushes changes to Git repositories at scheduled intervals.

## Features

- Automatic git commit and push functionality
- Configurable scheduling via Windows Task Scheduler
- Repository URL memory (asks once, remembers forever)
- Detailed logging of all operations
- Support for custom branch names
- File change tracking and statistics

## Requirements

- Python 3.6 or higher
- Git installed and configured
- GitHub account with personal access token

## Installation

1. Clone or download this repository to your local machine
2. Ensure Python is installed (`python --version` to check)
3. Install Git if not already installed

## Configuration

1. Edit `autopush.py` and update the following variables:
   - `USERNAME`: Your GitHub username
   - `TOKEN`: Your GitHub personal access token
   - `LOG_DIR`: Directory for log files (default: `C:\GitAutoPush`)

2. Generate a GitHub personal access token:
   - Go to GitHub Settings > Developer settings > Personal access tokens
   - Generate new token with `repo` permissions
   - Copy the token and paste it in the script

## Usage

### Manual Execution

Navigate to your repository directory and run:

```bash
python C:\GitAutoPush\autopush.py
```

On first run, the script will prompt for your GitHub repository URL. It will remember this URL for future runs.

### Automated Execution

Set up Windows Task Scheduler to run the script every 30 minutes:

1. Press `Win + R`, type `taskschd.msc`, press Enter
2. Click "Create Task" (not "Basic Task")
3. Name: `Git AutoPush`
4. Triggers tab: New trigger, Daily, Repeat every 30 minutes, Duration: Indefinitely
5. Actions tab: New action, Start a program
   - Program: Path to Python executable
   - Arguments: Full path to autopush.py
   - Start in: Your repository directory

## How It Works

1. The script checks if the current directory is a Git repository
2. If no remote origin is configured, it prompts for the GitHub URL
3. Creates or switches to an `auto-commit` branch
4. Checks for uncommitted changes
5. If changes exist, commits them with timestamp and pushes to GitHub
6. Logs all operations to the specified log directory

## Logging

All operations are logged to:
- Console output for immediate feedback
- Log file: `C:\GitAutoPush\autopush.log`

Logs include:
- Repository information
- Commit details
- Changed files and line statistics
- Push results

## File Structure

```
AutoPush/
├── autopush.py          # Main script
├── README.md            # This file
└── logs/                # Log files (created automatically)
```

## Troubleshooting

- Ensure Git is properly configured with your credentials
- Verify your GitHub token has the correct permissions
- Check that the repository directory contains a `.git` folder
- Review log files for detailed error information


