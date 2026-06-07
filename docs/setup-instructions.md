# Setup Instructions

This guide explains how to run MemoMeet locally.

Repository: https://github.com/manish-12ys/MemoMeet

## 1. Install Git

Make sure Git is installed on your system.

Check Git installation:

```bash
git --version
```

## 2. Install Python

Install Python 3.10 or newer.

Check Python installation:

```bash
python --version
```

On some systems, the command may be:

```bash
python3 --version
```

## 3. Install UV

UV is a fast Python package and environment manager. You can use it to create a virtual environment and install dependencies.

### Windows

Using PowerShell as administator:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Restart the terminal after installation, then check:

```powershell
uv --version
```

### macOS

Using curl:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Restart the terminal or reload your shell, then check:

```bash
uv --version
```

### Linux

Using curl:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Restart the terminal or reload your shell, then check:

```bash
uv --version
```

## 4. Clone the Repository

```bash
git clone https://github.com/manish-12ys/MemoMeet.git
cd MemoMeet
```

## 5. Create a Virtual Environment with UV

```bash
uv venv
```

## 6. Activate the Virtual Environment

### Windows

```powershell
.venv\Scripts\activate
```

### macOS and Linux

```bash
source .venv/bin/activate
```

## 7. Install Dependencies

```bash
uv sync
```

## 8. Configure Environment Variables

Create a `.env` file from the example file.

### Windows PowerShell

```powershell
Copy-Item .env.example .env
```

### macOS and Linux

```bash
cp .env.example .env
```

Then open the `.env` file and add the required values. The Groq key is required for the AI memory and preparation features:

```env
SECRET_KEY=change-me-in-production
DATABASE_URL=sqlite:///memomeet.db
GROQ_API_KEY=your-groq-api-key
GROQ_MODEL=openai/gpt-oss-120b
GROQ_FALLBACK_MODEL=qwen/qwen3-32b
GROQ_API_URL=https://api.groq.com/openai/v1/chat/completions
```

Keep real API keys only in your local `.env` file or deployment provider secrets. Do not commit live keys to documentation or source control.

## 9. Run the Application

```bash
python main.py
```

If your system uses `python3`, run:

```bash
python3 main.py
```

## 10. Open the App

After the server starts, open the local URL shown in the terminal.

Usually, it will be:

```text
http://127.0.0.1:5000
```

## Alternative: Standard Python Virtual Environment

If you do not want to use UV, you can use Python's built-in virtual environment.

Create the environment:

```bash
uv venv
```

Activate it on Windows:

```powershell
venv\Scripts\activate
```

Activate it on macOS or Linux:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
uv sync
```

Run the app:

```bash
python main.py
```
