# 🤖 Configuration GitHub Actions pour déploiement automatique

## Ce qui sera automatisé

✅ Synchronisation depuis MongoDB toutes les heures  
✅ Génération automatique du HTML  
✅ Déploiement automatique sur Vercel  
✅ Aucune intervention manuelle nécessaire

## Étapes de configuration

### 1. Créer le dossier sur GitHub

Sur votre dépôt GitHub, créez cette structure :

```
.github/
  workflows/
    deploy.yml
```

### 2. Copier le fichier workflow

Copiez le contenu du fichier `deploy.yml` local dans le fichier sur GitHub.

### 3. Ajouter le secret MongoDB

**Important** : Pour que GitHub Actions puisse se connecter à MongoDB, vous devez ajouter votre connexion string en tant que secret :

1. Allez sur votre dépôt GitHub
2. Cliquez sur **Settings** (Paramètres)
3. Dans le menu de gauche, cliquez sur **Secrets and variables** → **Actions**
4. Cliquez sur **New repository secret**
5. Nom du secret : `MONGODB_URI`
6. Valeur : `mongodb+srv://enovelli_db_user:iF3VNRTtH969Il9K@test-ontology.mnf8vlo.mongodb.net/?appName=Test-Ontology`
7. Cliquez sur **Add secret**

### 4. Uploader les fichiers Python

Assurez-vous que ces fichiers sont sur GitHub :
- ✅ `sync_from_mongodb.py`
- ✅ `interactive_graph.py`
- ✅ `sofia_logo.png`

### 5. Tester le workflow

1. Allez dans l'onglet **Actions** de votre dépôt GitHub
2. Vous verrez le workflow "Synchronisation automatique MongoDB → Vercel"
3. Cliquez sur **Run workflow** pour tester manuellement
4. Attendez 1-2 minutes et vérifiez que ça fonctionne

## Comment ça fonctionne

1. **Automatiquement** : Chaque heure, GitHub Actions :
   - Se connecte à MongoDB
   - Récupère les concepts
   - Génère le HTML
   - Le pousse sur GitHub
   - Vercel détecte le changement et redéploie

2. **Manuellement** : Vous pouvez aussi lancer le workflow à tout moment :
   - Onglet **Actions** → **Run workflow**

## Modifier la fréquence

Dans le fichier `deploy.yml`, ligne `cron:` :

```yaml
# Toutes les heures (défaut)
- cron: '0 * * * *'

# Toutes les 30 minutes
- cron: '*/30 * * * *'

# Toutes les 6 heures
- cron: '0 */6 * * *'

# À 9h et 18h chaque jour
- cron: '0 9,18 * * *'
```

## Workflow complet après configuration

1. **Vous** : Ajoutez un concept dans MongoDB Atlas
2. **GitHub Actions** : Synchronise automatiquement (dans l'heure)
3. **Vercel** : Redéploie automatiquement le site
4. **Résultat** : Le concept apparaît en ligne sans intervention ! 🎉

## Avantages

✅ Zéro intervention manuelle  
✅ Toujours à jour automatiquement  
✅ Historique complet des modifications  
✅ Peut être déclenché manuellement si besoin  
✅ Gratuit (GitHub Actions offre 2000 minutes/mois)

## Besoin d'aide ?

Si vous avez des questions pour la configuration, demandez-moi !
