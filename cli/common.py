from __future__ import annotations

import shutil
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
APPS_DIR = PROJECT_ROOT / "apps"
DOCUMENTS_DIR = PROJECT_ROOT / "documents"
BACKUPS_DIR = PROJECT_ROOT / "backups"
README_FILE = PROJECT_ROOT / "README.md"

SKIP_DIRS = {
    ".git", "__pycache__", ".venv", "venv", "env",
    ".idea", ".vscode", "node_modules", "documents", "backups",
}


def ensure_documents_dir() -> Path:
    DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)
    return DOCUMENTS_DIR


def ask_dry_run(default_yes: bool = True) -> bool:
    prompt = "Run in Dry-Run preview mode first? [Y/n]: " if default_yes else "Run in Dry-Run preview mode? [y/N]: "
    ans = input(prompt).strip().lower()
    return ans != "n" if default_yes else ans == "y"


def create_backup_root(prefix: str) -> Path:
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_root = BACKUPS_DIR / f"{prefix}_{stamp}"
    backup_root.mkdir(parents=True, exist_ok=True)
    return backup_root


def backup_file(src: Path, backup_root: Path) -> None:
    if src.exists() and src.is_file():
        dest = backup_root / src.relative_to(PROJECT_ROOT)
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)