# 🤖 Sofia AI Chat - Guide d'installation

## Configuration complète du chat IA avec Claude

### 1. Installation des dépendances

```bash
pip install flask flask-cors anthropic python-dotenv
```

Ou utilisez le fichier requirements.txt :
```bash
pip install -r requirements.txt
```

### 2. Obtenir une clé API Anthropic

1. Créez un compte sur https://console.anthropic.com/
2. Générez une clé API dans les paramètres
3. Copiez la clé (commence par `sk-ant-...`)

### 3. Configuration de la clé API

Créez un fichier `.env` dans le dossier du projet :

```bash
ANTHROPIC_API_KEY=sk-ant-votre-clé-ici
```

⚠️ **Important** : Ne partagez jamais votre clé API publiquement !

### 4. Lancer le backend

```bash
python chat_backend.py
```

Le serveur démarre sur `http://localhost:5000`

### 5. Ouvrir l'interface

Ouvrez `index_ai_chat.html` dans votre navigateur.

### 6. Tester le chat

- Cliquez sur le bouton 🤖 en bas à gauche
- Posez des questions comme :
  - "Qu'est-ce que la liberté ?"
  - "Explique-moi le concept d'aliénation"
  - "Quelle est la différence entre morale et éthique ?"

## Architecture

```
Frontend (index_ai_chat.html)
    ↓ HTTP POST
Backend (chat_backend.py - Flask)
    ↓ API Call
Anthropic Claude API
    ↓ Response
Backend → Frontend → Utilisateur
```

## Fonctionnalités

✅ Interface chat moderne et responsive
✅ IA Claude 3.5 Sonnet pour des réponses intelligentes
✅ Historique de conversation
✅ Indicateur de frappe
✅ Connaissance des concepts philosophiques
✅ Design cohérent avec le graphe

## Dépannage

**Erreur : "Impossible de se connecter au serveur"**
→ Vérifiez que `python chat_backend.py` est lancé

**Erreur : "ANTHROPIC_API_KEY n'est pas configurée"**
→ Créez le fichier `.env` avec votre clé API

**Erreur CORS**
→ Le backend Flask a déjà CORS activé, mais vérifiez que vous utilisez `http://localhost` et non `file://`

## Alternatives moins chères

Si vous préférez une solution sans coût :
- Remplacez Anthropic par l'API OpenAI (GPT-3.5-turbo moins cher)
- Utilisez un modèle open source local (Ollama + Llama 3)
- Gardez la version simple sans IA (index_with_chat.html)

## Coûts estimés (Anthropic Claude)

- Claude 3.5 Sonnet : ~$3 par million de tokens
- Une conversation typique : ~1000 tokens = $0.003
- 100 conversations : ~$0.30

C'est très abordable pour un usage personnel !
