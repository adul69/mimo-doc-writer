# 📝 MiMo Doc Writer

> **AI-Powered Documentation Generator** — Built with MiMo AI V2.5

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)](https://flask.palletsprojects.com)
[![MiMo AI](https://img.shields.io/badge/MiMo-AI-orange.svg)](https://mimo.xiaomi.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Live Demo](https://img.shields.io/badge/Live%20Demo-Vercel-purple.svg)](https://mimo-doc-writer.vercel.app/)

---

## 🌐 Live Demo

**🔗 [Try MiMo Doc Writer](https://mimo-doc-writer.vercel.app/)**

Upload a repository or paste a GitHub URL to see MiMo AI in action!

---

## 📖 Overview

**MiMo Doc Writer** is an AI-powered documentation generator that uses **MiMo AI's reasoning capabilities** to analyze codebases and generate comprehensive documentation.

Unlike simple documentation tools, MiMo Doc Writer doesn't just describe code — it **explains the reasoning** behind design decisions, architecture choices, and implementation patterns.

### Key Differentiator

Most doc generators: *"This function takes X and returns Y"*  
MiMo Doc Writer: *"This function exists because [architectural reason]. It handles [edge case] by [approach], which is important because [business logic]."*

---

## 🎯 Features

| Feature | Description |
|---------|-------------|
| **Multi-Step Analysis** | SCAN → UNDERSTAND → GENERATE pipeline |
| **Deep Code Understanding** | Parses classes, functions, imports, dependencies |
| **Reasoning-Based Docs** | Explains WHY, not just WHAT |
| **Multiple Doc Types** | Full docs, README, API reference, Architecture |
| **GitHub Integration** | Direct repository analysis |
| **Multi-Language** | Python, JavaScript, TypeScript, Java, Go, Rust, etc. |
| **Real-Time Stats** | Shows files, classes, functions analyzed |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   MiMo Doc Writer                       │
├─────────────────────────────────────────────────────────┤
│  User Input (GitHub URL / File Upload)                  │
│    ↓                                                    │
│  ┌─────────────────────────────────────────────────────┐│
│  │  Multi-Step Analysis Pipeline                       ││
│  │                                                     ││
│  │  1. SCAN ─────→ Find files, structure, languages    ││
│  │       ↓                                             ││
│  │  2. UNDERSTAND → Parse code meaning, relationships  ││
│  │       ↓                                             ││
│  │  3. GENERATE ─→ MiMo AI creates documentation       ││
│  └─────────────────────────────────────────────────────┘│
│    ↓                                                    │
│  Structured Documentation (Markdown)                    │
└─────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/adul69/mimo-doc-writer.git
cd mimo-doc-writer
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
cp .env.example .env
# Edit .env with your MiMo API key
```

### 4. Run Application

```bash
python app.py
```

Visit `http://localhost:5000` and start generating documentation!

---

## 🔑 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `MIMO_API_KEY` | MiMo AI API key from [platform.xiaomimimo.com](https://platform.xiaomimimo.com) | Yes (for AI generation) |
| `MIMO_API_URL` | MiMo API endpoint | No (default: api.xiaomimimo.com/v1) |

> **Note:** Without API key, the app runs in demo mode with template-based documentation.

---

## 💡 How It Works

### Step 1: SCAN
- Traverses project directory
- Identifies supported file types (20+ languages)
- Builds file tree structure
- Calculates language distribution stats

### Step 2: UNDERSTAND
- Parses Python files for classes, functions, imports
- Parses JavaScript/TypeScript for components, hooks, imports
- Extracts dependency information
- Maps code relationships

### Step 3: GENERATE
- Sends structured context to MiMo AI
- MiMo's reasoning model analyzes code patterns
- Generates documentation explaining design decisions
- Outputs clean Markdown

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| **AI Model** | Xiaomi MiMo V2.5 (Reasoning) |
| **Backend** | Python + Flask |
| **Frontend** | Vanilla JS + Marked.js + Highlight.js |
| **Analysis** | Custom regex parser (Python, JS, TS, Java, Go, Rust) |
| **UI Style** | Dark theme, minimalist design |

---

## 📁 Project Structure

```
mimo-doc-writer/
├── app.py                  # Flask application & API endpoints
├── core/
│   ├── __init__.py
│   └── analyzer.py         # Multi-step code analysis engine
├── templates/
│   └── index.html          # Frontend UI
├── static/                 # (empty, CSS inline)
├── uploads/                # Temporary file uploads (gitignored)
├── requirements.txt
├── .env.example
├── .env                    # Your config (gitignored)
├── .gitignore
└── README.md
```

---

## 📊 Analysis Capabilities

### Supported Languages

| Language | Parsing |
|----------|---------|
| Python | Classes, functions, imports, decorators |
| JavaScript | Classes, functions, imports, requires |
| TypeScript | Interfaces, types, classes, functions |
| Java | Classes, methods, imports |
| Go | Structs, functions, imports |
| Rust | Structs, functions, uses |
| Ruby | Classes, methods, requires |
| PHP | Classes, functions, includes |

### Detected Patterns

- **Classes**: Name, parent class, file location
- **Functions**: Name, parameters, file location
- **Imports**: Module name, file location
- **Dependencies**: External packages (first-level)

---

## 🔐 Security Notes

- **Uploaded files** are stored temporarily in `uploads/` (gitignored)
- **API keys** should never be committed (`.env` is gitignored)
- **Demo mode** works without API keys for testing

---

## 🌐 Deployment

### PythonAnywhere (Free)

```bash
# Upload files to PythonAnywhere
# Set MIMO_API_KEY in .env
# Configure WSGI to point to app.py
```

### Vercel

```bash
npm i -g vercel
vercel --prod
```

### Railway

```bash
railway login
railway init
railway up
```

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing`)
5. Open Pull Request

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details

---

## 🙏 Acknowledgments

- **Xiaomi MiMo** — AI model powering the documentation generation
- **MiMo V2.5** — Reasoning capability for deep code understanding
- **MiMo API 开放平台** — Global API inference service

---

## 📧 Contact

- **GitHub**: [@adul69](https://github.com/adul69)
- **Project**: [MiMo Doc Writer](https://github.com/adul69/mimo-doc-writer)

---

<p align="center">
  Built with ❤️ using Xiaomi MiMo AI
</p>
