#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour générer une version statique de index_ai_chat.html
avec les données MongoDB intégrées directement
"""

from pymongo import MongoClient
from dotenv import load_dotenv
import os
import json

load_dotenv()

# Connexion à MongoDB
mongodb_uri = os.environ.get("MONGODB_URI")
if 'tlsAllowInvalidCertificates' not in mongodb_uri:
    separator = '&' if '?' in mongodb_uri else '?'
    mongodb_uri = f"{mongodb_uri}{separator}tlsAllowInvalidCertificates=true"

client = MongoClient(mongodb_uri)
db = client['ontologie_sofia']
concepts_collection = db['concepts']

# Récupérer tous les concepts
concepts = list(concepts_collection.find())

# Convertir en format vis.js
nodes = []
edges = []

for concept in concepts:
    # Créer le nœud
    node = {
        "id": concept.get('id'),
        "label": concept.get('label', concept.get('nom', '')),
        "title": concept.get('definition', ''),
        "color": concept.get('color', '#97C2FC')
    }
    nodes.append(node)
    
    # Créer les arêtes (relations)
    relations = concept.get('relations', [])
    for relation in relations:
        if isinstance(relation, dict):
            edge = {
                "from": concept.get('id'),
                "to": relation.get('to'),
                "label": relation.get('label', '')
            }
            edges.append(edge)

# Lire le template HTML
with open('index_ai_chat.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# Remplacer la section de chargement dynamique par des données statiques
nodes_json = json.dumps(nodes, ensure_ascii=False, indent=12)
edges_json = json.dumps(edges, ensure_ascii=False, indent=12)

# Trouver et remplacer la section
old_section = """        // Network data - sera chargé dynamiquement depuis MongoDB
        var nodes = new vis.DataSet([]);
        var edges = new vis.DataSet([]);"""

new_section = f"""        // Network data - chargé depuis MongoDB
        var nodes = new vis.DataSet({nodes_json});
        var edges = new vis.DataSet({edges_json});"""

html_content = html_content.replace(old_section, new_section)

# Commenter la fonction de chargement dynamique
html_content = html_content.replace(
    "// Charger les données au démarrage de la page\n        loadConceptsFromAPI();",
    "// Données déjà chargées statiquement depuis MongoDB\n        // loadConceptsFromAPI();"
)

# Sauvegarder
with open('index_ai_chat_static.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"✅ Fichier généré : index_ai_chat_static.html")
print(f"📊 {len(nodes)} concepts et {len(edges)} relations intégrés")
