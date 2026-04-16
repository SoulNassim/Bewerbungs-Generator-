# 🎯 Applify - AI-Powered German Job Application Generator

> **Professional cover letters generated in seconds with AI** — Fully redesigned from desktop app to beautiful modern web platform

<div align="center">

**[🌐 Live Demo](https://applify.nassim.dev) • [📖 Docs](./QUICKSTART.md) • [🤖 Features](#-features) • [💻 Tech](#-tech-stack)**

---

### 🎨 Modern Web Interface
Clean, responsive design with real-time A4 preview  
Multiple layouts • Live editing • Professional PDFs

</div>

---

## 🌟 What's New in v2.0

**Complete transformation from Tkinter desktop app to Flask web app!**

| Aspect | v1 (Desktop) | v2 (Web) |
|--------|------------|---------|
| **Platform** | Windows/Mac/Linux desktop | Any browser, any device |
| **UI** | Dark Tkinter theme | 🎨 Modern gradient design |
| **Preview** | Text-only editor | 📄 Live A4 WYSIWYG editor |
| **Editing** | Dialog boxes | ✏️ Click anywhere to edit |
| **Layouts** | 1 option | 4 professional styles |
| **Speed** | Slow startup | ⚡ Instant & responsive |
| **Responsiveness** | Fixed window | 📱 Desktop/tablet/mobile |

---

## ✨ Key Features

### 🤖 AI-Powered Generation
- **GPT-3.5 Integration** – Generates personalized, professional cover letters
- **Smart Context** – Uses your CV for better personalization
- **Customizable Style** – Control tone, formality, and key points
- **Real-time** – Get results in 3-5 seconds

### 🎨 Beautiful Modern Design
- **Gradient UI** – Purple/blue gradient with smooth animations
- **Responsive** – Perfect on desktop, tablet, and mobile
- **Professional** – Modern design suitable for your portfolio
- **Accessible** – Dark mode support, keyboard navigation

### 📄 Professional Documents
- **4 Layouts**: Classic, Modern, Minimal, Compact
- **3 Fonts**: Helvetica, Times New Roman, Courier
- **Live Preview**: See exactly how it looks (A4 format)
- **Fully Editable**: Click anywhere to make changes
- **Signature Support**: Add your handwritten signature
- **PDF Export**: Professional, download-ready files

### 💾 Smart Profile Management
- **Save Profiles** – Store personal & company details
- **Quick Load** – Reuse profiles for multiple applications
- **JSON Storage** – Simple, portable format

### 🎯 Additional Features
- ✅ CV/Resume upload (PDF/TXT auto-extract)
- ✅ Copy to clipboard
- ✅ Statistics tracking
- ✅ Debug mode with test data
- ✅ Drag-drop file uploads

---

## 🚀 Quick Start (5 Minutes)

### Requirements
- Python 3.9+
- OpenAI API Key ([free tier available](https://platform.openai.com/account/api-keys))

### Installation

```bash
# 1. Clone/Navigate
cd Bewerbungs-Generator-

# 2. Create virtual environment
python -m venv venv
source venv/Scripts/activate  # Windows
source venv/bin/activate      # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup API key
echo "OPENAI_API_KEY=sk-your-key-here" > .env

# 5. Run
python app.py

# 6. Open browser
# http://localhost:5000
```

---

## 📖 How to Use

### 1️⃣ Enter Your Profile
- Go to **Profil** tab
- Fill in personal details
- **Optional**: Save as profile for reuse

### 2️⃣ Company Details
- Switch to **Firma** tab
- Enter job title, company, contact info

### 3️⃣ Upload CV (Optional)
- Go to **Optionen** tab  
- Upload CV (PDF/TXT) for AI personalization

### 4️⃣ Generate
- Click **✨ Bewerbung generieren**
- Wait 3-5 seconds for AI to work

### 5️⃣ Edit & Export
- **Edit**: Click anywhere in document
- **Style**: Use **Tools** tab to change layout/font
- **Download**: Get PDF or copy to clipboard

---

## 💻 Tech Stack

### Backend
- **Framework**: Flask 3.0.0
- **API**: RESTful endpoints
- **PDF**: ReportLab 4.0.7 (generation)
- **AI**: OpenAI GPT-3.5-turbo
- **Files**: PyPDF2 (CV extraction)

### Frontend
- **HTML5** + **CSS3** – Modern responsive design
- **Vanilla JavaScript** – No framework overhead
- **Google Fonts** – Inter typeface
- **Responsive Grid** – Mobile-first layout

### Design
- **Colors**: Purple gradient (`#667eea` → `#764ba2`)
- **Animations**: Smooth CSS transitions
- **Icons**: Emoji for friendly UX
- **Accessibility**: WCAG compliant

---

## 📁 Project Structure

```
Bewerbungs-Generator-/
├── app.py                    # Flask backend
├── requirements.txt          # Python dependencies  
├── .env                      # API keys (create this)
├── templates/
│   └── index.html           # Web interface
├── profiles/                # Saved profiles (JSON)
├── README.md                # This file
└── QUICKSTART.md            # Quick reference
```

---

## 🔧 Configuration

### Environment Variables
```env
OPENAI_API_KEY=sk-your-openai-api-key
FLASK_ENV=development    # or production
FLASK_DEBUG=True        # or False for production
```

### API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| `GET` | `/` | Load web interface |
| `GET` | `/api/profiles` | List all profiles |
| `GET` | `/api/profile/<name>` | Load profile |
| `POST` | `/api/profile/<name>` | Save profile |
| `DELETE` | `/api/delete-profile/<name>` | Delete profile |
| `POST` | `/api/extract-cv` | Parse CV file |
| `POST` | `/api/generate-application` | Generate cover letter |
| `POST` | `/api/preview-pdf` | PDF preview |
| `POST` | `/api/generate-pdf` | Download PDF |

---

## 🚀 Deployment

### Local Network
```bash
python app.py
# Access: http://your-ip:5000
```

### Vercel (Recommended for Portfolio)
```bash
npm install -g vercel
vercel
```

### Docker
```bash
docker build -t applify .
docker run -p 5000:5000 -e OPENAI_API_KEY=sk-xxx applify
```

### Heroku / Railway / Render
Push to GitHub → Connect repo → Set env variables → Deploy

---

## 💡 Tips

**Speed Up**
- Save your profile → Reuse for multiple companies
- Upload CV once → AI learns your background

**Better Results**
- Detail your CV with achievements
- Customize "KI-Schreibstil" for each industry
- Highlight relevant skills

**Perfect PDF**
- Try different layouts in **Tools**
- Edit before downloading
- Choose fonts wisely (Helvetica = traditional, Times = creative)

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` |
| API key errors | Check `.env` format (no quotes/spaces) |
| Port 5000 in use | Change port in `app.py` or stop process |
| PDF not downloading | Check browser download settings |
| CV extraction fails | Ensure PDF is readable (not image scan) |

---

## 📊 Performance

- **Generation**: 3-5 seconds
- **PDF Size**: ~150-200 KB
- **API Calls**: 1 per generation
- **Storage**: ~1-2 KB per profile
- **Browser Support**: All modern browsers

---

## 🤝 Contributing

Want to help improve Applify?

1. Fork repo
2. Create feature branch: `git checkout -b feature/awesome`
3. Commit: `git commit -m "Add awesome feature"`
4. Push: `git push origin feature/awesome`
5. Open pull request

---

## 🎓 Learning Resources

This codebase demonstrates:
- ✅ Flask REST API architecture
- ✅ Client-side form handling
- ✅ PDF generation with Python
- ✅ OpenAI API integration
- ✅ Modern CSS/JS (no frameworks!)
- ✅ File upload & processing
- ✅ JSON persistence
- ✅ Async patterns
- ✅ Error handling

Perfect for your portfolio! 🚀

---

## 📜 License

Open source for personal and portfolio use.

---

## 🙋 Support

- **Issues**: GitHub Issues tab
- **Discussions**: GitHub Discussions
- **Quick Help**: See [QUICKSTART.md](./QUICKSTART.md)

---

## 📝 Version History

### v2.0 (Current) – 🎉 Complete Redesign
- ✨ Flask web app (was Tkinter desktop)
- 🎨 Modern UI with gradient design
- 📄 Live A4 preview with editing
- 🔤 4 layout styles + 3 fonts
- 📱 Fully responsive design
- ⚡ Better performance

### v1.0 – Original Desktop App
- Tkinter GUI
- PDF generation
- Profile management

---

<div align="center">

### 🌟 Made with ❤️ for Job Hunters

[⭐ Star on GitHub](https://github.com/SoulNassim/Bewerbungs-Generator-) • [🐛 Report Issue](https://github.com/SoulNassim/Bewerbungs-Generator-/issues) • [💬 Discuss](https://github.com/SoulNassim/Bewerbungs-Generator-/discussions)

![Python](https://img.shields.io/badge/Python-3.9+-3776ab?style=flat-square&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0-black?style=flat-square&logo=flask)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Status](https://img.shields.io/badge/Status-Production-brightgreen?style=flat-square)

</div>

