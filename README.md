# 🤖 AI-Assist CLI (Powered by Gemini)

AI-Assist is a simple, interactive CLI tool that transforms natural language instructions into shell commands using Gemini AI. It enhances developer productivity by eliminating the need to search for command-line syntax.

---

## ✨ Features

- 🧠 **Natural language to command**: Ask in plain text, get a shell command back.
- 🎛️ **Interactive interface**: Modify, confirm, or cancel command execution.
- 🎨 **Rich UI**: Stylish terminal experience with `rich` and `questionary`.
- 🔐 **Safe by design**: Always asks for confirmation before running any command.

## 🛠️ Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/carellihoula/AssistantIACLI.git
   cd AssistantIACLI
   ```

2. Install dependencies:

   ```bash
   pixi shell
   ```

   ```bash
   pixi install
   ```

## 🚀 Usage

```bash
ai  [your instruction here]
```

### Example

```bash
ai list all docker containers
```

📦 Gemini will respond with:

```
docker ps -a
```

You’ll be prompted to:

- Execute the command directly
- Modify it before execution
- Cancel the operation

## 🧩 Tech Stack

- [Python 3.9+](https://www.python.org/)
- [Gemini AI API](https://ai.google.dev/)
- [`rich`](https://github.com/Textualize/rich) – for colorful output and spinners
- [`questionary`](https://github.com/tmbo/questionary) – for interactive CLI prompts

## 🔐 Disclaimer

This tool executes system commands. Always **read and review** generated commands before running them. Use at your own risk.

---

## 🧪 Development

To run locally for development:

```bash
python main.py "your natural language query"
```

## 🙌 Contributing

Pull requests and issues are welcome! If you'd like to improve the UX, support more shells, or add AI providers, feel free to fork and contribute.

## 📄 License

This project is licensed under the [MIT License](LICENSE).

Made with ❤️ by Carel Lihoula Ntsoumou
