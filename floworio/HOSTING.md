# 🌐 Floworio — Hosting & Deployment Guide

## 🎯 Besplatne Opcije za Testiranje

### Option 1: Vercel (Frontend) + Railway (Backend) — PREPORUČENO ✅

**Prednosti:**
- Besplatno za testiranje
- Automatski deploy iz Git-a
- Skalabilno na produkciju
- Brzo i jednostavno

#### 1. Deploy Frontend na Vercel

```bash
# 1. Kreiraj Vercel nalog
# https://vercel.com/signup

# 2. Instaliraj Vercel CLI
npm i -g vercel

# 3. Deploy
cd C:\Users\LENOVO\floworio\apps\web
vercel

# Odgovori na pitanja:
# - Scope: Tvoj nalog
# - Project name: floworio-web
# - Framework: Next.js
# - Build command: npm run build
# - Output directory: .next
```

**Rezultat:** https://floworio-web.vercel.app

#### 2. Deploy Backend na Railway

```bash
# 1. Kreiraj Railway nalog
# https://railway.app/

# 2. Kreiraj novi projekt
# - New Project → GitHub Repo
# - Odaberi floworio repo
# - Odaberi apps/api folder

# 3. Dodaj environment varijable
# - OPENAI_API_KEY=...
# - TIKTOK_ACCESS_TOKEN=...
# - itd.

# 4. Deploy se dešava automatski
```

**Rezultat:** https://floworio-api.railway.app

---

### Option 2: Render (Frontend + Backend)

**Prednosti:**
- Sve na jednoj platformi
- Besplatno za testiranje
- Jednostavno za početnike

#### Deploy na Render

```bash
# 1. Kreiraj Render nalog
# https://render.com/

# 2. Frontend
# - New Web Service
# - Connect GitHub repo
# - Build command: npm run build
# - Start command: npm run start
# - Environment: Node

# 3. Backend
# - New Web Service
# - Connect GitHub repo
# - Build command: pip install -r requirements.txt
# - Start command: uvicorn main:app --host 0.0.0.0 --port 8000
# - Environment: Python 3.11
```

---

### Option 3: Docker + Heroku (Alternativa)

```bash
# 1. Kreiraj Heroku nalog
# https://www.heroku.com/

# 2. Instaliraj Heroku CLI
# https://devcenter.heroku.com/articles/heroku-cli

# 3. Login
heroku login

# 4. Kreiraj app
heroku create floworio-app

# 5. Dodaj environment varijable
heroku config:set OPENAI_API_KEY=sk-...

# 6. Deploy
git push heroku main
```

---

## 📋 Korak-po-Korak: Vercel + Railway (BEST)

### A. Pripremi Git Repo

```bash
cd C:\Users\LENOVO\floworio

# Inicijalizuj Git (ako nije već)
git init
git add .
git commit -m "Initial commit: Floworio SaaS platform"

# Kreiraj GitHub repo
# https://github.com/new
# Naziv: floworio

# Push na GitHub
git remote add origin https://github.com/YOUR_USERNAME/floworio.git
git branch -M main
git push -u origin main
```

### B. Deploy Frontend na Vercel

```bash
# 1. Otvori https://vercel.com/new
# 2. Klikni "Import Git Repository"
# 3. Odaberi floworio repo
# 4. Vercel će automatski detektovati vercel.json
# 5. Konfiguracija:
#    - Framework: Next.js
#    - Root Directory: (ostavi prazno - vercel.json će to obraditi)
#    - Build Command: npm run build
#    - Output Directory: .next
#    - Environment Variables: (ostavi prazno za sada)
# 6. Klikni "Deploy"
```

**Rezultat:** Tvoja aplikacija će biti dostupna na `https://floworio-web.vercel.app`

**Ako i dalje ne radi:**
```bash
# Testiraj lokalno
cd apps/web
npm run build
npm run start

# Ako build ne radi, provjeri:
# 1. Node verzija: node --version (trebalo bi 18+)
# 2. Dependencies: npm install
# 3. Build: npm run build
```

### C. Deploy Backend na Railway

