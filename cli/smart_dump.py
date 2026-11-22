from __future__ import annotations

from pathlib import Path

BASE_DIR = Path.cwd()
CONTEXT_FILE = BASE_DIR / "AI_PROJECT_CONTEXT.md"
DOCS_DIR = BASE_DIR / "document"
OUT_FILE = DOCS_DIR / "selected_code_dump.txt"

ALLOWED_EXTS = {".py", ".html", ".md", ".txt", ".json", ".yml", ".yaml", ".env"}
SKIP_DIRS = {
    "migrations",
    "__pycache__",
    ".git",
    ".venv",
    "venv",
    "node_modules",
    ".idea",
    ".vscode",
}

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
    return (
        path.is_file()
        and path.suffix.lower() in ALLOWED_EXTS
        and not any(part in SKIP_DIRS for part in path.parts)
    )


def get_subdirs(folder: Path) -> list[Path]:
    if not folder.exists() or not folder.is_dir():
        return []
    return [
        d
        for d in sorted(folder.iterdir(), key=lambda p: p.name.lower())
        if d.is_dir() and d.name not in SKIP_DIRS
    ]


def match_single_term(path: Path, term: str, mode: str) -> bool:
    q = term.strip().lower()
    if not q:
        return True

    rel_str = str(path.relative_to(BASE_DIR)).lower()
    file_name = path.name.lower()
    file_stem = path.stem.lower()

    if mode == "exact":
        return q in {file_name, file_stem}

    return q in file_name or q in rel_str


def matches_query(path: Path, query: str, mode: str, use_aliases: bool = True) -> bool:
    raw = query.strip().lower()
    if not raw:
        return True

    terms = [t.strip() for t in raw.replace(",", " ").split() if t.strip()]
    if not terms:
        return True

    for term in terms:
        candidates = [term]
        if use_aliases and term in KEYWORD_ALIASES:
            for alias in KEYWORD_ALIASES[term]:
                if alias not in candidates:
                    candidates.append(alias)

        if any(match_single_term(path, cand, mode) for cand in candidates):
            return True

    return False


def pick_path_menu(title: str, options: list[str]) -> tuple[str, str | None]:
    print(f"\n{'=' * 55}")
    print(f"📁 {title}")
    print(f"{'=' * 55}")
    for idx, opt in enumerate(options, start=1):
        print(f"  {idx}. {opt}")
    print("  [Enter] -> ALL (இந்த இடத்திலிருந்து அனைத்தையும் எடு)")
    print("  [Name]  -> நேரடியாக பெயர்/பாதையை டைப் செய்யலாம்")
    print("  0       -> Exit")

    while True:
        raw = input("\nதேர்வு செய்யவும் (Number / Name / Enter): ").strip()
        if raw == "":
            return ("ALL", None)
        if raw in {"0", "q", "Q"}:
            return ("EXIT", None)
        if raw.isdigit():
            num = int(raw)
            if 1 <= num <= len(options):
                return ("ITEM", options[num - 1])
            print(f"❌ 1 முதல் {len(options)} வரை உள்ள எண்ணை உள்ளிடவும்.")
            continue
        return ("DIRECT", raw)


def ask_search_options() -> tuple[str, str, bool]:
    print(f"\n{'=' * 55}")
    print("🔎 File / Keyword Search (Optional)")
    print(f"{'=' * 55}")
    print("  [Enter]         -> எந்த ஃபில்டரும் இல்லாமல் ALL")
    print("  urls.py / admin.py / conf.py / config -> பெயர் அல்லது கீவேர்ட்")

    query = input("தேட வேண்டிய பெயர்/கீவேர்ட் (அல்லது Enter): ").strip()
    if not query:
        return ("", "include", False)

    print("\nMatch Type தேர்வு செய்யவும்:")
    print("  1. Include (பெயர்/பாத்-ல் எங்காவது இருந்தாலும் வரும் — Default)")
    print("  2. Exact Match (கோப்பின் பெயர் சரியாக மேட்ச் ஆனால் மட்டும் வரும்)")
    mode_raw = input("Match Type [Enter = 1 / Include]: ").strip()
    mode = "exact" if mode_raw == "2" else "include"

    use_aliases = False
    if mode == "include":
        print("\nSmart Alias (உதாரணமாக 'config' என்றால் 'conf.py' & 'config' இரண்டும்):")
        alias_raw = input("Alias சேர்க்க வேண்டுமா? [Enter = Yes (Y) / n = No]: ").strip().lower()
        use_aliases = alias_raw not in {"n", "no"}

    return (query, mode, use_aliases)


