import requests
from importlib.metadata import version, PackageNotFoundError
from rich.console import Console

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