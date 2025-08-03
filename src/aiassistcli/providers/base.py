from abc import ABC, abstractmethod


class AIProvider(ABC):
    def __init__(self, api_key: str):
        self.api_key = api_key
        

    @abstractmethod
    def generate(self, model: str, prompt: str, refine: bool = False) -> str:
        pass

    @abstractmethod
    def explain_command(self, model: str, command: str) -> str:
        pass

    @abstractmethod
    def refine_prompt(self, model: str, prompt: str) -> str:
        pass

class AIError(Exception):
    """Custom exception for AI provider errors."""
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