```bash
# 1. Otvori https://railway.app/
# 2. Klikni "New Project"
# 3. Odaberi "Deploy from GitHub"
# 4. Odaberi floworio repo
# 5. Konfiguracija:
#    - Root Directory: apps/api
#    - Build Command: pip install -r requirements.txt
#    - Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
# 6. Dodaj Environment Variables:
#    - OPENAI_API_KEY=sk-...
#    - API_BASE_URL=https://floworio-api.railway.app
#    - FRONTEND_URL=https://floworio-web.vercel.app
# 7. Klikni "Deploy"
```

**Rezultat:** Tvoj API će biti dostupan na `https://floworio-api.railway.app`

### D. Ažuriraj Frontend da koristi Production API

Otvori `C:\Users\LENOVO\floworio\apps\web\src\app\layout.tsx` i dodaj:

```typescript
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'https://floworio-api.railway.app';
```

Ili kreiraj `.env.production`:

```env
NEXT_PUBLIC_API_URL=https://floworio-api.railway.app
```

---

## 🔐 Environment Variables za Production

### Frontend (.env.production)
```env
NEXT_PUBLIC_API_URL=https://floworio-api.railway.app
```

### Backend (Railway Config)
```env
API_BASE_URL=https://floworio-api.railway.app
FRONTEND_URL=https://floworio-web.vercel.app
OPENAI_API_KEY=sk-proj-...
ANTHROPIC_API_KEY=sk-ant-...
TIKTOK_ACCESS_TOKEN=...
INSTAGRAM_ACCESS_TOKEN=...
INSTAGRAM_USER_ID=...
YOUTUBE_API_KEY=...
LINKEDIN_ACCESS_TOKEN=...
DATABASE_URL=postgresql://...
REDIS_URL=redis://...
```

---

## ✅ Checklist za Deployment

- [ ] GitHub repo kreiran i push-ovan
- [ ] Vercel nalog kreiran
- [ ] Railway nalog kreiran
- [ ] Frontend deploy-ovan na Vercel
- [ ] Backend deploy-ovan na Railway
- [ ] Environment varijable postavljene
- [ ] Frontend ažuriran sa production API URL-om
- [ ] Testiran upload fajla
- [ ] Testirana AI story generacija
- [ ] Testiran video render

---

## 🧪 Testiranje Production Build-a Lokalno

```bash
# Frontend
cd apps/web
npm run build
npm run start
# Otvori http://localhost:3000

# Backend
cd apps/api
pip install -r requirements.txt
python -m uvicorn main:app --host 0.0.0.0 --port 8000
# Otvori http://localhost:8000/docs
```

---

## 📊 Monitoring & Logs

### Vercel
- Otvori https://vercel.com/dashboard
- Klikni na projekt
- Vidi "Deployments" i "Logs"

### Railway
- Otvori https://railway.app/
- Klikni na projekt
- Vidi "Logs" i "Metrics"

---

## 🚨 Troubleshooting

### Frontend ne radi nakon deploy-a
```bash
# Provjeri build
npm run build

# Provjeri environment varijable
echo $NEXT_PUBLIC_API_URL

# Redeploy
vercel --prod
```

### Backend vraća 502 Bad Gateway
```bash
# Provjeri logs na Railway
# Provjeri da li su sve zavisnosti instalirane
pip install -r requirements.txt

# Provjeri port
# Railway koristi $PORT environment varijablu
```

### API nije dostupan iz frontend-a
```bash
# Provjeri CORS
# Dodaj u main.py:
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://floworio-web.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 💰 Troškovi

| Servis | Besplatno | Plaćeno |
|--------|----------|---------|
| Vercel | ✅ 100GB/mo | $20/mo |
| Railway | ✅ $5/mo credit | Pay-as-you-go |
| Render | ✅ 750 sati/mo | $7/mo |
| Heroku | ❌ (ukinuto) | $7/mo |

**Za testiranje:** Sve je besplatno! 🎉

---

## 🎯 Sljedeći Koraci

1. ✅ Kreiraj GitHub repo
2. ✅ Deploy frontend na Vercel
3. ✅ Deploy backend na Railway
4. ✅ Testiraj production build
5. ✅ Dodaj custom domain (opciono)
6. ✅ Setup monitoring i alerts

**Tvoja aplikacija će biti live za 15 minuta!** 🚀
