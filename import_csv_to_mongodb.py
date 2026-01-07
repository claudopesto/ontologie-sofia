#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour importer le CSV existant dans MongoDB
"""

import pandas as pd
from pymongo import MongoClient
import certifi

def import_csv_to_mongodb(csv_path, connection_string, database_name, collection_name):
    """
    Importe un fichier CSV dans MongoDB
    
    Args:
        csv_path: Chemin vers le fichier CSV
        connection_string: URL de connexion MongoDB
        database_name: Nom de la base de données
        collection_name: Nom de la collection
    """
    try:
        # Lecture du CSV
        print(f"📖 Lecture du fichier CSV : {csv_path}")
        df = pd.read_csv(csv_path, encoding='utf-8')
        
        print(f"✅ {len(df)} lignes trouvées")
        print(f"📊 Colonnes : {', '.join(df.columns.tolist())}\n")
        
        # Connexion à MongoDB
        print("📡 Connexion à MongoDB...")
        client = MongoClient(connection_string, tlsCAFile=certifi.where())
        db = client[database_name]
        collection = db[collection_name]
        
        # Suppression des données existantes (optionnel)
        existing_count = collection.count_documents({})
        if existing_count > 0:
            print(f"⚠️  {existing_count} documents existants trouvés")
            response = input("Voulez-vous les supprimer et tout réimporter ? (o/n) : ")
            if response.lower() == 'o':
                collection.delete_many({})
                print("🗑️  Données existantes supprimées")
        
        # Conversion du DataFrame en liste de dictionnaires
        records = df.to_dict('records')
        
        # Insertion dans MongoDB
        print("📥 Import des données dans MongoDB...")
        result = collection.insert_many(records)
        
        print(f"✅ {len(result.inserted_ids)} concepts importés avec succès !")
        
        # Affichage d'un exemple
        print("\n📋 Exemple de document importé :")
        sample = collection.find_one()
        if sample:
            for key, value in sample.items():
                if key != '_id':
                    print(f"  • {key}: {value}")
        
        client.close()
        return True
        
    except FileNotFoundError:
        print(f"❌ Fichier non trouvé : {csv_path}")
        return False
    except Exception as e:
        print(f"❌ Erreur : {e}")
        return False

if __name__ == "__main__":
    # Configuration
    CSV_PATH = '/Users/elsa/Downloads/Concepts-Grid view (3).csv'
    
    # Option 1 : MongoDB local
    # CONNECTION_STRING = "mongodb://localhost:27017/"
    
    # Option 2 : MongoDB Atlas (gratuit)
    CONNECTION_STRING = "mongodb+srv://enovelli_db_user:iF3VNRTtH969Il9K@test-ontology.mnf8vlo.mongodb.net/?appName=Test-Ontology"
    
    DATABASE_NAME = "ontologie_sofia"
    COLLECTION_NAME = "concepts"
    
    print("🚀 Import du CSV vers MongoDB\n")
    print(f"📂 Fichier source : {CSV_PATH}")
    print(f"🗄️  Base de données : {DATABASE_NAME}")
    print(f"📦 Collection : {COLLECTION_NAME}\n")
    
    success = import_csv_to_mongodb(
        CSV_PATH, 
        CONNECTION_STRING, 
        DATABASE_NAME, 
        COLLECTION_NAME
    )
    
    if success:
        print("\n🎉 Import terminé !")
        print("\n💡 Prochaines étapes :")
        print("1. Modifiez vos données directement dans MongoDB (via Compass ou Atlas)")
        print("2. Lancez : python sync_from_mongodb.py")
        print("3. Votre visualisation sera mise à jour automatiquement !")
    else:
        print("\n❌ L'import a échoué")
