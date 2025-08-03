import subprocess
import sys
from aiassistcli.ai_generate import AIGenerator
from aiassistcli.config import custom_style, load_config
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
import questionary
from .history import save_history

def run_prompt(prompt: str) -> None:

    console = Console()
    gen = AIGenerator()
    default_model = load_config().get("default_model")
    provider = default_model["provider"]
    
    console.print(f"[bold cyan]🧠 Query:[/bold cyan] {prompt}")
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[grey] Processing...[/grey]"),
            transient=True
        ) as progress:
            progress.add_task("thinking", total=None)
            command = gen.generate(prompt)
        
    except Exception as e:
        console.print(f"[red]Gemini Error:[/red] {e}")
        sys.exit(1)

    console.print(f"\n[bold green]💡 {provider} suggests:[/bold green]")
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
            ).ask()
        
    if choice.startswith("1"):
            is_confirmed = questionary.confirm("Are you sure you want to execute this command?").ask()
            if is_confirmed:
                # console.print("[cyan] Executing...[/cyan]\n")
                subprocess.run(command, shell=True)
                save_history(prompt, command, action="run")
            # else:
            #     console.print("[red]🚫 Command cancelled.[/red]")
            # break
            

    elif choice.startswith("2"):
            new_cmd = questionary.text("📝 Modify the command:", default=command ).ask()
            
            if new_cmd:
                is_confirmed = questionary.confirm("Are you sure you want to execute this command?").ask()
                if is_confirmed:
                    # console.print("[cyan] Executing...[/cyan]\n")
                    subprocess.run(new_cmd, shell=True)
                    save_history(prompt, new_cmd, action="run")
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
                    explanation = gen.explain_command(command)
            except Exception as e:
                console.print(f"[red]Gemini Error:[/red] {e}")
                sys.exit(1)

            console.print(f"[green] {explanation}[/green]\n")
            save_history(prompt, command, action="explain")

    else:
            # console.print("[red]🚫 Command cancelled.[/red]")
            save_history(prompt, command, action="cancel")
            # break