from pathlib import Path
import json
import google.generativeai as genai
# from dotenv import load_dotenv
from aiassistcli.ai_prompt import build_prompt

CONFIG_DIR = Path.home() / ".ai-assist"
CONFIG_PATH = CONFIG_DIR / "config.json"

def save_api_key(key: str):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(json.dumps({"api_key": key}))
    
    # secure file permissions (Linux/macOS)
    # CONFIG_PATH.chmod(stat.S_IRUSR | stat.S_IWUSR)  # rw-------

def load_api_key() -> str | None:
    if CONFIG_PATH.exists():
        try:
            data = json.loads(CONFIG_PATH.read_text())
            return data.get("api_key")
        except Exception:
            return None
    return None

def get_command_from_ai(prompt, api_key):

    # Configure Gemini with the provided API key
    genai.configure(api_key=api_key)
    
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(build_prompt(prompt))
    return response.text.strip()
    
