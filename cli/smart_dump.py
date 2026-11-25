from __future__ import annotations

from pathlib import Path

try:
    from cli.common import PROJECT_ROOT, SKIP_DIRS, ensure_documents_dir
except ImportError:
    from common import PROJECT_ROOT, SKIP_DIRS, ensure_documents_dir

CONTEXT_FILE = PROJECT_ROOT / "documents" / "AI_PROJECT_CONTEXT.md"
ALLOWED_EXTS = {".py", ".html", ".md", ".txt", ".json", ".yml", ".yaml", ".env"}

KEYWORD_ALIASES: dict[str, list[str]] = {
    "config": ["conf", "config"],
    "configs": ["conf", "config"],
    "conf": ["conf", "config"],
    "url": ["urls.py", "url"],
    "urls": ["urls.py", "url"],
    "admin": ["admin.py", "admin"],
    "setting": ["settings", "conf.py", "config"],
    "settings": ["settings", "conf.py", "config"],
}


def is_valid_file(path: Path) -> bool:
    return path.is_file() and path.suffix.lower() in ALLOWED_EXTS and not any(p in SKIP_DIRS or p == "migrations" for p in path.parts)


def get_subdirs(folder: Path) -> list[Path]:
    return [d for d in sorted(folder.iterdir(), key=lambda p: p.name.lower()) if d.is_dir() and d.name not in SKIP_DIRS and d.name != "migrations"]


def matches_query(path: Path, query: str, mode: str, use_aliases: bool = True) -> bool:
    terms = [t.strip() for t in query.strip().lower().replace(",", " ").split() if t.strip()]
    if not terms:
        return True
    rel_str = str(path.relative_to(PROJECT_ROOT)).lower()
    fname, fstem = path.name.lower(), path.stem.lower()
    for term in terms:
        cands = [term] + (KEYWORD_ALIASES.get(term, []) if use_aliases else [])
        for c in cands:
            if (c in {fname, fstem}) if mode == "exact" else (c in fname or c in rel_str):
                return True
    return False


def write_output(target_path: Path, query: str, mode: str, files: list[Path]) -> None:
    docs_dir = ensure_documents_dir()
    out_file = docs_dir / "selected_code_dump.txt"
    blocks = [f"# Target: {target_path.relative_to(PROJECT_ROOT) if target_path != PROJECT_ROOT else '.'}\n# Files: {len(files)}\n"]
    for f in files:
        blocks.append(f"\n{'=' * 65}\nFILE: {f.relative_to(PROJECT_ROOT)}\n{'=' * 65}\n{f.read_text(encoding='utf-8', errors='replace')}")
    out_file.write_text("\n".join(blocks), encoding="utf-8")
    print(f"\nSaved {len(files)} file(s) to: {out_file.relative_to(PROJECT_ROOT)}")


def main() -> None:
    current_path, dump_all = PROJECT_ROOT, False
    while current_path.is_dir():
        subs = get_subdirs(current_path)
        if not subs:
            dump_all = True
            break
        print(f"\nPath: {'.' if current_path == PROJECT_ROOT else current_path.relative_to(PROJECT_ROOT)}")
        for idx, d in enumerate(subs, 1):
            print(f"  {idx}. {d.name}")
        raw = input("Choose number (Enter=ALL, 0=Exit): ").strip()
        if raw == "":
            dump_all = True
            break
        if raw == "0":
            return
        if raw.isdigit() and 1 <= int(raw) <= len(subs):
            current_path = subs[int(raw) - 1]

    query = input("Search keyword (or Enter for ALL): ").strip()
    mode = "exact" if query and input("Match [1=Include, 2=Exact]: ").strip() == "2" else "include"
    candidates = [p for p in (sorted(current_path.rglob("*")) if (dump_all or query) else sorted(current_path.iterdir())) if is_valid_file(p)]
    files = [p for p in candidates if matches_query(p, query, mode)] if query else candidates
    write_output(current_path, query, mode, files)


if __name__ == "__main__":
    main()