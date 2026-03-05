# 🚀 GitHub Setup — Floworio

## Korak 1: Kreiraj novi repo na GitHub-u

1. Otvori https://github.com/new
2. Popuni formu:
   - **Repository name:** `floworio`
   - **Description:** Data to viral video in 60 seconds
   - **Visibility:** Public
   - **Initialize repository:** Ne (ostavi prazno)
3. Klikni "Create repository"

## Korak 2: Push kod na GitHub

Kod je već commitovan lokalno. Sada trebam da ga pushnem:

```bash
cd C:\Users\LENOVO\floworio
git push -u origin main
```

## Korak 3: Verifikuj na GitHub-u

Otvori https://github.com/bojandek/floworio i provjeri da li je kod pushovan.

---

## 📁 Što će biti na GitHub-u

```
floworio/
├── apps/
│   ├── web/              # Next.js frontend
│   └── api/              # FastAPI backend
├── packages/
│   └── types/            # Shared TypeScript types
├── infrastructure/       # Docker setup
├── README.md
├── SETUP.md
├── DEPLOYMENT.md
├── HOSTING.md
├── vercel.json
├── railway.json
└── .gitignore
```

---

## 🎯 Sljedeći Koraci

1. ✅ Kreiraj repo na GitHub-u
2. ✅ Push kod: `git push -u origin main`
3. ✅ Deploy na Vercel (https://vercel.com/new)
4. ✅ Deploy na Railway (https://railway.app/)

**Aplikacija će biti live za 15 minuta!** 🚀
