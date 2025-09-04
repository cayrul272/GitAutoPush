import os
import subprocess
import datetime

USERNAME = "<your-username>"
TOKEN = "<your-token>"
LOG_DIR = r"C:\GitAutoPush"
LOG_FILE = os.path.join(LOG_DIR, "autopush.log")

def run_command(cmd, cwd=None):
    """Run shell command and return output"""
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, shell=True)

def log(message):
    """Write logs in UTF-8"""
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{datetime.datetime.now()} - {message}\n")

def main():
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    repo_dir = os.getcwd()

    if not os.path.exists(os.path.join(repo_dir, ".git")):
        log("❌ Not a git repository")
        print("This folder is not a git repository.")
        return

    result = run_command("git config --get remote.origin.url", cwd=repo_dir)
    repo_url = result.stdout.strip()

    if not repo_url:
        repo_url = input("Enter GitHub repo URL (e.g. https://github.com/<your-username>/<your-repo-name>): ").strip()
        if not repo_url:
            print("❌ No URL provided, exiting.")
            return
        authed_url = repo_url.replace("https://", f"https://{USERNAME}:{TOKEN}@")
        run_command(f"git remote add origin {authed_url}", cwd=repo_dir)
    else:
        authed_url = repo_url.replace("https://", f"https://{USERNAME}:{TOKEN}@")
        run_command(f"git remote set-url origin {authed_url}", cwd=repo_dir)

    # Ensure branch exists
    run_command("git checkout auto-commit", cwd=repo_dir)
    if "did not match any file(s)" in run_command("git branch", cwd=repo_dir).stderr:
        run_command("git checkout -b auto-commit", cwd=repo_dir)

    # Check for changes
    diff_check = run_command("git status --porcelain", cwd=repo_dir)
    if not diff_check.stdout.strip():
        log("ℹ️ No changes to commit")
        print("No changes found.")
        return

    # Collect file + line stats before committing
    changed_files = run_command("git diff --cached --name-status", cwd=repo_dir).stdout.strip()
    if not changed_files:
        changed_files = run_command("git diff --name-status", cwd=repo_dir).stdout.strip()

    line_stats = run_command("git diff --stat", cwd=repo_dir).stdout.strip()

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    run_command("git add .", cwd=repo_dir)
    run_command(f'git commit -m "auto-commit {timestamp}"', cwd=repo_dir)
    push_result = run_command("git push origin auto-commit", cwd=repo_dir)

    # Console + log summary
    print("\n================ PUSH SUMMARY ================\n")
    print(f"✅ Repo: {repo_url}")
    print(f"🌿 Branch: auto-commit")
    print(f"📂 Directory: {repo_dir}")
    print(f"🕒 Commit Time: {timestamp}")
    print("\n📄 Changed Files:")
    print(changed_files if changed_files else "No file list available")
    print("\n✍️ Line Changes:")
    print(line_stats if line_stats else "No line stats available")
    print("\n==============================================\n")

    log(f"✅ Changes committed and pushed to {repo_url}")
    log(f"Branch: auto-commit")
    log(f"Directory: {repo_dir}")
    log(f"Message: auto-commit {timestamp}")
    log("Changed Files:\n" + (changed_files or "None"))
    log("Line Stats:\n" + (line_stats or "None"))
    log(f"Push output: {push_result.stdout} {push_result.stderr}")

    print("✅ Changes committed and pushed successfully!")

if __name__ == "__main__":
    main()