def collect_target_files(
    target_path: Path,
    dump_all: bool,
    query: str,
    mode: str,
    use_aliases: bool,
) -> list[Path]:
    if target_path.is_file():
        candidates = [target_path] if is_valid_file(target_path) else []
    elif dump_all or query:
        candidates = [p for p in sorted(target_path.rglob("*")) if is_valid_file(p)]
    else:
        candidates = [p for p in sorted(target_path.iterdir()) if is_valid_file(p)]

    if not query:
        return candidates

    return [p for p in candidates if matches_query(p, query, mode=mode, use_aliases=use_aliases)]


def main() -> None:
    if CONTEXT_FILE.exists():
        print(f"📘 Reference Context: {CONTEXT_FILE.name} (கண்டறியப்பட்டது)")
    else:
        print(f"⚠️ குறிப்பு: {CONTEXT_FILE.name} இல்லை; {BASE_DIR} அடிப்படையில் இயங்குகிறது.")

    current_path = BASE_DIR
    dump_all = False

    while current_path.is_dir():
        subs = get_subdirs(current_path)
        if not subs:
            dump_all = True
            break

        rel_label = "." if current_path == BASE_DIR else str(current_path.relative_to(BASE_DIR))
        action, value = pick_path_menu(f"Path: {rel_label}", [d.name for d in subs])

        if action == "EXIT":
            print("வெளியேறியது.")
            return
        if action == "ALL":
            dump_all = True
            break
        if action == "ITEM" and value is not None:
            current_path = current_path / value
            continue
        if action == "DIRECT" and value is not None:
            direct_candidate = (BASE_DIR / value).resolve()
            if direct_candidate.exists():
                current_path = direct_candidate
                dump_all = current_path.is_dir()
                break
            dump_all = True
            query, mode, use_aliases = value, "include", True
            files = collect_target_files(current_path, dump_all, query, mode, use_aliases)
            write_output(current_path, query, mode, files)
            return

    query, mode, use_aliases = ask_search_options()
    files = collect_target_files(current_path, dump_all=dump_all, query=query, mode=mode, use_aliases=use_aliases)
    write_output(current_path, query, mode, files)


def write_output(target_path: Path, query: str, mode: str, files: list[Path]) -> None:
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    target_label = "." if target_path == BASE_DIR else str(target_path.relative_to(BASE_DIR))
    header = (
        f"# Reference: {CONTEXT_FILE.name}\n"
        f"# Target Path: {target_label}\n"
        f"# Query: {query if query else 'ALL'}\n"
        f"# Match Mode: {mode if query else 'ALL'}\n"
        f"# Matched Files: {len(files)}\n"
    )

    blocks = [header]
    for f in files:
        rel = f.relative_to(BASE_DIR)
        code = f.read_text(encoding="utf-8", errors="replace")
        blocks.append(f"\n{'=' * 65}\nFILE: {rel}\n{'=' * 65}\n{code}")

    OUT_FILE.write_text("\n".join(blocks), encoding="utf-8")
    rel_out = OUT_FILE.relative_to(BASE_DIR)
    print(f"\n✅ முடிந்தது! {len(files)} கோப்புகள் '{rel_out}' கோப்பில் சேமிக்கப்பட்டன.")
    for f in files[:15]:
        print(f"   • {f.relative_to(BASE_DIR)}")
    if len(files) > 15:
        print(f"   ... மற்றும் {len(files) - 15} கோப்புகள்.")


if __name__ == "__main__":
    main()