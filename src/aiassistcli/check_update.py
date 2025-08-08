import requests
from importlib.metadata import version, PackageNotFoundError
from rich.console import Console
from pathlib import Path
from packaging.version import parse as parse_version
import importlib.metadata
import shutil

console = Console()

def check_update(package="canoaicli"):
    try:
        current_version = version(package)

        # latest version available on PyPI
        response = requests.get(f"https://pypi.org/pypi/{package}/json", timeout=3)
        latest_version = response.json()["info"]["version"]

        if current_version != latest_version:
            console.print(f"\n[bold yellow]🔔 Update available :[/] [green]{latest_version}[/] "
              f"(you have [red]{current_version}[/])\n"
              f"👉 [bold cyan]pip install --upgrade {package}[/]\n")

    except PackageNotFoundError:
        pass
        # print("Package not found")


def remove_old_config_once(package="canoaicli"):
    config_path = Path.home() / ".ai-assist" / "config.json"
    backup_path = config_path.with_suffix(".json.bak")
    flag_path = Path.home() / ".ai-assist" / ".old_config_removed"

    # Skip if config has already been removed previously
    if flag_path.exists():
        return

    try:
        # Check currently installed version of the package
        current_version = version(package)
        print(f"Current installed version: {current_version}")
        # If version is older than 2.0.0 and config file exists
        if parse_version(current_version) == parse_version("2.0.0"):
            if config_path.exists():
                # Back up the existing config file
                shutil.copy2(config_path, backup_path)

                config_path.unlink()

                console.print(f"[bold green][INFO][/bold green] Old configuration removed. A backup was saved as: [bold]{backup_path}[/bold]")

        # Create a flag file to ensure this runs only once
        flag_path.parent.mkdir(parents=True, exist_ok=True)
        flag_path.write_text("old config removed\n")

    except PackageNotFoundError:
        pass
    except Exception as e:
        console.print(f"[bold yellow][WARNING][/bold yellow] Error during config cleanup: {e}")
