import subprocess
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def get_shell_command(prompt):
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(
        f"""You are a bash assistant. Reply only with a POSIX shell command corresponding to:
"{prompt}".
No explanation. Just the command."""
    )
    return response.text.strip()

def run_assistant():
    print("🤖 Welcome to AI-Assist (Powered by Gemini)\n")

    user_input = input("🧠 What do you want to do?\n> ")

    print("\n🔎 Gemini is thinking...\n")
    try:
        command = get_shell_command(user_input)
    except Exception as e:
        print("❌ Gemini Error:", e)
        return

    print("💡 Suggested command:")
    print(f"> {command}\n")

    print("What do you want to do?")
    print("[1] ✅ Execute")
    print("[2] ✏️ Modify")
    print("[3] ❌ Cancel")
    choice = input("> ").strip()

    if choice == "1":
        print("\n▶️ Executing...")
        subprocess.run(command, shell=True)
    elif choice == "2":
        mod = input("✏️ Modified command:\n> ")
        subprocess.run(mod, shell=True)
    else:
        print("🚫 Command cancelled.")

if __name__ == "__main__":
    run_assistant()
