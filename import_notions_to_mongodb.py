#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour importer le fichier "Notions pour penser-Grid view.csv" dans MongoDB
en gardant uniquement les colonnes 'label', 'type' et 'connections'
"""

import pandas as pd
from pymongo import MongoClient
import certifi
import os

def import_notions_to_mongodb(csv_path):
    """
    Importe le fichier CSV des notions dans MongoDB
    en ne conservant que les colonnes label, type et connections
    
    Args:
        csv_path: Chemin vers le fichier CSV
    """
    try:
        # Lecture du CSV
        print(f"📖 Lecture du fichier CSV : {csv_path}")
        df = pd.read_csv(csv_path, encoding='utf-8')
        
        print(f"✅ {len(df)} lignes trouvées")
        print(f"📊 Colonnes disponibles : {', '.join(df.columns.tolist())}\n")
        
        # Sélection uniquement des colonnes souhaitées
        columns_to_keep = ['label', 'type', 'connections']
        
        # Vérification que les colonnes existent
        missing_columns = [col for col in columns_to_keep if col not in df.columns]
        if missing_columns:
            print(f"❌ Colonnes manquantes : {', '.join(missing_columns)}")
            return
        
        # Filtrage des colonnes
        df_filtered = df[columns_to_keep].copy()
        
        # Remplacement des valeurs NaN par des chaînes vides
        df_filtered = df_filtered.fillna('')
        
        print(f"📋 Colonnes sélectionnées : {', '.join(columns_to_keep)}")
        print(f"📊 Aperçu des données :")
        print(df_filtered.head())
        print()
        
        # Connexion à MongoDB
        connection_string = os.environ.get('MONGODB_URI', 
            'mongodb+srv://enovelli_db_user:iF3VNRTtH969Il9K@test-ontology.mnf8vlo.mongodb.net/?appName=Test-Ontology')
        
        print("📡 Connexion à MongoDB...")
        client = MongoClient(connection_string, tlsCAFile=certifi.where())
        db = client['ontologie_sofia']
        collection = db['notions']
        
        # Suppression des données existantes
        existing_count = collection.count_documents({})
        if existing_count > 0:
            print(f"⚠️  {existing_count} documents existants trouvés dans la collection 'notions'")
            response = input("Voulez-vous les supprimer et tout réimporter ? (o/n) : ")
            if response.lower() == 'o':
                collection.delete_many({})
                print("🗑️  Données existantes supprimées")
            else:
                print("❌ Import annulé")
                return
        
        # Conversion du DataFrame en liste de dictionnaires
        records = df_filtered.to_dict('records')
        
        # Insertion dans MongoDB
        print("📥 Import des données dans MongoDB...")
        result = collection.insert_many(records)
        
        print(f"✅ {len(result.inserted_ids)} concepts importés avec succès !")
        print(f"📊 Collection : ontologie_sofia.notions")
        print(f"🔗 Base de données : ontologie_sofia")
        
        # Affichage de quelques exemples
        print("\n📝 Exemples de documents importés :")
        for doc in collection.find().limit(3):
            print(f"  - {doc['label']}: {doc['type'][:50]}...")
        
        client.close()
        print("\n🎉 Import terminé !")
        
    except FileNotFoundError:
        print(f"❌ Fichier non trouvé : {csv_path}")
    except Exception as e:
        print(f"❌ Erreur : {e}")

if __name__ == "__main__":
    # Chemin vers le fichier CSV
    csv_file = "/Users/elsa/Downloads/Notions pour penser-Grid view.csv"
    
    import_notions_to_mongodb(csv_file)
