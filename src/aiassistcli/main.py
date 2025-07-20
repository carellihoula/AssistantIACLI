import subprocess
import sys
from aiassistcli.config import configure, explain_command_with_ai, load_api_key, get_command_from_ai, custom_style
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
import questionary
from questionary import Style


console = Console()


def main():

    if len(sys.argv) >= 2 and sys.argv[1] == "configure":
        configure()
        return
    
    if len(sys.argv) < 2:
        console.print("[red]❗ Usage: ai [natural language instruction][/red]")
        sys.exit(1)
    
    api_key = load_api_key()
    if not api_key:
        console.print("[red]❗No API key provided to Gemini API. Please run:[/red] [bold]ai configure[/bold]")
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
            command = get_command_from_ai(question, api_key=api_key)
        
    except Exception as e:
        console.print(f"[red]Gemini Error:[/red] {e}")
        sys.exit(1)

    console.print("\n[bold green]💡 Gemini suggests:[/bold green]")
    console.print(f"[green] {command}[/green]\n")

    # while True:
    choice = questionary.select(
            "What do you want to do?",
            choices=[
                "1. Execute",
                "2. Modify command",
                "3. Show command with explanation",
                "4. Exit",
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
            # break

    elif choice.startswith("2"):
            new_cmd = questionary.text("📝 Modify the command:", default=command ).ask()
            
            if new_cmd:
                is_confirmed = questionary.confirm("Are you sure you want to execute this command?").ask()
                if is_confirmed:
                    console.print("[cyan] Executing...[/cyan]\n")
                    subprocess.run(new_cmd, shell=True)
                # else : 
                #     console.print("[red]🚫 Command cancelled.[/red]")
            # break
                
    elif choice.startswith("3"):
            try:
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[grey] Explaining command...[/grey]"),
                    transient=True
                ) as progress:
                    progress.add_task("explaining", total=None)
                    explanation = explain_command_with_ai(command, api_key=api_key)
            except Exception as e:
                console.print(f"[red]Gemini Error:[/red] {e}")
                sys.exit(1)

            console.print(f"[green] {explanation}[/green]\n")

    else:
            # console.print("[red]🚫 Command cancelled.[/red]")
            pass
            # break

if __name__ == "__main__":
    main()
