# 🚀 Floworio — Quick Start Guide

## ⚡ Brzo Pokretanje Cijele Aplikacije

### Korak 1: Pripremi Okruženje

```bash
# Otvori PowerShell kao Administrator
# Navigiraj u floworio folder
cd C:\Users\LENOVO\floworio
```

### Korak 2: Pokreni Backend (Terminal 1)

```bash
# Otvori prvi terminal (PowerShell)
cd C:\Users\LENOVO\floworio\apps\api

# Instaliraj zavisnosti (prvi put)
pip install -r requirements.txt

# Pokreni API server
python -m uvicorn main:app --reload --port 8000
```

**Očekivani output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Application startup complete
```

✅ **Backend je pokrenut na:** http://127.0.0.1:8000

---

### Korak 3: Pokreni Frontend (Terminal 2)

```bash
# Otvori drugi terminal (PowerShell)
cd C:\Users\LENOVO\floworio\apps\web

# Instaliraj zavisnosti (prvi put)
npm install

# Pokreni development server
npm run dev
```

**Očekivani output:**
```
> next dev
  ▲ Next.js 14.0.0
  - Local:        http://localhost:3000
  - Environments: .env.local

✓ Ready in 2.5s
```

✅ **Frontend je pokrenut na:** http://localhost:3000

---

## 🌐 Otvori Aplikaciju

### U Browser-u Otvori:

1. **Landing Page (Početna stranica)**
   - http://localhost:3000
   - Vidiš Apple-style hero sa pricing-om

2. **Dashboard (Pregled projekata)**
   - http://localhost:3000/dashboard
   - Vidiš sve tvoje projekte

3. **Create Project (Kreiraj projekt)**
   - http://localhost:3000/create
   - 5-step wizard za kreiranje videa

4. **Templates (Upravljanje template-ima)**
   - http://localhost:3000/templates
   - Vidiš sve dostupne template-e

5. **API Documentation (Swagger)**
   - http://127.0.0.1:8000/docs
   - Interaktivna API dokumentacija

---

## 🧪 Testiranje Aplikacije

### Test 1: Provjeri Landing Page
```
1. Otvori http://localhost:3000
2. Trebalo bi da vidiš:
   - Naslov "Type a topic. Get a viral video. In 60 seconds."
   - Pricing sekcija sa 4 plana
   - "Get Started" dugme
3. Klikni "Get Started" → trebalo bi da odeš na /dashboard
```

### Test 2: Provjeri Dashboard
```
1. Otvori http://localhost:3000/dashboard
2. Trebalo bi da vidiš:
   - Statistiku (Total Videos, This Month, Published, Views)
   - "New Project" dugme
   - Primjer projekata (ako postoje)
3. Klikni "New Project" → trebalo bi da odeš na /create
```

### Test 3: Provjeri Create Wizard
```
1. Otvori http://localhost:3000/create
2. Trebalo bi da vidiš:
   - 5 koraka: Upload → Configure → Story → Preview → Publish
   - Upload zona za fajlove
3. Klikni na različite korake da testirate navigaciju
```

### Test 4: Provjeri Templates
```
1. Otvori http://localhost:3000/templates
2. Trebalo bi da vidiš:
   - Template Manager sa filterima po tipu chart-a
   - "Novi Template" dugme
   - Filteri: Bar Race, Pie Race, Line Chart, Area Chart, World Map
3. Klikni "Novi Template" da kreirate template
```

### Test 5: Provjeri API
```
1. Otvori http://127.0.0.1:8000/docs
2. Trebalo bi da vidiš:
   - Swagger UI sa svim API endpoint-ima
   - 7 routers: Upload, Story, TTS, Render, Publish, Templates, Advanced Templates
3. Klikni na endpoint da vidiš detalje
```

---

## 🔧 Troubleshooting

### Problem: Backend ne pokreće se

**Rješenje:**
```bash
# Provjeri Python verziju
python --version  # Trebalo bi 3.8+

# Provjeri da li su zavisnosti instalirane
pip list | grep fastapi

