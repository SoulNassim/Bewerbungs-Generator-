# Applify - German Cover Letter Generator

A web app that generates German cover letters using GPT-3.5. I built this because writing applications is tedious and I wanted to speed up the process.

This started as a Python CLI script, evolved into a Tkinter desktop app, and is now a modern Flask web app with a live A4 preview.

---

## What it does

- You fill in your details (name, company, job title)
- Optionally upload your CV (PDF/TXT) 
- Click a button
- GPT-3.5 writes a personalized German cover letter
- You see it in real-time on an editable A4 preview
- Download as PDF or copy to clipboard

That's it. Saves maybe 30 minutes per application.

---

## Quick Start

```bash
cd Bewerbungs-Generator-
python -m venv venv
source venv/Scripts/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
echo "OPENAI_API_KEY=sk-your-key-here" > .env
python app.py
# Open http://localhost:5000
```

You'll need an [OpenAI API key](https://platform.openai.com/account/api-keys) (the free tier is enough).

---

## Features

**Core stuff:**
- AI generates cover letters using your CV context
- Real-time A4 preview - see changes as you type
- Save profiles for quick reuse
- PDF download
- Copy to clipboard

**Nice-to-haves:**
- 4 different layouts (Classic, Modern, Minimal, Compact)
- 3 font options 
- Signature upload
- Debug mode with sample data for testing
- Mobile responsive

---

## How it looks

**Form + Live Preview:**

The left side has all your inputs (company name, job title, your details). The right side shows exactly what the cover letter will look like. Click anywhere on the preview to edit it directly.

**Editable A4 Document:**

Everything is contenteditable, so you can tweak the AI output however you want before downloading.

---

## Tech Stack

**Backend:**
- Flask (Python)
- OpenAI API for generation
- ReportLab for PDF creation
- PyPDF2 for CV parsing
- JSON for profile storage

**Frontend:**
- HTML/CSS (vanilla, no frameworks)
- Vanilla JavaScript (kept it simple)
- Google Fonts (Inter typeface)
- Responsive CSS Grid

No React, no build tools, no complexity. Just HTML/CSS/JS that works.

---

## Architecture

**Server side (`app.py`):**
- 8 REST endpoints
- Handles profile CRUD
- Calls OpenAI API
- Generates PDFs
- Parses uploaded CVs

**Client side (`templates/index.html`):**
- Single page app
- Tab-based UI 
- Contenteditable A4 preview
- Form validation
- File uploads with drag-drop

The whole thing is about 2500 lines of code total.

---

## Why I Built This

1. **Authenticity** - The German job market has specific conventions. AI helps but needs context.
2. **Speed** - Writing 10+ applications per week gets old fast.
3. **Learning** - Good practice for API integration, PDF generation, Flask basics.
4. **Portfolio** - Shows I can build a complete product end-to-end.

---

## 📖 How to Use

### 1️⃣ Enter Your Profile
- Go to **Profil** tab
- Fill in personal details
- **Optional**: Save as profile for reuse

## How to Use

1. Fill Profil tab
2. Fill Firma tab 
3. Upload CV (optional)
4. Click generate
5. Edit & download

---

## Deployment

It's just Flask, deploy anywhere. See [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed steps for each platform.

**Quick options:**
- Railway - reliable, easy
- Render - has free tier
- PythonAnywhere - straightforward  
- Docker + any cloud

---

## Troubleshooting

`ModuleNotFoundError` → Run `pip install -r requirements.txt`  
API key errors → Check `.env` format (no quotes)  
Port in use → Change port in `app.py`  
CV extraction fails → Use readable PDFs (not scanned)

---

## API

8 REST endpoints for profile management, CV parsing, generation, PDF export. See code for details.

---

## License

Open source. Use for personal/portfolio purposes.

