import subprocess
import sys
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
import questionary
from questionary import Style
from aiassistcli.ai_config import get_command_from_ai


console = Console()

# 🎨 Custom style for questionary
custom_style = Style([
   ('qmark', 'fg:#673ab7 bold'),        
    ('question', 'bold'),               
    ('answer', 'fg:#f44336 bold'),      
    ('pointer', 'fg:#673ab7 bold'),     
    ('highlighted', 'fg:#673ab7 bold'), 
    ('selected', 'fg:#cc5454'),         
    ('separator', 'fg:#cc5454'),        
    ('instruction', ''),               
    ('text', ''),                      
    ('disabled', 'fg:#858585 italic')
])

def main():
    # print("🤖 Welcome to AI-Assist (Powered by Gemini)\n")
    if len(sys.argv) < 2:
        console.print("[red]❗ Usage: ai-assist [natural language instruction][/red]")
        sys.exit(1)

    question = " ".join(sys.argv[1:])
    console.print(f"[bold cyan]🧠 Query:[/bold cyan] {question}")
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[grey] Processing...[/grey]"),
            transient=True
        ) as progress:
            progress.add_task("thinking", total=None)
            command = get_command_from_ai(question)
        
    except Exception as e:
        console.print(f"[red]Gemini Error:[/red] {e}")
        sys.exit(1)

    console.print("\n[bold green]💡 Gemini suggests:[/bold green]")
    console.print(f"[green] {command}[/green]\n")

    choice = questionary.select(
        "What do you want to do?",
        choices=[
            "1. Execute",
            "2. Modify command",
            "3. Cancel",
        ],
        style=custom_style
        ).ask(),
    
    choice = " ".join(list(choice))
    
    if choice.startswith("1"):
        is_confirmed = questionary.confirm("Are you sure you want to execute this command?").ask()
        if is_confirmed:
            # console.print("[cyan] Executing...[/cyan]\n")
            subprocess.run(command, shell=True)
        # else:
        #     console.print("[red]🚫 Command cancelled.[/red]")

    elif choice.startswith("2"):
        new_cmd = questionary.text("📝 Modify the command:", default=command ).ask()
        
        if new_cmd:
            is_confirmed = questionary.confirm("Are you sure you want to execute this command?").ask()
            if is_confirmed:
                console.print("[cyan] Executing...[/cyan]\n")
                subprocess.run(new_cmd, shell=True)
            # else : 
            #     console.print("[red]🚫 Command cancelled.[/red]")

    else:
        # console.print("[red]🚫 Command cancelled.[/red]")
        pass

if __name__ == "__main__":
    main()
