# 🚀 Déploiement sur Railway + Vercel

## Architecture
- **Railway** : Backend API (Flask + Claude AI)
- **Vercel** : Frontend (HTML statiques)

---

## 🔧 ÉTAPE 1 : Déployer le backend sur Railway

### 1.1 Créer un compte Railway
👉 Allez sur [railway.app](https://railway.app) et connectez-vous avec GitHub

### 1.2 Créer un nouveau projet
1. Cliquez sur **"New Project"**
2. Choisissez **"Deploy from GitHub repo"**
3. Autorisez Railway à accéder à vos repos GitHub
4. Sélectionnez le repo de votre projet ontologie

### 1.3 Configurer les variables d'environnement
Dans Railway, allez dans l'onglet **Variables** et ajoutez :
```
ANTHROPIC_API_KEY=sk-ant-...votre_clé...
```

### 1.4 Déploiement automatique
Railway détecte automatiquement les fichiers `Procfile`, `requirements.txt` et `railway.json`.
Le déploiement démarre automatiquement ! 🎉

### 1.5 Récupérer l'URL du backend
Une fois déployé, Railway vous donne une URL comme :
```
https://votre-projet.railway.app
```

**⚠️ COPIEZ CETTE URL** - vous en aurez besoin pour l'étape 2

---

## 🎨 ÉTAPE 2 : Déployer le frontend sur Vercel

### 2.1 Mettre à jour l'URL de l'API
Dans `index_ai_chat.html`, remplacez :
```javascript
const API_URL = 'http://localhost:5001/chat';
```
par :
```javascript
const API_URL = 'https://votre-projet.railway.app/chat';
```

### 2.2 Déployer sur Vercel
Vous connaissez déjà Vercel ! Déployez simplement les fichiers HTML :
- `index.html`
- `index_ai_chat.html`
- `notions_interactive.html`
- `ontologie_interactive.html`

---

## ✅ ÉTAPE 3 : Tester

1. Ouvrez votre site Vercel : `https://votre-site.vercel.app/index_ai_chat.html`
2. Cliquez sur le bouton de chat 🤖
3. Posez une question philosophique !

---

## 🔍 Vérifications

### Backend (Railway)
Testez l'API avec curl :
```bash
curl https://votre-projet.railway.app/health
```
Doit retourner : `{"status":"ok"}`

### Frontend (Vercel)
Ouvrez la console du navigateur (F12) et vérifiez qu'il n'y a pas d'erreur CORS.

---

## 💰 Coûts

- **Railway** : Gratuit jusqu'à $5 de crédit/mois (largement suffisant)
- **Vercel** : Gratuit (vous êtes déjà dans les limites)
- **Claude API** : ~$0.003 par question/réponse

---

## 🆘 Aide rapide

### Erreur CORS
Vérifiez que `chat_backend.py` a bien la config CORS avec `*.vercel.app`

### API Claude ne répond pas
Vérifiez que `ANTHROPIC_API_KEY` est bien configurée dans Railway (Variables)

### Frontend ne se connecte pas
Vérifiez l'URL de l'API dans `index_ai_chat.html` (doit pointer vers Railway)

---

## 📝 Fichiers créés pour Railway
- ✅ `Procfile` - Commande de démarrage
- ✅ `railway.json` - Configuration Railway
- ✅ `runtime.txt` - Version Python
- ✅ `requirements.txt` - Dépendances (avec gunicorn)
- ✅ `chat_backend.py` - CORS configuré pour Vercel
