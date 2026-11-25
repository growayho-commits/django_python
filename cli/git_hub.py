import subprocess
from datetime import datetime

try:
    from cli.common import PROJECT_ROOT, ensure_documents_dir
except ImportError:
    from common import PROJECT_ROOT, ensure_documents_dir


def append_work_log(tag_name: str, summary: str) -> None:
    docs_dir = ensure_documents_dir()
    log_file = docs_dir / "WORK_LOG.md"
    if not log_file.exists():
        log_file.write_text("# Hybrid Marketplace - Date-Wise Work Log\n\n", encoding="utf-8")
    entry = f"## {tag_name}\n- {summary}\n\n"
    with log_file.open("a", encoding="utf-8") as f:
        f.write(entry)
    print(f"Updated work log: {log_file.relative_to(PROJECT_ROOT)}")


def git_manager():
    print("=" * 65)
    print("   HYBRID MARKETPLACE - GIT & GITHUB UTILITY (cli/git_hub.py)")
    print("=" * 65)

    print("\nSelect Git Action:")
    print("  [1] Check Git Status")
    print("  [2] Quick Commit & Push (All changes)")
    print("  [3] Pull latest changes from GitHub")
    print("  [4] Create & Push yyyy.mm.dd Version Tag + Update WORK_LOG.md")
    print("  [5] Compress Local Git Space (git gc)")
    choice = input("Enter choice [1-5]: ").strip()

    if choice == "1":
        subprocess.run(["git", "status"], cwd=PROJECT_ROOT)

    elif choice == "2":
        msg = input("\nEnter commit message: ").strip() or "Update project files"
        if subprocess.run(["git", "add", "."], cwd=PROJECT_ROOT).returncode == 0:
            if subprocess.run(["git", "commit", "-m", msg], cwd=PROJECT_ROOT).returncode == 0:
                subprocess.run(["git", "push", "origin", "main"], cwd=PROJECT_ROOT)

    elif choice == "3":
        subprocess.run(["git", "pull", "origin", "main"], cwd=PROJECT_ROOT)

    elif choice == "4":
        default_tag = datetime.now().strftime("%Y.%m.%d")
        tag_name = input(f"\nEnter version tag [Default: {default_tag}]: ").strip() or default_tag
        summary = input("Enter release summary: ").strip() or f"Release {tag_name}"
        append_work_log(tag_name, summary)
        subprocess.run(["git", "add", "."], cwd=PROJECT_ROOT)
        subprocess.run(["git", "commit", "-m", f"Release {tag_name}: {summary}"], cwd=PROJECT_ROOT)
        subprocess.run(["git", "tag", "-a", tag_name, "-m", f"Version {tag_name}: {summary}"], cwd=PROJECT_ROOT)
        subprocess.run(["git", "push", "origin", "main"], cwd=PROJECT_ROOT)
        subprocess.run(["git", "push", "origin", tag_name], cwd=PROJECT_ROOT)

    elif choice == "5":
        print("\nCompressing local .git repository space...")
        subprocess.run(["git", "gc", "--aggressive", "--prune=now"], cwd=PROJECT_ROOT)
        print("Done! Local Git space compressed.")

    else:
        print("Invalid choice.")


if __name__ == "__main__":
    git_manager()