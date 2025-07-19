
import os
import google.generativeai as genai
from dotenv import load_dotenv
from rich.console import Console
from aiassistcli.ai_prompt import build_prompt



load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

console = Console()

def get_command_from_ai(prompt):
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(build_prompt(prompt))
    return response.text.strip()