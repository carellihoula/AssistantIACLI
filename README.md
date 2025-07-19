# Canoaicli – AI in your terminal

**Canoaicli** is a minimalist and intelligent command-line tool. It lets you generate terminal commands from simple natural language instructions, powered by Google Gemini AI.

---

## 🚀 Installation

Make sure you have **Python ≥ 3.11**, then install it easily from PyPI:

```bash
pip install canoaicli
```

## 🧠 Configuration

Before starting, configure your Gemini API key (get one from [Google AI Studio](https://makersuite.google.com/app/apikey)):

```bash
ai configure
```

This will prompt you for your API key, which will be stored securely on your system.

---

## 💡 Usage

Once installed and configured, use AI directly in your terminal:

```bash
ai <your command>
```

Examples:

```bash
ai how to list all docker containers
ai delete all git branches except main
```

The tool will show you the appropriate shell commands, clearly and ready to be copied or run.

## 🛠️ Features

- Generate bash/git/docker commands from natural language
- Fast and smooth usage
- Interactive interface (thanks to `rich` and `questionary`)
- Secure Gemini API key configuration
- Open source and extensible

---

## 📦 Local development

To contribute to the project:

```bash
git clone https://github.com/carellihoula/AssistantIACLI.git
```

```bash
cd AssistantIACLI
```

```bash
pixi shell
```

```bash
pixi install
```

---

## 📃 License

MIT

---

## ✨ Demo video

_(coming soon)_ 🎥
