from rich.console import Console
from aiassistcli.providers.openai_compatible import OpenAICompatibleProvider
from aiassistcli.providers.gemini_provider import GeminiProvider
from aiassistcli.config import load_config

console = Console()

PROVIDER_URLS = {
    "openai": "https://api.openai.com/v1/",
    "anthropic": "https://api.anthropic.com/v1/",
    "deepseek": "https://api.deepseek.com",
}

class AIGenerator:
    def __init__(self):
        self.config = load_config()
        self.providers = {}

    def _get_provider(self, provider_name: str):
        if provider_name in self.providers:
            return self.providers[provider_name]

        api_key = self.config.get("providers", {}).get(provider_name, {}).get("api_key")
        if not api_key:
            console.print(f"[red]❗ No API key configured for {provider_name}[/red]")
            return None

        if provider_name in PROVIDER_URLS:
            provider = OpenAICompatibleProvider(api_key, PROVIDER_URLS[provider_name])
        elif provider_name == "gemini":
            provider = GeminiProvider(api_key)
        else:
            console.print(f"[red]❗ Unknown provider: {provider_name}[/red]")
            return None

        self.providers[provider_name] = provider
        return provider

    def generate(self, prompt: str) -> str | None:
        default_model = self.config.get("default_model")
        if not default_model:
            console.print("[red]❗ No default model configured. Run 'ai configure' first[/red]")
            return None

        provider_name = default_model["provider"]
        model_id = default_model["model"]
        provider = self._get_provider(provider_name)
        if not provider:
            return None

        # console.print(f"[cyan]Using {provider_name}/{model_id}[/cyan]")
        response = provider.generate(model_id, prompt)
        return response

    def explain_command(self, command: str) -> str | None:
        default_model = self.config.get("default_model")
        if not default_model:
            console.print("[red]❗ No default model configured. Run 'ai configure' first[/red]")
            return None

        provider_name = default_model["provider"]
        model_id = default_model["model"]
        provider = self._get_provider(provider_name)
        if not provider:
            return None

        # console.print(f"[cyan]Explaining with {provider_name}/{model_id}[/cyan]")
        response = provider.explain_command(model_id, command)
        return response
    
    def refine_prompt(self, prompt: str) -> str | None:
        default_model = self.config.get("default_model")
        if not default_model:
            console.print("[red]❗ No default model configured. Run 'ai configure' first[/red]")
            return None

        provider_name = default_model["provider"]
        model_id = default_model["model"]
        provider = self._get_provider(provider_name)
        if not provider:
            return None

        refined = provider.refine_prompt(model_id, prompt)
        return refined
