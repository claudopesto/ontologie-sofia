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

# Palette de couleurs par catégorie
CATEGORY_COLORS = {
    'Existence': '#7c81fd',
    'Politique': '#080d94',
    'Cognitif': '#eea5b2',
    'Morale': '#f878cd',
    'Sciences': '#e2a9f1'
}

# Première passe : créer un mapping label → id et construire les nœuds
label_to_id = {}
nodes = []

for i, concept in enumerate(concepts):
    concept_id = concept.get('id', '').strip() or str(i + 1)
    label = concept.get('label', '').strip()
    definition = concept.get('definition', '').strip()
    categorie = concept.get('categorie ', '').strip() or 'Autre'
    
    # Couleur selon la catégorie
    color = CATEGORY_COLORS.get(categorie, '#97C2FC')
    
    # Couleur de police (blanc pour Politique et Sciences)
    font_color = 'white' if categorie in ['Politique', 'Sciences'] else '#333'
    
    if not label:  # Skip empty rows
        continue
    
    # Enregistrer le mapping
    label_to_id[label] = concept_id
    
    # Créer le nœud
    node = {
        "id": concept_id,
        "label": label,
        "title": f"{definition}\n\nCatégorie: {categorie}",
        "color": color,
        "group": categorie,
        "font": {"color": font_color}
    }
    nodes.append(node)

# Deuxième passe : créer les arêtes avec les IDs corrects
edges = []
for i, concept in enumerate(concepts):
    concept_id = concept.get('id', '').strip() or str(i + 1)
    label = concept.get('label', '').strip()
    
    if not label:
        continue
    
    # Créer les arêtes (relations) - colonne relations_to
    relations_str = concept.get('relations_to', '').strip()
    if not relations_str:
        # Fallback: essayer la dernière colonne sans nom
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

# Sauvegarder les données dans graph_data.json
graph_data = {
    "nodes": nodes,
    "edges": edges
}

with open('graph_data.json', 'w', encoding='utf-8') as f:
    json.dump(graph_data, f, ensure_ascii=False, indent=2)

print(f"✅ Fichier sauvegardé : graph_data.json")

# Lire le template HTML
with open('index_ai_chat.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# Remplacer la section de chargement dynamique par des données statiques
nodes_json = json.dumps(nodes, ensure_ascii=False, indent=12)
edges_json = json.dumps(edges, ensure_ascii=False, indent=12)

# Trouver et remplacer la section
marker = "        var nodes = new vis.DataSet("

# Remplacer les DataSets
if marker in html_content:
    # Trouver le début des nodes
    start_idx = html_content.find(marker)
    
    # Trouver la fin du DataSet des edges
    edges_start = html_content.find("var edges = new vis.DataSet(", start_idx)
    if edges_start == -1:
        print("❌ Erreur: var edges non trouvé")
    else:
        # Trouver la fin des edges (chercher ]);)
        edges_end = html_content.find(");", edges_start) + 2
        
        # Construire le nouveau contenu
        before = html_content[:start_idx]
        after = html_content[edges_end:]
        
        new_data_section = f"""        // Network data - chargé depuis Google Sheets
        var nodes = new vis.DataSet({nodes_json});
        var edges = new vis.DataSet({edges_json})"""
        
        html_content = before + new_data_section + after
        print("✅ Données remplacées dans le HTML")
else:
    print("❌ Erreur: marker var nodes non trouvé")

# Sauvegarder
with open('index_ai_chat.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"✅ Fichier mis à jour : index_ai_chat.html")
print(f"📊 {len(nodes)} concepts et {len(edges)} relations intégrés")
