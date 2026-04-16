# 🚀 Deployment Guide – Applify

Choose your favorite platform and get Applify live in minutes!

---

## 🌐 Platform Comparison

| Platform | Cost | Ease | Best For | Python |
|----------|------|------|----------|--------|
| **Railway** | Pay-as-you-go | ⭐⭐⭐⭐⭐ Easy | Beginners | ✅ Perfect |
| **Render** | Free tier | ⭐⭐⭐⭐ Easy | Learning | ✅ Great |
| **Heroku** | Paid only | ⭐⭐⭐⭐ Easy | Production | ✅ Good |
| **PythonAnywhere** | Free tier | ⭐⭐⭐ Medium | Students | ✅ Perfect |
| **AWS** | Free tier* | ⭐⭐ Hard | Advanced | ✅ Complex |

**Recommendation**: Start with **Railway** (easiest) or **Render** (free tier)

---

## 1️⃣ Railway (⭐ RECOMMENDED)

Easiest deployment for Python Flask apps!

### Steps

1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Create new project → Deploy from GitHub repo
4. Select `Bewerbungs-Generator-` repository
5. Railway auto-detects Flask app
6. Add environment variables:
   - `OPENAI_API_KEY` = your key
7. Deploy! ✅

**Time**: ~2 minutes  
**Cost**: Free tier ($5/month credit) or pay-as-you-go  
**URL**: `https://applify-[random].railway.app`

### Custom Domain
Railway Settings → Domain → Add custom domain

---

## 2️⃣ Render (Free Tier)

Great for learning & portfolios!

### Steps

1. Go to [render.com](https://render.com)
2. Sign up with GitHub
3. New Web Service → Connect GitHub repo
4. Settings:
   - **Name**: applify
   - **Build command**: `pip install -r requirements.txt`
   - **Start command**: `gunicorn app:app`
5. Add environment variable: `OPENAI_API_KEY`
6. Deploy! ✅

**Time**: ~3 minutes  
**Cost**: Free tier (with limitations) or paid  
**URL**: `https://applify.onrender.com`

### Note
Render auto-sleeps free tier after 15 min idle (restart on first request).

---

## 3️⃣ Heroku (Paid)

Professional, reliable hosting.

### Steps

1. Install [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
2. Login: `heroku login`
3. Create app: `heroku create applify-[yourname]`
4. Set API key: `heroku config:set OPENAI_API_KEY=sk-xxx`
5. Deploy:
   ```bash
   git push heroku main
   ```
6. View app: `heroku open`

**Time**: ~5 minutes  
**Cost**: Starting at $7/month  
**URL**: `https://applify-[yourname].herokuapp.com`

---

## 4️⃣ PythonAnywhere (Free Tier)

Best for Python beginners!

### Steps

1. Sign up at [pythonanywhere.com](https://www.pythonanywhere.com)
2. Upload code via git or file upload
3. Set up virtual environment
4. Configure Flask web app
5. Add API key in Environment variables
6. Enable app ✅

**Time**: ~10 minutes  
**Cost**: Free tier available  
**URL**: `https://[username].pythonanywhere.com`

---

## 5️⃣ Docker + Cloud Run / ECS / AKS

For advanced users & production!

### Dockerfile

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

### Deploy on Google Cloud Run

```bash
gcloud run deploy applify \
  --source . \
  --platform managed \
  --region us-central1 \
  --set-env-vars OPENAI_API_KEY=sk-xxx
```

**Time**: ~15 minutes  
**Cost**: Free tier available  
**URL**: `https://applify-[hash].run.app`

---

## Quick Deployment Commands

### Railway
```bash
railway link
railway deploy
```

### Render
```bash
# Just push to GitHub - Render auto-deploys on push!
git push origin main
```

### Heroku
```bash
heroku create applify-[yourname]
heroku config:set OPENAI_API_KEY=sk-xxx
git push heroku main
```

### PythonAnywhere
```bash
# Upload via web interface or
# Set up Git integration
```

---

## Pre-Deployment Checklist

- [ ] `requirements.txt` updated (`pip freeze > requirements.txt`)
- [ ] `.env` file NOT committed (in `.gitignore`)
- [ ] `OPENAI_API_KEY` set in platform environment
- [ ] Test locally: `python app.py` works
- [ ] No hardcoded secrets in code
- [ ] `FLASK_ENV=production` for production
- [ ] All files committed to GitHub

---

## Environment Variables

Every platform needs `OPENAI_API_KEY`:

```env
OPENAI_API_KEY=sk-your-key-here
FLASK_ENV=production
FLASK_DEBUG=False
```

---

## After Deployment

### Test Your App
```bash
curl https://your-applify-url.com
```

### Monitor
Most platforms provide:
- ✅ Logs
- ✅ Performance metrics
- ✅ Error tracking
- ✅ Uptime monitoring

### Custom Domain
Point your domain's DNS to your deployment URL:
- Railway: `*.railway.app`
- Render: `*.onrender.com`
- Heroku: `*.herokuapp.com`

---

## Troubleshooting

### App won't start
```bash
# Check logs:
railway logs          # Railway
render logs           # Render
heroku logs --tail    # Heroku
```

### API key not working
- Check environment variable is set correctly
- No quotes around key
- Restart app after changing

### Port issues
- Flask runs on port `$PORT` (platform sets this)
- Don't hardcode port 5000 for production

### Memory errors
- Upgrade to paid tier
- Optimize code (remove unused imports)

---

## Cost Breakdown

| Platform | Free | Paid |
|----------|------|------|
| Railway | $5 credit | Pay-as-you-go (~$5-20/month) |
| Render | Limited | $7+/month |
| Heroku | ❌ Discontinued | $7+/month |
| PythonAnywhere | Limited | $5+/month |
| Cloud Run | ~$2.90/month | Pay-as-you-go |

---

## Next Steps

1. **Choose platform** (Railway recommended)
2. **Commit code** to GitHub
3. **Connect GitHub** to platform
4. **Add API key** to environment
5. **Deploy** 🚀
6. **Test** the app
7. **Share** your URL! 🎉

---

## Support

- **Railway**: [@railway_app](https://twitter.com/railway_app)
- **Render**: [Support](https://render.com/docs)
- **Heroku**: [Dev Center](https://devcenter.heroku.com/)
- **PythonAnywhere**: [Help](https://www.pythonanywhere.com/help/)

---

Happy deploying! 🎉
