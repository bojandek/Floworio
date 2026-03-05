# 🔐 Rješavanje Git Autentifikacije

## Problem
```
remote: Permission to bojandek/floworio.git denied to premium-digital-dev.
fatal: unable to access 'https://github.com/bojandek/floworio.git/': The requested URL returned error: 403
```

Git je konfiguriran sa `premium-digital-dev` nalogom, a trebam `bojandek`.

---

## Rješenje 1: Resetuj Git Kredencijale (PREPORUČENO)

### Windows — Koristi Credential Manager

1. **Otvori Credential Manager:**
   - Pritisni `Win + R`
   - Upiši: `control /name Microsoft.CredentialManager`
   - Klikni OK

2. **Pronađi GitHub kredencijale:**
   - Klikni "Windows Credentials"
   - Pronađi `git:https://github.com` ili `github.com`
   - Klikni na nju i "Edit"
   - Promijeni korisničko ime na `bojandek`
   - Promijeni lozinku na **Personal Access Token (PAT)**

3. **Ako nema GitHub kredencijala:**
   - Klikni "Add a generic credential"
   - **Internet or network address:** `git:https://github.com`
   - **User name:** `bojandek`
   - **Password:** (tvoj GitHub PAT token)
   - Klikni "OK"

---

## Rješenje 2: Koristi SSH Ključ (ALTERNATIVA)

### Generiši SSH ključ

```powershell
ssh-keygen -t ed25519 -C "bojan@example.com"
# Pritisni Enter za sve pitanja
```

### Dodaj SSH ključ na GitHub

1. Otvori https://github.com/settings/keys
2. Klikni "New SSH key"
3. Kopiraj sadržaj iz: `C:\Users\LENOVO\.ssh\id_ed25519.pub`
4. Ulijepи u GitHub
5. Klikni "Add SSH key"

### Promijeni Git remote na SSH

```powershell
cd C:\Users\LENOVO\floworio
git remote set-url origin git@github.com:bojandek/floworio.git
git push -u origin main
```

---

## Rješenje 3: Koristi GitHub Personal Access Token (PAT)

### Kreiraj PAT

1. Otvori https://github.com/settings/tokens
2. Klikni "Generate new token" → "Generate new token (classic)"
3. Popuni:
   - **Note:** Floworio Push
   - **Expiration:** 90 days
   - **Scopes:** Odaberi `repo`
4. Klikni "Generate token"
5. **Kopiraj token** (neće se moći vidjeti ponovo!)

### Koristi PAT za push

```powershell
cd C:\Users\LENOVO\floworio
git push -u origin main
# Kada traži lozinku, ulijepи PAT token
```

---

## Rješenje 4: Resetuj Git Config

```powershell
# Resetuj globalni config
git config --global --unset user.name
git config --global --unset user.email

# Postavi novi config
git config --global user.name "bojandek"
git config --global user.email "bojan@example.com"

# Pokušaj push
cd C:\Users\LENOVO\floworio
git push -u origin main
```

---

## ✅ Checklist

- [ ] Otvori Credential Manager
- [ ] Resetuj GitHub kredencijale
- [ ] Postavi korisničko ime na `bojandek`
- [ ] Postavi lozinku na PAT token
- [ ] Pokreni: `git push -u origin main`
- [ ] Verifikuj na https://github.com/bojandek/floworio

---

## 🎉 Kada je Gotovo

Trebalo bi da vidiš:
```
Enumerating objects: 74, done.
...
To https://github.com/bojandek/floworio.git
 * [new branch]      main -> main
Branch 'main' is set up to track remote branch 'main' from 'origin'.
```

**Sretno!** 🚀
