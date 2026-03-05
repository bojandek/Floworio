# 📤 Push Floworio na GitHub

## 🎯 Korak-po-Korak Instrukcije

### Korak 1: Kreiraj novi repo na GitHub-u

1. **Otvori GitHub**
   - Idi na https://github.com/new
   - Ili klikni na "+" u gornjem desnom uglu → "New repository"

2. **Popuni formu:**
   - **Repository name:** `floworio`
   - **Description:** Data to viral video in 60 seconds
   - **Visibility:** Public ✅
   - **Initialize this repository with:** Ne čekaj (ostavi prazno)
   - Klikni "Create repository"

3. **Kopira instrukcije sa GitHub-a**
   - GitHub će ti pokazati instrukcije za push
   - Trebalo bi da vidiš nešto kao:
   ```bash
   git remote add origin https://github.com/bojandek/floworio.git
   git branch -M main
   git push -u origin main
   ```

### Korak 2: Push kod iz PowerShell-a

Otvori PowerShell i pokreni:

```powershell
cd C:\Users\LENOVO\floworio
git push -u origin main
```

**Očekivani output:**
```
Enumerating objects: 74, done.
Counting objects: 100% (74/74), done.
Delta compression using up to 8 threads
Compressing objects: 100% (59/59), done.
Writing objects: 100% (74/74), done.
Total 74 (delta 0), reused 0 (delta 0), pack-reused 0 (from 0)
remote: 
remote: Create a pull request for 'main' on GitHub by visiting:
remote:      https://github.com/bojandek/floworio/pull/new/main
remote: 
To https://github.com/bojandek/floworio.git
 * [new branch]      main -> main
Branch 'main' is set up to track remote branch 'main' from 'origin'.
```

### Korak 3: Verifikuj na GitHub-u

1. Otvori https://github.com/bojandek/floworio
2. Trebalo bi da vidiš sve fajlove:
   - `apps/web/` — Frontend
   - `apps/api/` — Backend
   - `packages/types/` — Shared types
   - `infrastructure/` — Docker
   - `README.md`, `SETUP.md`, `DEPLOYMENT.md`, `HOSTING.md`

---

## 🔐 Ako Trebam Autentifikaciju

Ako GitHub traži lozinku, trebam **Personal Access Token (PAT)**:

1. Otvori https://github.com/settings/tokens
2. Klikni "Generate new token" → "Generate new token (classic)"
3. Popuni:
   - **Note:** Floworio Push
   - **Expiration:** 90 days
   - **Scopes:** Odaberi `repo` (full control of private repositories)
4. Klikni "Generate token"
5. **Kopiraj token** (neće se moći vidjeti ponovo!)
6. Kada PowerShell traži lozinku, **ulijepи token umjesto lozinke**

---

## ✅ Checklist

- [ ] Kreiraj repo na https://github.com/new
- [ ] Naziv: `floworio`
- [ ] Visibility: Public
- [ ] Klikni "Create repository"
- [ ] Pokreni: `git push -u origin main`
- [ ] Verifikuj na https://github.com/bojandek/floworio

---

## 🎉 Rezultat

Kada je sve gotovo, trebalo bi da vidiš:

```
https://github.com/bojandek/floworio
```

Sa svim fajlovima:
- 49 files changed
- 16,435 insertions
- Full-stack SaaS platform

---

## 🚀 Sljedeći Koraci

1. ✅ Push na GitHub
2. ✅ Deploy na Vercel (https://vercel.com/new)
3. ✅ Deploy na Railway (https://railway.app/)
4. ✅ Aplikacija će biti live za 15 minuta!

**Sretno!** 🎉
