# 🚀 Quick Start Guide – Modernized Bewerbungsgenerator

## 5-Minute Setup

### Step 1: Install Dependencies
```bash
cd "d:\Code Projects\Bewerbungs-Generator-"
pip install -r requirements.txt
```

### Step 2: Add Your API Key
Create `.env` file in the project root:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

### Step 3: Run the App
```bash
python app.py
```

### Step 4: Open in Browser
Visit: `http://localhost:5000`

---

## What Changed

| Old Version | New Version |
|------------|------------|
| Tkinter Desktop App | Modern Web App |
| Dark theme only | Beautiful gradient UI |
| Complex dialogs | Intuitive tabbed interface |
| No profile preview | Real-time preview |
| Static design | Smooth animations |

---

## Key Features

✅ **AI-Powered** – GPT-3.5 generates personalized cover letters
✅ **Modern UI** – Beautiful, responsive design
✅ **Profile Management** – Save multiple profiles
✅ **PDF Export** – Professional DIN A4 format
✅ **CV Upload** – Include your CV for better personalization
✅ **Signature Support** – Add your handwritten signature
✅ **No Installation Needed** – Runs in any web browser

---

## Troubleshooting

**"Module not found" error?**
```bash
pip install -r requirements.txt
```

**API Key not working?**
- Check your `.env` file format
- Ensure no spaces around the `=` sign
- Restart the Flask app after changing `.env`

**Port 5000 already in use?**
```bash
python app.py  # Edit app.py and change port to 5001
```

**PDF not downloading?**
- Check your browser's download settings
- Ensure all required fields are filled

---

## Deployment Options

### Local Network
```bash
python app.py  # Then access from: http://yourip:5000
```

### Docker (Optional)
```bash
docker build -t bewerbungsgenerator .
docker run -p 5000:5000 -e OPENAI_API_KEY=xxx bewerbungsgenerator
```

### Cloud Deployment
- Heroku, Railway, Render (free tier available)
- Just push the code and set `OPENAI_API_KEY` env variable

---

Enjoy! 🎉
