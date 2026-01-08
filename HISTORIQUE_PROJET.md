# 📚 Historique du Projet - Ontologie Sofia

## 🎯 Vue d'ensemble
Création d'une plateforme web interactive pour explorer les concepts philosophiques avec visualisation de graphe et chat IA.

---

## 🚀 Étapes du développement

### 1️⃣ **Visualisation de l'ontologie**
- ✅ Graphe interactif avec vis.js pour 34 concepts philosophiques
- ✅ Catégorisation par couleurs (Individu, Cognitif, Normes externes, Autre)
- ✅ Suppression des flèches → lignes fines pour meilleure lisibilité
- ✅ Popups avec définitions au clic sur les nœuds
- ✅ Effets de hover dynamiques

### 2️⃣ **Base de données MongoDB**
- ✅ Connexion à MongoDB Atlas (cloud)
- ✅ Collection `concepts` : 29 concepts philosophiques originaux
- ✅ Collection `notions` : 29 nouvelles notions philosophiques
- ✅ Import automatique depuis CSV
- ✅ Scripts de synchronisation (sync_concepts.py, sync_notions.py)

### 3️⃣ **Chat IA avec Claude**
- ✅ Intégration de Claude 3 Haiku (Anthropic API)
- ✅ Interface de chat moderne avec design gradient violet
- ✅ Contexte philosophique pré-chargé pour Sofia
- ✅ Historique de conversation (10 derniers messages)
- ✅ Indicateur de saisie animé
- ✅ Gestion des erreurs et encodage UTF-8

### 4️⃣ **Architecture cloud**
- ✅ **Backend Flask** déployé sur Railway
  - API REST avec endpoints `/chat` et `/health`
  - Configuration CORS pour Vercel
  - Variables d'environnement sécurisées
  - URL : https://ontologie-production.up.railway.app

- ✅ **Frontend** déployé sur Vercel
  - Interface HTML/CSS/JavaScript responsive
  - URL : https://ontologie-sofia.vercel.app/index_ai_chat.html

- ✅ **Code source** sur GitHub
  - Repository : claudopesto/ontologie-sofia
  - Branche : main
  - Auto-déploiement configuré
  - Fichier .env exclu (.gitignore)

### 5️⃣ **Résolution des problèmes techniques**

#### Clé API Anthropic
- ❌ Première clé invalide → erreurs 404
- ❌ Modèles Claude non disponibles
- ✅ Nouvelle clé générée
- ✅ Modèle `claude-3-haiku-20240307` validé et fonctionnel

#### Encodage et CORS
- ❌ Erreurs d'encodage UTF-8 sur caractères français
- ✅ Configuration `sys.stdout.reconfigure(encoding='utf-8')`
- ❌ Problème CORS avec wildcard `*.vercel.app`
- ✅ URL Vercel explicite ajoutée dans configuration CORS

#### Déploiement
- ❌ Conflit port 5000 local (AirPlay macOS)
- ✅ Migration vers Railway (backend cloud)
- ❌ GitHub Secret Scanning (clé API dans .env)
- ✅ Nettoyage historique Git avec `git filter-branch`
- ✅ Configuration Railway Variables
- ✅ Redéploiements automatiques depuis GitHub

---

## 📁 Structure finale du projet

```
ontologie-sofia/
├── index_ai_chat.html          # Interface principale avec chat IA
├── chat_backend.py             # API Flask pour Claude
├── sync_concepts.py            # Import MongoDB concepts
├── sync_notions.py             # Import MongoDB notions
├── ontologie.csv               # Données concepts
├── sofia_logo.png              # Logo du projet
├── .env                        # Clés API (non versionné)
├── .gitignore                  # Exclusions Git
├── requirements.txt            # Dépendances Python
├── Procfile                    # Configuration Railway
├── railway.json                # Config Railway
├── runtime.txt                 # Version Python
└── README.md                   # Documentation
```

---

## 🛠️ Technologies utilisées

**Frontend**
- HTML5 / CSS3 / JavaScript
- vis.js 9.1.2 (graphe interactif)
- Design responsive avec media queries

**Backend**
- Python 3.11
- Flask 3.1.0 (serveur web)
- Flask-CORS 5.0.0 (gestion CORS)
- Anthropic 0.75.0 (API Claude)
- python-dotenv 1.0.0 (variables d'environnement)
- gunicorn 21.2.0 (serveur WSGI production)
- pymongo (MongoDB)

**Infrastructure**
- Railway (backend API)
- Vercel (frontend statique)
- GitHub (version control)
- MongoDB Atlas (base de données cloud)

---

## 🎨 Fonctionnalités actuelles

✅ Visualisation interactive de 34 concepts philosophiques  
✅ Catégorisation par couleurs et légende  
✅ Chat IA avec Sofia alimenté par Claude  
✅ Réponses philosophiques contextualisées  
✅ Design moderne et responsive  
✅ Déploiement en production  
✅ Architecture scalable  

---

## 🔮 Améliorations futures possibles

- [ ] Connexion du chat à la base MongoDB pour contexte dynamique
- [ ] Authentification utilisateur
- [ ] Sauvegarde des conversations
- [ ] Recherche de concepts
- [ ] Export de graphes en image
- [ ] Mode sombre
- [ ] Multilangue (anglais, espagnol...)
- [ ] Analytics et monitoring
- [ ] Tests automatisés
- [ ] Documentation API

---

## 📊 Métriques du projet

- **Concepts philosophiques** : 34
- **Lignes de code Python** : ~200
- **Lignes de code HTML/CSS/JS** : ~600
- **Commits GitHub** : 15+
- **Temps de développement** : 3 jours
- **Coût mensuel estimé** :
  - Railway : Gratuit (tier Hobby)
  - Vercel : Gratuit
  - MongoDB Atlas : Gratuit (M0)
  - Anthropic API : ~0.25¢ par message (~$5/mois usage modéré)

---

## 🎓 Leçons apprises

1. **GitHub Secret Scanning** protège efficacement contre l'exposition de clés API
2. **Railway redéploie automatiquement** depuis GitHub après chaque push
3. **CORS avec wildcards** ne fonctionne pas toujours → utiliser URLs explicites
4. **Encodage UTF-8** doit être forcé pour Python sur Railway
5. **Cache Vercel** peut nécessiter force-reload (Cmd+Shift+R) pour voir les mises à jour
6. **Modèles IA** évoluent rapidement → vérifier la disponibilité des versions
7. **Variables d'environnement Railway** sont distinctes du fichier .env local

---

## 🏆 Résultat

**Plateforme web fonctionnelle et professionnelle** permettant d'explorer visuellement des concepts philosophiques et de discuter avec une IA spécialisée en philosophie, le tout déployé en production sur une infrastructure cloud moderne.

🌐 **Accès public** : https://ontologie-sofia.vercel.app/index_ai_chat.html

---

*Dernière mise à jour : 8 janvier 2026*
