from pathlib import Path
import json
import questionary
from rich.console import Console
import pyperclip

CONFIG_DIR = Path.home() / ".ai-assist"
CONFIG_PATH = CONFIG_DIR / "config.json"

SUPPORTED_MODELS = {
    "openai": ["gpt-4o", "gpt-4o-mini"],
    "anthropic": ["claude-sonnet-4-20250514", "claude-opus-4-20250514", "claude-3-7-sonnet-20250219"],
    "deepseek": ["deepseek-chat", "deepseek-reasoner"],
    "gemini": ["gemini-2.0-flash", "gemini-2.0-pro"],
}

DEFAULT_PROVIDER = "gemini"
DEFAULT_MODEL = "gemini-2.0-flash"

# 🎨 Custom style for questionary
custom_style = questionary.Style([
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

console = Console()

def save_config(config: dict):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(json.dumps(config, indent=2))

def load_config() -> dict:
    if CONFIG_PATH.exists():
        return json.loads(CONFIG_PATH.read_text())
    return {}

def configure():
    choice = questionary.select(
        "Select configuration mode:",
        choices=[
            "1. Use default (Gemini Flash)",
            "2. Choose another provider/model",
        ],
        style=custom_style
    ).ask()

    config = load_config()

    if choice.startswith("1"):
        # Cas 1 : default Gemini Flash
        api_key = questionary.password("🔐 Enter your Gemini API key:", style=custom_style).ask()

        if not api_key:
            console.print("[red]❌ No API key entered. Aborting.[/red]")
            return

        config["default_model"] = {
            "provider": DEFAULT_PROVIDER,
            "model": DEFAULT_MODEL,
        }
        config.setdefault("providers", {})[DEFAULT_PROVIDER] = {"api_key": api_key}
        save_config(config)

        console.print(
            f"[white bold]Active model: [/white bold] [green]{DEFAULT_PROVIDER}/{DEFAULT_MODEL}[/green]"
             " - You can now use: [bold cyan]ai ask <your prompt>[/bold cyan]"
        )


    else:
        provider = questionary.select(
            "Select provider:", choices=list(SUPPORTED_MODELS.keys()), style=custom_style
        ).ask()

        model = questionary.select(
            "Select model:", choices=SUPPORTED_MODELS[provider], style=custom_style
        ).ask()

        api_key = questionary.password(f"🔐 Enter your API key for {provider}:", style=custom_style).ask()
        if not api_key:
            console.print("[red]❌ No API key entered.[/red]")
            return

        config["default_model"] = {"provider": provider, "model": model}
        config.setdefault("providers", {})[provider] = {"api_key": api_key}
        save_config(config)

        console.print(
            f"[white bold]Active model: [/white bold][green]{provider}/{model}[/green]"
            " - You can now use: [bold cyan]ai ask <your prompt>[/bold cyan]"
        )

def list_models():
    console.print("\n[bold cyan]Available models[/bold cyan]:")
    for provider, models in SUPPORTED_MODELS.items():
        for model in models:
            console.print(f" - {provider}/{model}")
    config = load_config()
    default_model = config.get("default_model")
    if default_model:
        console.print(
            f"\n[green]✔ Default: {default_model['provider']}/{default_model['model']}[/green]"
        )
    else:
        console.print("\n[red] No default model configured.[/red]")
    
def copy_command(command: str):
    pyperclip.copy(command)
    # console.print(f"[green]✅ Command copied to clipboard![/green] Paste it in your terminal with [cyan]Ctrl+V[/cyan] or [cyan]Right‑Click → Paste[/cyan].")