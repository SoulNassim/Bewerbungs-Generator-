# 🎯 Bewerbungsgenerator Pro – Modernized Edition

> A sleek, modern web application for generating AI-powered German job applications with a beautiful UI

---

## ✨ Features

- 🤖 **AI-Powered Cover Letters** – Uses OpenAI GPT-3.5 to generate tailored cover letters
- 🎨 **Modern Web UI** – Beautiful, responsive design with gradient backgrounds and smooth animations
- 📱 **Fully Responsive** – Works perfectly on desktop, tablet, and mobile devices
- 💾 **Profile Management** – Save, load, and manage multiple application profiles
- 📄 **PDF Export** – Generate professional DIN A4 cover letters with your signature
- 📎 **CV Import** – Upload PDF or TXT files for AI context
- ✍️ **Signature Upload** – Include your handwritten signature in generated PDFs
- 🚀 **Real-time Preview** – See your cover letter before downloading
- 📊 **Statistics** – Track your generated applications

---

## 🛠️ Tech Stack

**Backend:**
- Python 3.9+
- Flask + Flask-CORS
- OpenAI API (GPT-3.5)
- ReportLab (PDF generation)
- PyPDF2 (PDF parsing)

**Frontend:**
- HTML5 + CSS3 (modern design with gradients & animations)
- Vanilla JavaScript (no framework bloat)
- Responsive Grid Layout

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- OpenAI API Key ([Get one here](https://platform.openai.com/account/api-keys))

### Installation

1. **Clone/Navigate to the repository:**
   ```bash
   cd Bewerbungs-Generator-
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # Windows
   # or
   source venv/bin/activate      # Linux/Mac
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your API key:**
   Create a `.env` file in the project root:
   ```env
   OPENAI_API_KEY=your_api_key_here
   ```

5. **Run the application:**
   ```bash
   python app.py
   ```

6. **Open in your browser:**
   ```
   http://localhost:5000
   ```

---

## 📖 How to Use

1. **Enter Your Information**
   - Navigate to the "Persönlich" tab and fill in your details
   - Save as a profile for future use

2. **Add Company Details**
   - Go to "Unternehmen" tab
   - Enter the job title, company name, and contact information

3. **Customize Settings**
   - In "Einstellungen" tab:
     - Upload your CV (PDF/TXT) for AI context
     - Upload your signature (optional)
     - Customize the AI writing style

4. **Generate Application**
   - Click "✨ Bewerbung generieren"
   - View the preview on the right side
   - Copy to clipboard or download as PDF

---

## 📁 Project Structure

```
Bewerbungs-Generator-/
├── app.py                 # Flask backend
├── requirements.txt       # Python dependencies
├── .env                   # API keys (create this)
├── templates/
│   └── index.html        # Modern web interface
├── profiles/             # Saved user profiles (auto-created)
└── README.md             # This file
```

---

## 🎨 Design Highlights

- **Modern Gradient UI** – Purple/blue gradient background with glassmorphic cards
- **Smooth Animations** – Fade-in effects on page load
- **Tab Navigation** – Organized sections for personal, company, and settings
- **Real-time Preview** – See your cover letter as you work
- **Responsive Layout** – Grid-based design that adapts to all screen sizes
- **Professional Color Scheme** – Clean, modern aesthetic suitable for portfolio display

---

## 🔧 Customization

### Changing the AI Writing Style
Edit the default prompt in `index.html`:
```javascript
<textarea id="stylePrompt" placeholder="...">
Schreibe professionell, freundlich und überzeugend.
</textarea>
```

### Modifying the Design
The UI is pure CSS in `index.html`. Key colors:
- Primary: `#667eea` (purple)
- Secondary: `#764ba2` (darker purple)
- Background: Linear gradient from primary to secondary

---

## 📝 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/profiles` | GET | List all saved profiles |
| `/api/profile/<name>` | GET | Load a profile |
| `/api/profile/<name>` | POST | Save a profile |
| `/api/delete-profile/<name>` | DELETE | Delete a profile |
| `/api/extract-cv` | POST | Extract text from CV file |
| `/api/generate-application` | POST | Generate cover letter with AI |
| `/api/generate-pdf` | POST | Generate PDF from cover letter |

---

## ⚙️ Environment Variables

Create a `.env` file with:
```env
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxx
```

---

## 📄 License

This project is open source and available for personal and portfolio use.

---

## 🤝 Contributing

Feel free to fork and submit pull requests for improvements!

---

## 📧 Support

For issues or questions, open an issue on GitHub or contact the maintainer.

---

**Happy Job Hunting! 🚀**
