# 🚀 Floworio — Setup Guide

## Brzi Start (5 minuta)

### 1️⃣ Pokreni Backend API

Otvori **Terminal 1**:

```bash
cd C:\Users\LENOVO\floworio\apps\api
python -m uvicorn main:app --reload --port 8000
```

✅ API će biti dostupan na: **http://localhost:8000**  
📚 API dokumentacija: **http://localhost:8000/docs**

---

### 2️⃣ Pokreni Frontend (Next.js)

Otvori **Terminal 2**:

```bash
cd C:\Users\LENOVO\floworio\apps\web
npm run dev
```

✅ Web app će biti dostupan na: **http://localhost:3000**

---

## 🔧 Podešavanje API Ključeva (Opciono)

### Za AI Story Generation

Otvori `C:\Users\LENOVO\floworio\apps\api\.env` i dodaj:

```env
# Odaberi jedan od ova dva:
OPENAI_API_KEY=sk-proj-...
# ILI
ANTHROPIC_API_KEY=sk-ant-...
```

**Gdje dobiti ključeve:**
- OpenAI: https://platform.openai.com/api-keys
- Anthropic: https://console.anthropic.com/

**Napomena:** Ako ne dodaš ključeve, sistem će koristiti template script (i dalje radi).

---

### Za Kokoro TTS (Voiceover)

```bash
pip install kokoro soundfile
```

GitHub: https://github.com/hexgrad/kokoro

---

### Za Social Media Publishing

U `.env` fajlu dodaj tokene za platforme koje želiš:

```env
# TikTok
TIKTOK_ACCESS_TOKEN=...

# Instagram
INSTAGRAM_ACCESS_TOKEN=...
INSTAGRAM_USER_ID=...

# YouTube
YOUTUBE_API_KEY=...
```

**Setup guide za svaku platformu:**
- TikTok: https://developers.tiktok.com/doc/content-posting-api-get-started
- Instagram: https://developers.facebook.com/docs/instagram-api/guides/reels
- YouTube: https://developers.google.com/youtube/v3

---

## 🧪 Testiranje

```bash
cd C:\Users\LENOVO\floworio\apps\api
python -m pytest tests/ -v
```

Trenutno: **14 testova** za upload i story generaciju.

---

## 🐳 Docker (Alternativa)

```bash
cd C:\Users\LENOVO\floworio\infrastructure
docker-compose up -d
```

Ovo pokreće:
- Next.js frontend (port 3000)
- FastAPI backend (port 8000)
- Redis (port 6379)

---

## 📊 Kako koristiti

1. **Upload Excel** — Drag & drop fajl sa podacima
2. **Configure** — Odaberi tip grafa (Bar Race, Pie, Line...), aspect ratio (9:16, 1:1, 16:9)
3. **AI Story** — Generiši narativ + voiceover (Kokoro TTS)
4. **Render** — Remotion renderuje video (React → MP4)
5. **Publish** — Objavi na TikTok, Instagram, YouTube, LinkedIn

---

## 🔍 Troubleshooting

### Frontend ne radi?
```bash
cd C:\Users\LENOVO\floworio\apps\web
npm install
npm run dev
```

### Backend ne radi?
```bash
cd C:\Users\LENOVO\floworio\apps\api
pip install -r requirements.txt
python -m uvicorn main:app --reload --port 8000
```

### Remotion rendering ne radi?
- Instaliraj FFmpeg: https://ffmpeg.org/download.html
- Dodaj FFmpeg u PATH

### Testovi ne prolaze?
```bash
pip install pytest pytest-asyncio
python -m pytest tests/ -v
```

---

## 📁 Struktura Projekta

```
C:\Users\LENOVO\floworio\
├── apps/
│   ├── web/              # Next.js frontend (localhost:3000)
│   └── api/              # FastAPI backend (localhost:8000)
├── packages/
│   └── types/            # Shared TypeScript types
├── infrastructure/
│   └── docker-compose.yml
└── README.md
```

---

## 🎯 Sljedeći Koraci

1. ✅ Pokreni oba servera (frontend + backend)
2. 📊 Uploaduj test Excel fajl
3. 🎨 Konfiguriši video
4. ✍️ Generiši AI story (ili preskoči)
5. 🎬 Renderuj video sa Remotion
6. 🚀 Objavi na social media

---

**Pitanja?** Otvori issue ili kontaktiraj tim.
