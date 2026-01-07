#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour synchroniser les notions depuis MongoDB et générer la visualisation
"""

import os
import pandas as pd
from pymongo import MongoClient
import certifi
import subprocess

def sync_notions_from_mongodb():
    """
    Récupère les notions depuis MongoDB et génère le fichier CSV
    puis appelle le script de génération du graphique
    """
    try:
        # Connexion à MongoDB
        connection_string = os.environ.get('MONGODB_URI', 
            'mongodb+srv://enovelli_db_user:iF3VNRTtH969Il9K@test-ontology.mnf8vlo.mongodb.net/?appName=Test-Ontology')
        
        print("🔄 Connexion à MongoDB...")
        client = MongoClient(connection_string, tlsCAFile=certifi.where())
        db = client['ontologie_sofia']
        collection = db['notions']
        
        # Récupération des données
        print("📥 Récupération des notions...")
        documents = list(collection.find({}, {'_id': 0, 'label': 1, 'type': 1, 'connections': 1}))
        
        if not documents:
            print("❌ Aucune notion trouvée dans MongoDB")
            return
        
        print(f"✅ {len(documents)} notions récupérées")
        
        # Conversion en DataFrame
        df = pd.DataFrame(documents)
        
        # Sauvegarde dans ontologie.csv
        csv_path = 'ontologie.csv'
        df.to_csv(csv_path, index=False, encoding='utf-8')
        print(f"💾 Fichier '{csv_path}' créé avec {len(df)} notions")
        
        # Fermeture de la connexion
        client.close()
        
        # Génération du graphique interactif
        print("\n🎨 Génération du graphique interactif...")
        result = subprocess.run(['python', 'interactive_graph_notions.py'], 
                              capture_output=True, 
                              text=True)
        
        if result.returncode == 0:
            print("✅ Graphique interactif généré avec succès !")
            print(result.stdout)
        else:
            print("❌ Erreur lors de la génération du graphique :")
            print(result.stderr)
        
    except Exception as e:
        print(f"❌ Erreur : {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("=" * 60)
    print("🔄 SYNCHRONISATION DES NOTIONS DEPUIS MONGODB")
    print("=" * 60)
    print()
    
    sync_notions_from_mongodb()
    
    print()
    print("=" * 60)
    print("✨ Synchronisation terminée !")
    print("=" * 60)
