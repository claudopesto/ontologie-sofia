#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de synchronisation entre MongoDB et la visualisation ontologique
"""

import pandas as pd
from pymongo import MongoClient
import subprocess
import os
import certifi

def sync_from_mongodb(connection_string, database_name, collection_name):
    """
    Synchronise les données depuis MongoDB et régénère la visualisation
    
    Args:
        connection_string: URL de connexion MongoDB (ex: "mongodb://localhost:27017/")
        database_name: Nom de la base de données
        collection_name: Nom de la collection contenant les concepts
    """
    try:
        # Connexion à MongoDB
        print("📡 Connexion à MongoDB...")
        
        # Configuration SSL pour compatibilité GitHub Actions
        tls_params = {}
        if os.environ.get('GITHUB_ACTIONS'):
            # Sur GitHub Actions, utiliser les certificats système
            tls_params = {
                'tls': True,
                'tlsAllowInvalidCertificates': False
            }
        else:
            # En local, utiliser certifi
            tls_params = {'tlsCAFile': certifi.where()}
        
        client = MongoClient(connection_string, **tls_params)
        db = client[database_name]
        collection = db[collection_name]
        
        # Récupération des données
        print("📥 Récupération des données...")
        concepts = list(collection.find())
        
        if not concepts:
            print("⚠️  Aucune donnée trouvée dans la collection")
            return False
        
        # Conversion en DataFrame
        df = pd.DataFrame(concepts)
        
        # Suppression de l'_id de MongoDB si présent
        if '_id' in df.columns:
            df = df.drop('_id', axis=1)
        
        # Vérification des colonnes requises
        required_columns = ['label', 'type', 'connections', 'catégorie']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            print(f"❌ Colonnes manquantes : {', '.join(missing_columns)}")
            return False
        
        # Sauvegarde du CSV
        csv_path = 'ontologie.csv'  # Chemin relatif pour GitHub Actions
        df.to_csv(csv_path, index=False, encoding='utf-8')
        print(f"✅ CSV sauvegardé : {csv_path}")
        
        # Régénération de la visualisation
        print("🔄 Régénération de la visualisation HTML...")
        result = subprocess.run(['python', 'interactive_graph.py'], 
                              capture_output=True, 
                              text=True)
        
        if result.returncode == 0:
            print("✅ Visualisation mise à jour avec succès !")
            return True
        else:
            print(f"❌ Erreur lors de la régénération : {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur : {e}")
        return False
    finally:
        if 'client' in locals():
            client.close()

def insert_sample_data(connection_string, database_name, collection_name):
    """
    Insère des données d'exemple dans MongoDB (pour tester)
    """
    try:
        client = MongoClient(connection_string)
        db = client[database_name]
        collection = db[collection_name]
        
        # Données d'exemple
        sample_concepts = [
            {
                "label": "Liberté",
                "type": "État d'un individu qui n'est soumis qu'aux obligations qu'il se choisit",
                "connections": "Émancipation, Aliénation",
                "catégorie": "individu"
            },
            {
                "label": "Conscience",
                "type": "Aucune info",
                "connections": "Inconscient",
                "catégorie": "cognitif"
            }
        ]
        
        collection.insert_many(sample_concepts)
        print(f"✅ {len(sample_concepts)} concepts d'exemple insérés")
        client.close()
        return True
        
    except Exception as e:
        print(f"❌ Erreur : {e}")
        return False

if __name__ == "__main__":
    # Configuration MongoDB
    # Utiliser la variable d'environnement si disponible (GitHub Actions)
    # Sinon utiliser la valeur par défaut (local)
    CONNECTION_STRING = os.environ.get(
        'MONGODB_URI',
        "mongodb+srv://enovelli_db_user:iF3VNRTtH969Il9K@test-ontology.mnf8vlo.mongodb.net/?appName=Test-Ontology"
    )
    
    DATABASE_NAME = "ontologie_sofia"
    COLLECTION_NAME = "concepts"
    
    print("🚀 Démarrage de la synchronisation MongoDB\n")
    
    # Pour insérer des données d'exemple (décommentez si besoin) :
    # insert_sample_data(CONNECTION_STRING, DATABASE_NAME, COLLECTION_NAME)
    
    # Synchronisation
    success = sync_from_mongodb(CONNECTION_STRING, DATABASE_NAME, COLLECTION_NAME)
    
    if success:
        print("\n🎉 Synchronisation terminée avec succès !")
    else:
        print("\n❌ La synchronisation a échoué")
