import argparse
from aiassistcli.ai_generate import AIGenerator
from aiassistcli.config import SUPPORTED_MODELS, configure, load_config
from .history import handle_history
from .run_prompt import run_prompt
from aiassistcli import __version__
from rich.console import Console

console = Console()

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

def main():
    parser = argparse.ArgumentParser(prog="ai", description="AI assistant CLI tool")
    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"%(prog)s {__version__}",
        help="Show version"
    )
    subparsers = parser.add_subparsers(dest="command")

    # ai configure
    subparsers.add_parser("configure", help="Configure your AI API key")

    # ai models list
    subparsers.add_parser("models-list", help="List available models")

    # ai history
    history_parser = subparsers.add_parser("history", help="Show command history")
    history_parser.add_argument("--search", help="Filter by keyword")
    history_parser.add_argument("--limit", type=int, default=10, help="Number of entries to show")
    history_parser.add_argument("action", nargs="?", choices=["clear"], help="Clear history")

    # ai <prompt>
    ask_parser = subparsers.add_parser("ask", help="Ask AI a question")
    ask_parser.add_argument("prompt", nargs=argparse.REMAINDER, help="Ask a question to the AI")
    ask_parser.add_argument("--refine", action="store_true", help="Refine the prompt before sending")

    args = parser.parse_args()

    if args.command == "configure":
        configure()

    elif args.command == "models-list":
        list_models()

    elif args.command == "history":
        handle_history(args)

    elif args.command == "ask":
        gen = AIGenerator()
        prompt = " ".join(args.prompt)
        final_prompt = prompt

        if args.refine:
            refined = gen.refine_prompt(prompt)
            final_prompt = refined

        run_prompt(final_prompt)
            
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
