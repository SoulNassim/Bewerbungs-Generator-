# 🧾 Bewerbungsgenerator Pro

> An AI-powered job application generator for the German job market — built with Python, tkinter, and GPT-3.5.

---

## ✨ Features

- 📝 **AI-generated cover letter text** via OpenAI GPT-3.5, tailored to the job and company
- 📄 **PDF export** of the finished cover letter (formatted, DIN A4)
- 📋 **CV import** (PDF or TXT) for automatic personalization of the AI text
- 🖊️ **Signature upload** — embed your handwritten signature directly into the PDF
- 💾 **Profile system** — save and reload your personal data across multiple applications
- 🎨 **Modern dark UI** using [ttkbootstrap](https://ttkbootstrap.readthedocs.io/) with the Superhero theme
- 🌐 **Fully in German** — tailored for the German application standard

---

## 🖥️ Screenshot

<!-- Add a screenshot of the app here -->
> Run the app and take a screenshot to showcase the UI!

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- An [OpenAI API Key](https://platform.openai.com/account/api-keys)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/soulzero04/BewerbungNew.git
   cd BewerbungNew
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API key:**

   Create a `.env` file in the project root:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

4. **Run the app:**
   ```bash
   python BewerbungNew.py
   ```

---

## 📦 Dependencies

| Package | Purpose |
|---|---|
| `openai` | AI text generation via GPT-3.5 |
| `ttkbootstrap` | Modern themed tkinter UI |
| `reportlab` | PDF generation |
| `PyPDF2` | Reading CV/resume PDFs |
| `python-dotenv` | Loading API keys from `.env` |

---

## 🗂️ How It Works

1. Fill in your **personal details** and the **company/job information**
2. Optionally upload your **CV** (PDF or TXT) for personalized AI text
3. Optionally upload a **signature image** to embed in the PDF
4. Click **"Bewerbung generieren & speichern"**
5. The app calls the OpenAI API to generate a tailored paragraph
6. The full cover letter is exported as both a `.txt` and a `.pdf` file

---

## 📁 File Output

Generated files are saved in the current directory with the naming convention:
```
Bewerbung_<Firmenname>_<Jobtitel>.pdf
Bewerbung_<Firmenname>_<Jobtitel>.txt
```

---

## ⚙️ Configuration

You can customize the AI writing style using the **"KI-Stil Anweisung"** field in the UI. For example:
- `"Schreibe professionell und überzeugend."` *(default)*
- `"Schreibe freundlich und enthusiastisch."`
- `"Formuliere knapp und präzise."`

---

## 🔒 Privacy

- Your personal data is stored **locally only** (in `profiles/*.json`)
- The `.env` file containing your API key is **excluded from version control** via `.gitignore`

---

## 📄 License

This project is for personal use. Feel free to fork and adapt it for your own job applications!

---

<p align="center">Made with ❤️ and Python</p>
