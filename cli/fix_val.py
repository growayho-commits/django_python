import os
import py_compile

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
APPS_DIR = os.path.join(PROJECT_ROOT, "apps")
CORE_DIR = os.path.join(PROJECT_ROOT, "core")

EXCLUDED_DIRS = {'__pycache__', 'migrations'}

def fix_and_validate_mode():
    print("=" * 70)
    print("   HYBRID MARKETPLACE - FIX & VALIDATE (fix_val.py)")
    print("=" * 70 + "\n")

    if not os.path.exists(PROJECT_ROOT):
        print(f"⚠️ Error: Project root not found at path: {PROJECT_ROOT}!")
        return

    print("🔍 [Step 1] Running pre-flight Python syntax compilation checks...")
    print("-" * 70)

    syntax_errors = []
    target_dirs = [APPS_DIR, CORE_DIR, SCRIPT_DIR]
    
    # அனைத்துப் பிழைகளைக் கண்டறிந்து சேகரித்தல்
    for d in target_dirs:
        if os.path.exists(d):
            for root, dirs, files in os.walk(d):
                dirs[:] = [dir_name for dir_name in dirs if dir_name not in EXCLUDED_DIRS]
                for file in files:
                    if file.endswith(".py"):
                        file_path = os.path.join(root, file)
                        try:
                            py_compile.compile(file_path, doraise=True)
                        except Exception as e:
                            syntax_errors.append((file_path, str(e)))

    total_errors = len(syntax_errors)
    print(f"\n📊 Validation Summary: Found {total_errors} syntax errors in total.\n" + "-" * 70)

    if total_errors == 0:
        print("🎉 [Status] All Python files are clean and syntactically sound!")
        print("=" * 70)
        return True

    # பயனரிடம் முறையைத் தேர்ந்தெடுக்குமாறு கேட்டல் (Manual / Automatic)
    print("💡 Choose your fixing mode:")
    print("   [1] Manual (ஒவ்வொரு எரராகக் காட்டி உங்களது அனுமதியுடன் (y/N) சரி செய்யும்)")
    print("   [2] Automatic (அனைத்து எரர்களையும் கேள்வியின்றி ஒரே அடியில் ஆட்டோமேட்டிக்காகச் சரி செய்யும்)")
    
    mode_choice = input("👉 Enter your choice [1 or 2, Default is 1]: ").strip()
    is_automatic = (mode_choice == '2')

    fixed_count = 0

    print("\n" + "-" * 70)
    for idx, (file_path, error_msg) in enumerate(syntax_errors, 1):
        rel_path = os.path.relpath(file_path, PROJECT_ROOT)
        print(f"\n[{idx}/{total_errors}] ❌ Syntax Error in: {rel_path}")
        print(f"     --> Details: {error_msg}")

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            should_fix = False

            if is_automatic:
                should_fix = True
                print(f"     ⚡ [Auto Mode] Fixing automatically...")
            else:
                # Manual முறை: ஒவ்வொரு பிழைக்கும் y/N கேட்கும்
                choice = input(f"     👉 Do you want to fix this error? [y/N]: ").strip().lower()
                if choice == 'y':
                    should_fix = True

            if should_fix:
                # மார்க் டவுன் ஆர்ட்டிஃபாக்ட்களை நீக்குதல்
                new_content = content.replace("```", "")
                new_content = new_content.replace("", "").replace("", "").replace("", "")
                
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                
                try:
                    py_compile.compile(file_path, doraise=True)
                    print(f"  ✔️ [Success] Error fixed and verified for {rel_path}")
                    fixed_count += 1
                except Exception as post_fix_err:
                    print(f"  ⚠️ [Warning] Cleaned, but check manually. Error: {post_fix_err}")
            else:
                print(f"  ⏭️ Skipped this file.")

        except Exception as e:
            print(f"  ❌ Error processing file: {e}")

    print("\n" + "=" * 70)
    print(f"🎉 Session Completed!")
    print(f"   - Total Errors Initially: {total_errors}")
    print(f"   - Successfully Fixed: {fixed_count}")
    print(f"   - Remaining: {total_errors - fixed_count}")
    print("=" * 70)

if __name__ == "__main__":
    fix_and_validate_mode()