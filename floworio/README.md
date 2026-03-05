# 🎬 Floworio — Data Story SaaS Platform

> **Upload Excel → AI Story → Remotion Video → Social Media**

Turn your time-series data into viral animated videos with AI narration, published automatically to TikTok, Instagram, YouTube, and LinkedIn.

---

## 🏗️ Architecture

```
floworio/
├── apps/
│   ├── web/                    # Next.js 14 frontend
│   │   ├── src/
│   │   │   ├── app/            # Next.js App Router
│   │   │   ├── components/     # UI components (5-step wizard)
│   │   │   │   ├── upload/     # Excel file upload
│   │   │   │   ├── config/     # Chart configuration
│   │   │   │   ├── story/      # AI story + Kokoro TTS
│   │   │   │   ├── preview/    # Remotion video preview
│   │   │   │   └── publish/    # Social media publishing
│   │   │   ├── remotion/       # Remotion compositions
│   │   │   │   ├── BarRace.tsx # Bar chart race animation
│   │   │   │   └── Root.tsx    # Composition registry
│   │   │   └── store/          # Zustand state management
│   │   └── remotion.config.ts
│   └── api/                    # FastAPI Python backend
│       ├── main.py             # FastAPI app
│       └── routers/
│           ├── upload.py       # Excel upload + DataHandler (from sjvisualizer)
│           ├── story.py        # AI story generation (OpenAI/Anthropic)
│           ├── tts.py          # Kokoro TTS voiceover
│           ├── render.py       # Remotion video rendering
│           └── publish.py      # Social media publishing
└── infrastructure/
    └── docker-compose.yml
```

---

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- Python 3.11+
- FFmpeg (for audio mixing)

### 1. Clone & Install

```bash
git clone https://github.com/your-org/floworio.git
cd floworio

# Install frontend dependencies
cd apps/web
npm install

# Install backend dependencies
cd ../api
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Backend
cp apps/api/.env.example apps/api/.env
# Edit apps/api/.env with your API keys

# Frontend
cp apps/web/.env.example apps/web/.env.local
```

### 3. Start Development Servers

**Terminal 1 — Frontend:**
```bash
cd apps/web
npm run dev
# → http://localhost:3000
```

**Terminal 2 — Backend:**
```bash
cd apps/api
uvicorn main:app --reload --port 8000
# → http://localhost:8000
# → API docs: http://localhost:8000/docs
```

**Terminal 3 — Remotion Studio (optional):**
```bash
cd apps/web
npx remotion studio src/remotion/Root.tsx
# → http://localhost:3001
```

---

## 🔄 Complete Workflow

```
1. 📊 UPLOAD    → User uploads Excel/CSV file
                  → Python DataHandler interpolates data (from sjvisualizer)
                  → Returns data_id + column names + date range

2. 🎨 CONFIGURE → Select chart type (Bar Race, Pie, Line, Area, World Map)
                  → Choose aspect ratio (9:16 TikTok, 1:1 Instagram, 16:9 YouTube)
                  → Set title, subtitle, colors, duration, FPS

3. ✍️ AI STORY  → GPT-4 / Claude analyzes data and writes narration script
                  → Kokoro TTS (open-source) generates voiceover audio
                  → User can edit script and preview audio

4. 🎬 RENDER    → FastAPI sends data + config to Remotion
                  → Remotion renders React components as MP4 frames
                  → FFmpeg mixes video + voiceover audio
                  → Progress tracked via polling

5. 🚀 PUBLISH   → Select platforms (TikTok, Instagram, YouTube, LinkedIn)
                  → Add caption + hashtags (auto-generated from story)
                  → Publish immediately or schedule for later
```

---

## 🔧 Open Source Components

### 🎬 Remotion (Video Rendering)
- **GitHub**: https://github.com/remotion-dev/remotion
- **License**: MIT
- **Usage**: React-based programmatic video creation. Renders data animations server-side as high-quality MP4.

### 🎙️ Kokoro TTS (Voice Generation)
- **GitHub**: https://github.com/hexgrad/kokoro
- **License**: Apache 2.0
- **Usage**: 82M parameter open-source TTS model. 10 voices (EN/EN-GB). Runs locally, no API costs.
- **Install**: `pip install kokoro soundfile`

---

## 📊 Data Format

Your Excel file should have this structure:

| Date | Category 1 | Category 2 | Category 3 |
|------|-----------|-----------|-----------|
| 2020 | 1250 | 890 | 2100 |
| 2021 | 1480 | 1020 | 1950 |
| 2022 | 1720 | 1340 | 2300 |

- **First column**: Dates (year, full date, or month)
- **Other columns**: Data series (countries, companies, products, etc.)

---

## 🌐 Social Media APIs

| Platform | API | Formats | Setup |
|----------|-----|---------|-------|
| TikTok | Content Posting API v2 | 9:16 | [Docs](https://developers.tiktok.com/doc/content-posting-api-get-started) |
| Instagram | Graph API (Reels) | 9:16, 1:1 | [Docs](https://developers.facebook.com/docs/instagram-api/guides/reels) |
| YouTube | Data API v3 | 16:9, 9:16 | [Docs](https://developers.google.com/youtube/v3) |
| LinkedIn | Marketing API | 16:9, 1:1, 4:5 | [Docs](https://learn.microsoft.com/en-us/linkedin/marketing/) |

---

## 💰 SaaS Pricing Model

| Plan | Price | Videos/mo | Platforms | Voice |
|------|-------|-----------|-----------|-------|
| **Free** | $0 | 3 | 1 | ❌ |
| **Creator** | $19/mo | 30 | 3 | ✅ |
| **Pro** | $49/mo | 150 | All | ✅ Custom |
| **Agency** | $149/mo | Unlimited | All + API | ✅ |

---

## 🐳 Docker

```bash
cd infrastructure
docker-compose up -d
```

---

## 📝 Credits

- **sjvisualizer** by Sjoerd Tilmans — Data interpolation logic ported to REST API
  - GitHub: https://github.com/SjoerdTilmans/sjvisualizer
  - License: MIT

- **Remotion** — Video rendering engine
- **Kokoro TTS** — Open-source voice synthesis

---

## 📄 License

MIT License — see LICENSE file for details.

Built with ❤️ by the Floworio team.
