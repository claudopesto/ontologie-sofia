#!/usr/bin/env python3
"""
Script de déploiement automatique
Synchronise depuis MongoDB, génère le HTML et le déploie sur GitHub
"""

import subprocess
import shutil
import os

def run_command(command, description):
    """Exécute une commande et affiche le résultat"""
    print(f"\n🔄 {description}...")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ Erreur : {result.stderr}")
        return False
    print(f"✅ {description} terminé")
    return True

def main():
    print("=" * 50)
    print("🚀 DÉPLOIEMENT AUTOMATIQUE DE L'ONTOLOGIE")
    print("=" * 50)
    
    # 1. Synchroniser depuis MongoDB
    if not run_command("python sync_from_mongodb.py", "Synchronisation depuis MongoDB"):
        return
    
    # 2. Copier ontologie_interactive.html vers index.html
    print("\n🔄 Copie vers index.html...")
    try:
        shutil.copy2("ontologie_interactive.html", "index.html")
        print("✅ Fichier index.html créé")
    except Exception as e:
        print(f"❌ Erreur lors de la copie : {e}")
        return
    
    # 3. Git add, commit et push (si git est configuré)
    if os.path.exists(".git"):
        print("\n📤 Déploiement sur GitHub...")
        
        # Ajouter les fichiers
        run_command("git add index.html sofia_logo.png", "Ajout des fichiers")
        
        # Commit
        run_command('git commit -m "🤖 Mise à jour automatique depuis MongoDB"', "Commit")
        
        # Push
        if run_command("git push origin main", "Push vers GitHub"):
            print("\n" + "=" * 50)
            print("🎉 DÉPLOIEMENT RÉUSSI !")
            print("Attendez 2-3 minutes pour voir les changements en ligne")
            print("=" * 50)
    else:
        print("\n⚠️  Git n'est pas configuré. Le fichier index.html a été créé.")
        print("📋 Copiez manuellement le contenu dans GitHub, ou configurez git avec :")
        print("   git init")
        print("   git remote add origin https://github.com/VOTRE_USERNAME/VOTRE_REPO.git")

if __name__ == "__main__":
    main()