# Ako nedostaju, instaliraj ponovo
pip install -r requirements.txt

# Pokušaj sa drugačitim portom
python -m uvicorn main:app --reload --port 8001
```

### Problem: Frontend ne pokreće se

**Rješenje:**
```bash
# Provjeri Node verziju
node --version  # Trebalo bi 18+

# Obriši node_modules i reinstaliraj
rm -r node_modules
npm install

# Pokušaj sa drugačitim portom
npm run dev -- -p 3001
```

### Problem: Port je već u upotrebi

**Rješenje:**
```bash
# Pronađi proces koji koristi port
netstat -ano | findstr :8000  # Za backend
netstat -ano | findstr :3000  # Za frontend

# Ubij proces (zamijeni PID sa brojem iz output-a)
taskkill /PID <PID> /F

# Ili koristi drugačit port
python -m uvicorn main:app --reload --port 8001
npm run dev -- -p 3001
```

### Problem: CORS greške

**Rješenje:**
```
Ako vidiš CORS greške u browser console-u:
1. Provjeri da li je backend pokrenut na http://127.0.0.1:8000
2. Provjeri da li je frontend pokrenut na http://localhost:3000
3. Restartuj oba servera
```

---

## 📊 Testiranje API-ja sa cURL

### Test Upload Endpoint
```bash
curl -X POST "http://127.0.0.1:8000/api/upload" \
  -H "Content-Type: application/json" \
  -d '{"filename": "test.xlsx"}'
```

### Test Story Endpoint
```bash
curl -X POST "http://127.0.0.1:8000/api/story" \
  -H "Content-Type: application/json" \
  -d '{"data": "test data", "tone": "engaging"}'
```

### Test Templates List
```bash
curl "http://127.0.0.1:8000/api/templates/list"
```

### Test Advanced Templates List
```bash
curl "http://127.0.0.1:8000/api/templates/advanced/list"
```

---

## 🎯 Kompletan Test Scenario

### 1. Pokreni Backend i Frontend
```bash
# Terminal 1
cd C:\Users\LENOVO\floworio\apps\api
python -m uvicorn main:app --reload --port 8000

# Terminal 2
cd C:\Users\LENOVO\floworio\apps\web
npm run dev
```

### 2. Otvori Browser
```
http://localhost:3000
```

### 3. Testiraj Navigaciju
```
Landing Page → Dashboard → Create → Templates → API Docs
```

### 4. Testiraj Funkcionalnosti
```
- Klikni "Get Started" na landing page-u
- Otvori "New Project" na dashboard-u
- Kreiraj novi template na templates page-u
- Provjeri API dokumentaciju
```

### 5. Provjeri Console
```
- Otvori DevTools (F12)
- Provjeri Console tab za greške
- Provjeri Network tab za API pozive
```

---

## ✅ Checklist za Testiranje

- [ ] Backend pokrenut na http://127.0.0.1:8000
- [ ] Frontend pokrenut na http://localhost:3000
- [ ] Landing page se učitava
- [ ] Dashboard se učitava
- [ ] Create wizard se učitava
- [ ] Templates page se učitava
- [ ] API Swagger docs se učitavaju
- [ ] Nema CORS grešaka
- [ ] Nema JavaScript grešaka u console-u
- [ ] Sve navigacijske veze rade
- [ ] Svi dugmadi su klikabilni

---

## 🚀 Sljedeći Koraci

1. ✅ Pokreni backend i frontend
2. ✅ Testiraj sve stranice
3. ✅ Testiraj API endpoint-e
4. ✅ Kreiraj template
5. ✅ Push na GitHub
6. ✅ Deploy na Vercel + Railway

---

## 📞 Pomoć

Ako nešto ne radi:

1. **Provjeri logs** — Pogledaj output u terminalima
2. **Provjeri browser console** — F12 → Console tab
3. **Provjeri network** — F12 → Network tab
4. **Restartuj servere** — CTRL+C i pokreni ponovo
5. **Obriši cache** — CTRL+SHIFT+Delete u browser-u

---

**Sretno sa testiranjem!** 🎉
