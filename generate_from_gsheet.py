#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour générer une version statique de index_ai_chat.html
avec les données Google Sheets intégrées directement
"""

import requests
import csv
import json
from io import StringIO

# ID de votre Google Sheet
SHEET_ID = "1iIjx0cpG_inITgsoxR8hSSRDMt2uZMYlyD4KEhZSpiY"
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

# Récupérer les données depuis Google Sheets
response = requests.get(CSV_URL, allow_redirects=True)
response.encoding = 'utf-8'
csv_content = response.text

# Parser le CSV
reader = csv.DictReader(StringIO(csv_content))
concepts = list(reader)

# Palette de couleurs pour les concepts
COLORS = [
    '#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8',
    '#F7DC6F', '#BB8FCE', '#85C1E2', '#F8B739', '#52B788',
    '#E07A5F', '#81B29A', '#F2CC8F', '#D4A5A5', '#9D84B7'
]

# Première passe : créer un mapping label → id et construire les nœuds
label_to_id = {}
nodes = []

for i, concept in enumerate(concepts):
    concept_id = concept.get('id', '').strip() or str(i + 1)
    label = concept.get('label', '').strip()
    definition = concept.get('definition', '').strip()
    color = concept.get('color', '').strip() or COLORS[i % len(COLORS)]
    
    if not label:  # Skip empty rows
        continue
    
    # Enregistrer le mapping
    label_to_id[label] = concept_id
    
    # Créer le nœud
    node = {
        "id": concept_id,
        "label": label,
        "title": definition,
        "color": color
    }
    nodes.append(node)

# Deuxième passe : créer les arêtes avec les IDs corrects
edges = []
for i, concept in enumerate(concepts):
    concept_id = concept.get('id', '').strip() or str(i + 1)
    label = concept.get('label', '').strip()
    
    if not label:
        continue
    
    # Créer les arêtes (relations) - dernière colonne sans nom
    relations_str = concept.get('', '').strip()
    if relations_str:
        # Relations séparées par virgules
        related_concepts = [r.strip() for r in relations_str.split(',')]
        for related_label in related_concepts:
            if related_label and related_label in label_to_id:
                edge = {
                    "from": concept_id,
                    "to": label_to_id[related_label]
                }
                edges.append(edge)

print(f"📊 {len(nodes)} concepts trouvés")
print(f"🔗 {len(edges)} relations trouvées")

# Lire le template HTML
with open('index_ai_chat.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# Remplacer la section de chargement dynamique par des données statiques
nodes_json = json.dumps(nodes, ensure_ascii=False, indent=12)
edges_json = json.dumps(edges, ensure_ascii=False, indent=12)

# Trouver et remplacer la section
old_section = """        // Network data - chargé depuis MongoDB
        var nodes = new vis.DataSet("""

new_section = f"""        // Network data - chargé depuis Google Sheets
        var nodes = new vis.DataSet("""

# Remplacer les DataSets
if old_section in html_content:
    # Trouver la fin des DataSets
    start_idx = html_content.find(old_section)
    edges_start = html_content.find("var edges = new vis.DataSet(", start_idx)
    edges_end = html_content.find(");", edges_start) + 2
    
    # Construire le nouveau contenu
    before = html_content[:start_idx]
    after = html_content[edges_end:]
    
    new_data_section = f"""        // Network data - chargé depuis Google Sheets
        var nodes = new vis.DataSet({nodes_json});
        var edges = new vis.DataSet({edges_json})"""
    
    html_content = before + new_data_section + after
else:
    print("⚠️  Section à remplacer non trouvée, création manuelle...")

# Sauvegarder
with open('index_ai_chat.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"✅ Fichier mis à jour : index_ai_chat.html")
print(f"📊 {len(nodes)} concepts et {len(edges)} relations intégrés")
