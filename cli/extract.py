import os
from datetime import datetime

def extract_project_files():
    print("=" * 65)
    print("   ULTIMATE DJANGO CODE EXTRACTOR (extract.py)")
    print("=" * 65)
    
    # 1. Enter search keyword(s) (Supports single or comma-separated keywords)
    raw_input = input("Enter keyword(s) to search (e.g., user, super, catalogs): ").strip().lower()
    if not raw_input:
        print("Error: Keyword cannot be empty!")
        return

    keywords = [k.strip() for k in raw_input.split(",") if k.strip()]

    # 2. Choose search mode (Partial vs Exact)
    print("\nSelect Search Mode:")
    print("  [1] Partial Match (e.g., 'user' matches 'users', 'superusers')")
    print("  [2] Exact Match (Exact folder name only)")
    choice_type = input("Enter choice [1 or 2, Default is 1]: ").strip()
    is_exact = (choice_type == '2')

    # 3. Search matching folders across the project
    matched_paths = []
    for root, dirs, files in os.walk("."):
        if any(exc in root for exc in ['.git', '__pycache__', 'venv', '.vscode', 'code']):
            continue
            
        folder_base_name = os.path.basename(root).lower()
        normalized_root = root.replace("\\", "/").lower()
        
        for kw in keywords:
            if is_exact:
                if kw == folder_base_name and root not in matched_paths:
                    matched_paths.append(root)
            else:
                if (kw in folder_base_name or kw in normalized_root) and root not in matched_paths:
                    matched_paths.append(root)

    if not matched_paths:
        print(f"❌ Error: No folders found matching '{raw_input}'!")
        return

    # 4. Preview found locations *before* saving and let user choose interactively
    print(f"\n🔍 Found Locations ({len(matched_paths)} items):")
    for idx, path in enumerate(matched_paths, 1):
        print(f"  [{idx}] {path}")

    print("\nSelect choice(s) to extract (e.g., 1 2 or 'all'):")
    selection = input("Enter choice(s): ").strip().lower()

    selected_paths = []
    if selection == 'all' or not selection:
        selected_paths = matched_paths
    else:
        try:
            indices = [int(x) for x in selection.split()]
            for idx in indices:
                if 1 <= idx <= len(matched_paths):
                    selected_paths.append(matched_paths[idx - 1])
                else:
                    print(f"⚠️ Warning: Index {idx} out of range, skipped.")
        except ValueError:
            print("⚠️ Invalid input! Extracting all matched paths.")
            selected_paths = matched_paths

    if not selected_paths:
        print("❌ No paths selected. Operation cancelled.")
        return

    # 5. File type filter (.py and/or .html)
    print("\nSelect file types to extract:")
    print("  [1] Both (.py and .html)")
    print("  [2] Python files only (.py)")
    print("  [3] HTML files only (.html)")
    file_choice = input("Enter choice [1, 2, or 3, Default is 1]: ").strip()
    
    allow_py = file_choice in ('', '1', '2')
    allow_html = file_choice in ('', '1', '3')

    # 6. Output directory setup ('code/' folder)
    output_dir = "code"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    safe_name = "_".join(keywords).replace('/', '_').replace('.', '_')
    output_filename = os.path.join(output_dir, f"{safe_name}.txt")

    # 7. Check if file already exists (Append 'a' or Overwrite 'w')
    write_mode = "w"
    if os.path.exists(output_filename):
        print(f"\n⚠️ '{output_filename}' already exists!")
        choice = input("Do you want to Append ('a') or Overwrite ('w')? [a/w]: ").strip().lower()
        write_mode = "a" if choice == 'a' else "w"

    # 8. Collect target files recursively avoiding excluded folders
    files_to_process = []
    for path in selected_paths:
        if os.path.isfile(path):
            if (path.endswith(".py") and allow_py) or (path.endswith(".html") and allow_html):
                if path not in files_to_process:
                    files_to_process.append(path)
        else:
            for root, dirs, files in os.walk(path):
                dirs[:] = [d for d in dirs if d not in ('__pycache__', '.git', 'migrations')]
                for file in sorted(files):
                    if (file.endswith(".py") and allow_py) or (file.endswith(".html") and allow_html):
                        f_path = os.path.join(root, file)
                        if f_path not in files_to_process:
                            files_to_process.append(f_path)

    py_count = sum(1 for f in files_to_process if f.endswith(".py"))
    html_count = sum(1 for f in files_to_process if f.endswith(".html"))

    try:
        with open(output_filename, write_mode, encoding="utf-8") as outfile:
            if write_mode == "a":
                outfile.write("\n\n" + "#" * 80 + f"\n# Appended on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n" + "#" * 80 + "\n\n")
            
            # 9. Summary Report Header in English
            outfile.write("=" * 80 + "\n")
            outfile.write(f"SUMMARY REPORT | KEYWORD(S): '{raw_input}'\n")
            outfile.write(f"Generated on : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            outfile.write(f"Total Files  : {len(files_to_process)} (Python: {py_count}, HTML: {html_count})\n")
            outfile.write("Included Paths:\n")
            for sp in selected_paths:
                outfile.write(f"  - {os.path.abspath(sp)}\n")
            outfile.write("=" * 80 + "\n\n")

            # 10. Path View + Source Code Writing
            for file_path in files_to_process:
                outfile.write("=" * 80 + "\n")
                outfile.write(f"PATH: {os.path.abspath(file_path)}\n")
                outfile.write("=" * 80 + "\n\n")

                try:
                    with open(file_path, "r", encoding="utf-8") as infile:
                        content = infile.read()
                        outfile.write(content if content.strip() else "# [Empty File]")
                except Exception as e:
                    outfile.write(f"# [Error reading file: {e}]")
                
                outfile.write("\n\n\n")

        print("\n" + "=" * 65)
        print(f"✅ Success! Extracted {py_count} Python & {html_count} HTML files.")
        print(f"📁 Saved location: {output_filename}")
        print("=" * 65)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    extract_project_files()