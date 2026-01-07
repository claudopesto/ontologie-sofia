# 🚀 Comment lancer Sofia AI Chat

## Étape 1 : Ouvrir 2 terminaux

### Terminal 1 - Backend API
```bash
cd "/Users/elsa/Library/Mobile Documents/com~apple~CloudDocs/Causeries/Sofia/Ontologie"
source .venv/bin/activate
python chat_backend.py
```
Laissez ce terminal ouvert.

### Terminal 2 - Serveur Web
```bash
cd "/Users/elsa/Library/Mobile Documents/com~apple~CloudDocs/Causeries/Sofia/Ontologie"
python -m http.server 8000
```
Laissez ce terminal ouvert.

## Étape 2 : Ouvrir le navigateur

Allez à : **http://localhost:8000/index_ai_chat.html**

Cliquez sur 🤖 et chattez !

## ⚠️ Important
- Les DEUX terminaux doivent rester ouverts
- Ne fermez pas les terminaux pendant l'utilisation
- Pour arrêter : Ctrl+C dans chaque terminal
