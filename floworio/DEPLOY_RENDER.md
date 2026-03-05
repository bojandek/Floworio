# 🚀 Floworio — Deploy na Render

## 📋 Što je Render?

Render je besplatna platforma za hosting:
- ✅ Frontend (Next.js)
- ✅ Backend (Python/FastAPI)
- ✅ Databases
- ✅ Cron jobs
- ✅ Besplatno za male projekte

---

## ⚡ Brz Deployment na Render (10 minuta)

### Korak 1: Kreiraj Render Nalog

1. Otvori https://render.com
2. Klikni "Sign up"
3. Odaberi "Sign up with GitHub"
4. Autorizuj Render pristup GitHub-u

### Korak 2: Kreiraj Novi Projekt

1. Otvori https://dashboard.render.com
2. Klikni "New +" → "Web Service"
3. Odaberi "bojandek/floworio" repo
4. Klikni "Connect"

### Korak 3: Konfiguracija za Frontend

**Postavke:**
- **Name:** `floworio-web`
- **Environment:** Node
- **Build Command:** `cd apps/web && npm install && npm run build`
- **Start Command:** `cd apps/web && npm start`
- **Plan:** Free

**Environment Variables:**
```
NEXT_PUBLIC_API_URL=https://floworio-api.onrender.com
```

Klikni "Create Web Service"

### Korak 4: Kreiraj Backend Servis

1. Klikni "New +" → "Web Service"
2. Odaberi isti repo
3. Klikni "Connect"

**Postavke:**
- **Name:** `floworio-api`
- **Environment:** Python
- **Build Command:** `cd apps/api && pip install -r requirements.txt`
- **Start Command:** `cd apps/api && uvicorn main:app --host 0.0.0.0 --port $PORT`
- **Plan:** Free

**Environment Variables:**
```
PYTHONUNBUFFERED=1
```

Klikni "Create Web Service"

---

## 🔗 Rezultat

Kada su oba servisa deployovana:

```
✅ Frontend dostupan na: https://floworio-web.onrender.com
✅ Backend dostupan na: https://floworio-api.onrender.com
✅ API Docs dostupni na: https://floworio-api.onrender.com/docs
```

---

## 🧪 Testiraj Aplikaciju

### Test 1: Otvori Frontend
```
https://floworio-web.onrender.com
```

Trebalo bi da vidiš:
- Landing page sa pricing-om
- "Get Started" dugme
- Sve stranice dostupne

### Test 2: Provjeri API
```
https://floworio-api.onrender.com/docs
```

Trebalo bi da vidiš:
- Swagger dokumentacija
- Svi endpoint-i dostupni

### Test 3: Testiraj Navigaciju
```
Landing Page → Dashboard → Create → Templates
```

---

## ⚠️ Napomene za Render

### Free Plan Ograničenja
- ✅ Besplatno
- ⚠️ Spavaju nakon 15 minuta neaktivnosti
- ⚠️ Limitirani resursi
- ✅ Dovoljan za testiranje

### Ako Trebaju Bolji Performansi
Upgrade na Starter plan ($7/mjesec):
- Nema spavanja
- Bolji performansi
- Više resursa

---

## 🔧 Troubleshooting

### Problem: Build Fails

**Rješenje:**
1. Provjeri Render logs
2. Provjeri da li su sve zavisnosti instalirane
3. Provjeri build command

### Problem: Frontend ne može pristupiti Backend-u

**Rješenje:**
1. Provjeri `NEXT_PUBLIC_API_URL` environment varijablu
2. Provjeri da li je backend dostupan
3. Provjeri CORS u backend-u

### Problem: Servis spava

**Rješenje:**
1. Otvori aplikaciju da je "probudi"
2. Upgrade na Starter plan
3. Koristi cron job da je drži aktivnom

---

## 📊 Monitoring

### Render Dashboard
- https://dashboard.render.com
- Vidiš sve servise
- Vidiš logs
- Vidiš metrics

---

## 🎯 Sljedeći Koraci

1. ✅ Kreiraj Render nalog
2. ✅ Deploy frontend
3. ✅ Deploy backend
4. ✅ Testiraj aplikaciju
5. ✅ (Opciono) Upgrade na Starter plan

---

## 📞 Pomoć

Ako nešto ne radi:

1. **Provjeri Render logs** — Dashboard → Service → Logs
2. **Provjeri build output** — Dashboard → Service → Build Logs
3. **Provjeri environment varijable** — Dashboard → Service → Environment
4. **Restartuj servis** — Dashboard → Service → Restart

---

**Sretno sa Render deployment-om!** 🚀
