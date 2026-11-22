import os
import subprocess
import sys

def manage_file():
    print("=" * 50)
    print("       FILE MANAGER & VS CODE INTEGRATION       ")
    print("=" * 50)
    
    # 1. பயனரிடம் ஃபைல் பாதையை (File Path) உள்ளீடாக வாங்குதல்
    file_path = input("\nEnter the full file path (e.g., E:/project/app.py): ").strip()
    
    # மேற்கோள் குறிகள் (quotes) இருந்தால் அதை நீக்குதல்
    file_path = file_path.strip('"').strip("'")
    
    if not file_path:
        print("[-] Error: Invalid file path!")
        return

    # 2. ஃபைல் உள்ளதா எனச் சரிபார்த்தல்
    if os.path.exists(file_path):
        print(f"\n[+] File exists: '{file_path}'")
        
        # திறக்க வேண்டுமா என அனுமதி கேட்டல்
        choice = input("Do you want to open this file in VS Code? (y/n): ").strip().lower()
        if choice == 'y' or choice == 'yes':
            try:
                subprocess.run(['code', file_path], check=True, shell=True)
                print(f"[✓] Successfully opened '{file_path}' in VS Code!")
            except Exception as e:
                print(f"[-] Error opening file in VS Code: {e}")
        else:
            print("[!] Process cancelled by user.")

    else:
        print(f"\n[-] File does NOT exist at: '{file_path}'")
        
        # புதிய ஃபைல் உருவாக்கட்டுமா என அனுமதி கேட்டல்
        choice = input("Would you like to create a new fresh file? (y/n): ").strip().lower()
        if choice == 'y' or choice == 'yes':
            try:
                # ஃபைல் இருக்கும் ஃபோல்டர் இல்லை என்றால் உருவாக்கிக் கொள்ளுதல்
                directory = os.path.dirname(file_path)
                if directory and not os.path.exists(directory):
                    os.makedirs(directory, exist_ok=True)
                
                # புதிய வெற்று ஃபைலை உருவாக்குதல்
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write("")  # Fresh empty file
                
                print(f"[✓] Fresh file created successfully: '{file_path}'")
                
                # உருவாக்கிய புதிய ஃபைலை VS Code-ல் திறப்பது
                subprocess.run(['code', file_path], check=True, shell=True)
                print(f"[✓] Opened newly created file in VS Code!")
                
            except Exception as e:
                print(f"[-] Error creating or opening file: {e}")
        else:
            print("[!] File creation cancelled.")

if __name__ == "__main__":
    manage_file()