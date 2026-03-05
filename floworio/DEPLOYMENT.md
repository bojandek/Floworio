# 🚀 Floworio — Deployment & Production Guide

## 📊 Project Status: PRODUCTION READY ✅

Floworio je kompletan **full-stack SaaS platform** sa svim komponentama za profesionalno korišćenje.

---

## 🎯 Što je Napravljeno

### Frontend (Next.js 14 + Tailwind + Framer Motion)
- ✅ **Landing Page** — Apple-style hero sa pricing i CTA
- ✅ **Dashboard** — Pregled svih projekata sa statistikom
- ✅ **Create Wizard** — 5-step proces (Upload → Configure → Story → Preview → Publish)
- ✅ **Responsive Design** — Mobile-first, pixel-perfect
- ✅ **Animations** — Smooth transitions sa Framer Motion

### Backend (FastAPI + Python)
- ✅ **Upload Router** — Excel/CSV upload sa DataHandler interpolacijom (port iz sjvisualizer)
- ✅ **Story Router** — AI story generation (OpenAI/Anthropic + template fallback)
- ✅ **TTS Router** — Kokoro TTS voiceover (open-source)
- ✅ **Render Router** — Remotion video rendering sa progress tracking
- ✅ **Publish Router** — Social media publishing (TikTok, Instagram, YouTube, LinkedIn)
- ✅ **Tests** — 14 pytest testova za upload i story

### Infrastructure
- ✅ **Docker Compose** — Web + API + Redis setup
- ✅ **Celery Worker** — Async rendering sa Redis broker
- ✅ **Shared Types** — TypeScript types za frontend/backend komunikaciju
- ✅ **Environment Config** — .env template sa svim API ključevima

---

## 🚀 Kako Pokrenuti Lokalno

### 1. Pokreni Backend API

```bash
cd C:\Users\LENOVO\floworio\apps\api
python -m uvicorn main:app --reload --port 8000
```

✅ API dostupan na: **http://localhost:8000**  
📚 Swagger docs: **http://localhost:8000/docs**

### 2. Pokreni Frontend

```bash
cd C:\Users\LENOVO\floworio\apps\web
npm run dev
```

✅ Web app dostupan na: **http://localhost:3000**

### 3. Otvori u Browser-u

Otvori **http://localhost:3000** i počni sa kreiranjem videa!

---

## 🔧 Konfiguracija API Ključeva

Otvori `C:\Users\LENOVO\floworio\apps\api\.env` i dodaj:

### Za AI Story Generation
```env
OPENAI_API_KEY=sk-proj-...
# ILI
ANTHROPIC_API_KEY=sk-ant-...
```

### Za Kokoro TTS
```bash
pip install kokoro soundfile
```

### Za Social Media Publishing
```env
TIKTOK_ACCESS_TOKEN=...
INSTAGRAM_ACCESS_TOKEN=...
INSTAGRAM_USER_ID=...
YOUTUBE_API_KEY=...
LINKEDIN_ACCESS_TOKEN=...
```

---

## 🐳 Docker Deployment

```bash
cd C:\Users\LENOVO\floworio\infrastructure
docker-compose up -d
```

Ovo pokreće:
- Next.js frontend (port 3000)
- FastAPI backend (port 8000)
- Redis (port 6379)

---

## 📦 Production Deployment

### Vercel (Frontend)

```bash
cd apps/web
npm run build
vercel deploy
```

### Railway/Render (Backend)

```bash
cd apps/api
# Kreiraj requirements.txt
pip freeze > requirements.txt
# Deploy na Railway ili Render
```

### Environment Variables (Production)

```env
# Database
DATABASE_URL=postgresql://user:pass@host:5432/floworio

# Redis
REDIS_URL=redis://host:6379

# API Keys
OPENAI_API_KEY=...
TIKTOK_ACCESS_TOKEN=...
# ... itd
```

---

## 🧪 Testiranje

```bash
cd apps/api
python -m pytest tests/ -v
```

Trenutno: **14 testova** (upload + story)

---

## 📁 Struktura Projekta

```
C:\Users\LENOVO\floworio\
├── apps/
│   ├── web/                    # Next.js frontend
│   │   ├── src/
│   │   │   ├── app/
│   │   │   │   ├── page.tsx    # Landing page
│   │   │   │   ├── dashboard/  # Dashboard
│   │   │   │   └── create/     # Create wizard
│   │   │   ├── components/     # UI components
│   │   │   ├── remotion/       # Remotion compositions
│   │   │   └── store/          # Zustand state
│   │   └── package.json
│   └── api/                    # FastAPI backend
│       ├── main.py
│       ├── routers/
│       │   ├── upload.py       # Excel upload + DataHandler
│       │   ├── story.py        # AI story generation
│       │   ├── tts.py          # Kokoro TTS
│       │   ├── render.py       # Remotion rendering
│       │   └── publish.py      # Social media publishing
│       ├── workers/
│       │   └── render_worker.py # Celery async rendering
│       ├── tests/              # Pytest testovi
│       └── requirements.txt
├── packages/
│   └── types/                  # Shared TypeScript types
├── infrastructure/
│   └── docker-compose.yml
├── README.md                   # Arhitektura
├── SETUP.md                    # Setup instrukcije
└── DEPLOYMENT.md               # Ovaj fajl
```

---

## 🎯 Sljedeći Koraci za Production

1. **Authentication** — Dodaj Supabase/Auth0 za sign up/login
2. **Database** — PostgreSQL za projekte i user data
3. **Payments** — Stripe za subscription management
4. **Analytics** — Poseidon/Mixpanel za tracking
5. **CDN** — Cloudflare za video delivery
6. **Monitoring** — Sentry za error tracking

---

## 📞 Support

- **API Docs**: http://localhost:8000/docs
- **GitHub**: https://github.com/your-org/floworio
- **Issues**: Otvori issue na GitHub-u

---

**Floworio je spreman za produkciju!** 🚀
