import subprocess
import os
import sys
import google.generativeai as genai
from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown
import questionary

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

console = Console()

def get_command_from_gemini(prompt):
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(
            f"""You are a bash assistant. Reply only with a POSIX shell command corresponding to:
    "{prompt}".
    No explanation. Just the command. Remove markdown formatting."""
        )
    return response.text.strip()

def run_assistant():
    # print("🤖 Welcome to AI-Assist (Powered by Gemini)\n")
    if len(sys.argv) < 2:
        console.print("[red]❗ Usage: ai-assist [natural language instruction][/red]")
        sys.exit(1)

    question = " ".join(sys.argv[1:])
    console.print(f"[bold cyan]🧠 Query:[/bold cyan] {question}")
    console.print("[grey]⏳ Sending to Gemini...[/grey]\n")

    try:
        command = get_command_from_gemini(question)
    except Exception as e:
        console.print(f"[red]❌ Gemini Error:[/red] {e}")
        sys.exit(1)

    console.print("\n[bold green]💡 Gemini suggests:[/bold green]")
    console.print(f"[green]{command}[/green]\n")

    choice = questionary.select(
        "What do you want to do?",
        choices=[
            "1. ✅ Execute",
            "2. ✏️ Modify command",
            "3. ❌ Cancel"
        ]).ask()

    if choice.startswith("1"):
        console.print("[cyan]▶️ Executing...[/cyan]\n")
        subprocess.run(command, shell=True)

    elif choice.startswith("2"):
        new_cmd = questionary.text("📝 Modify the command:", default=command ).ask()
        subprocess.run(new_cmd, shell=True)

    else:
        console.print("[red]🚫 Command cancelled.[/red]")

if __name__ == "__main__":
    run_assistant()
