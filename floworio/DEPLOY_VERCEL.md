# 🚀 Floworio — Deploy na Vercel

## 📋 Što Trebam od Tebe

Za deployment trebam:

1. **GitHub Username** — Tvoj GitHub korisnik (npr. `bojandek`)
2. **GitHub Token** (opciono) — Za autentifikaciju
3. **Vercel Account** — Kreiraj na https://vercel.com/signup

---

## ⚡ Brz Deployment (5 minuta)

### Korak 1: Push Kod na GitHub

```bash
cd C:\Users\LENOVO\floworio

# Inicijalizuj Git (ako nije već)
git init

# Dodaj sve fajlove
git add .

# Kreiraj prvi commit
git commit -m "Initial commit: Floworio SaaS platform"

# Kreiraj repo na GitHub-u
# Otvori https://github.com/new
# Naziv: floworio
# Visibility: Public
# Klikni "Create repository"

# Postavi remote
git remote set-url origin https://github.com/bojandek/floworio.git

# Push kod
git push -u origin main
```

**Očekivani output:**
```
Enumerating objects: 74, done.
Counting objects: 100% (74/74), done.
...
To https://github.com/bojandek/floworio.git
 * [new branch]      main -> main
Branch 'main' is set up to track remote branch 'main' from 'origin'.
```

✅ **Kod je na GitHub-u:** https://github.com/bojandek/floworio

---

### Korak 2: Deploy Frontend na Vercel

#### Opcija A: Koristi Vercel CLI (Brže)

```bash
# Instaliraj Vercel CLI
npm i -g vercel

# Navigiraj u web folder
cd C:\Users\LENOVO\floworio\apps\web

# Deploy
vercel

# Odgovori na pitanja:
# - Scope: Tvoj nalog
# - Project name: floworio-web
# - Framework: Next.js
# - Build command: npm run build
# - Output directory: .next
# - Deploy: Yes
```

**Rezultat:** https://floworio-web.vercel.app

---

#### Opcija B: Koristi Vercel Web Interface (Preporučeno)

1. **Otvori Vercel**
   - https://vercel.com/dashboard

2. **Klikni "Add New..."**
   - Odaberi "Project"

3. **Odaberi GitHub Repo**
   - Klikni "Import Git Repository"
   - Odaberi `bojandek/floworio`

4. **Konfiguracija**
   - **Framework:** Next.js
   - **Root Directory:** `apps/web`
   - **Build Command:** `npm run build`
   - **Output Directory:** `.next`
   - **Environment Variables:** (ostavi prazno za sada)

5. **Deploy**
   - Klikni "Deploy"
   - Čekaj 2-3 minuta

**Rezultat:** https://floworio-web.vercel.app

---

### Korak 3: Deploy Backend na Railway (Alternativa)

Ako želiš da deployuješ i backend:

1. **Otvori Railway**
   - https://railway.app/

2. **Kreiraj Novi Projekt**
   - Klikni "New Project"
   - Odaberi "Deploy from GitHub"

3. **Odaberi Repo**
   - Odaberi `bojandek/floworio`

4. **Konfiguracija**
   - **Root Directory:** `apps/api`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`

5. **Environment Variables**
   - Dodaj ako trebaju (API ključevi, itd.)

6. **Deploy**
   - Klikni "Deploy"

**Rezultat:** https://floworio-api.railway.app

---

## 🔗 Povezivanje Frontend-a sa Backend-om

Ako si deployovao backend na Railway, trebam da ažuriram frontend:

### Kreiraj `.env.production` u `apps/web/`

```env
NEXT_PUBLIC_API_URL=https://floworio-api.railway.app
```

### Ili Koristi Vercel Environment Variables

1. Otvori Vercel Dashboard
2. Klikni na projekt
3. Otvori "Settings" → "Environment Variables"
4. Dodaj:
   - **Name:** `NEXT_PUBLIC_API_URL`
   - **Value:** `https://floworio-api.railway.app`
5. Redeploy

---

## ✅ Checklist za Deployment

- [ ] GitHub repo kreiran
- [ ] Kod pushovan na GitHub
- [ ] Vercel nalog kreiran
- [ ] Frontend deployovan na Vercel
- [ ] Frontend dostupan na https://floworio-web.vercel.app
- [ ] Backend deployovan na Railway (opciono)
- [ ] Backend dostupan na https://floworio-api.railway.app (opciono)
- [ ] Frontend i backend povezani (ako je backend deployovan)

---

## 🌐 Testiranje Deployed Aplikacije

### Test 1: Otvori Frontend
```
https://floworio-web.vercel.app
```

Trebalo bi da vidiš:
- Landing page sa pricing-om
- "Get Started" dugme
- Sve stranice dostupne

### Test 2: Provjeri API (ako je deployovan)
```
https://floworio-api.railway.app/docs
```

Trebalo bi da vidiš:
- Swagger dokumentacija
- Svi endpoint-i dostupni

### Test 3: Testiraj Navigaciju
```
Landing Page → Dashboard → Create → Templates
```

---

## 🔧 Troubleshooting

### Problem: Build Fails na Vercel

**Rješenje:**
```bash
# Provjeri build lokalno
cd apps/web
npm run build

# Ako build ne radi, provjeri:
# 1. Node verzija: node --version (trebalo bi 18+)
# 2. Dependencies: npm install
# 3. Build: npm run build
```

### Problem: API nije dostupan iz Frontend-a

**Rješenje:**
1. Provjeri da li je backend deployovan
2. Provjeri `NEXT_PUBLIC_API_URL` environment varijablu
3. Provjeri CORS u backend-u
4. Redeploy frontend

### Problem: Vercel ne nalazi `apps/web`

**Rješenje:**
1. Provjeri da li je `vercel.json` u root folder-u
2. Provjeri da li je `Root Directory` postavljen na `apps/web`
3. Redeploy

---

## 📊 Monitoring

### Vercel Dashboard
- https://vercel.com/dashboard
- Vidiš sve deploymente
- Vidiš logs
- Vidiš analytics

### Railway Dashboard
- https://railway.app/
- Vidiš sve deploymente
- Vidiš logs
- Vidiš metrics

---

## 🎯 Sljedeći Koraci

1. ✅ Push kod na GitHub
2. ✅ Deploy frontend na Vercel
3. ✅ Deploy backend na Railway (opciono)
4. ✅ Testiraj deployed aplikaciju
5. ✅ Dodaj custom domain (opciono)

---

## 📞 Pomoć

Ako nešto ne radi:

1. **Provjeri Vercel logs** — Dashboard → Project → Deployments
2. **Provjeri Railway logs** — Dashboard → Project → Logs
3. **Provjeri browser console** — F12 → Console
4. **Provjeri network** — F12 → Network

---

**Sretno sa deployment-om!** 🚀
