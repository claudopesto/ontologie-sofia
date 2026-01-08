#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

# Charger les données
with open('graph_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Lire le fichier HTML
with open('index_ai_chat.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Convertir en JSON avec indentation
nodes_json = json.dumps(data['nodes'], ensure_ascii=False, indent=12)
edges_json = json.dumps(data['edges'], ensure_ascii=False, indent=12)

# Chercher les marqueurs
start_marker = "// Network data - chargé depuis Google Sheets"
nodes_start = html.find(start_marker)

if nodes_start != -1:
    # Trouver la fin des edges
    edges_marker = "var edges = new vis.DataSet(["
    edges_start = html.find(edges_marker, nodes_start)
    
    if edges_start != -1:
        # Trouver la fin du DataSet des edges (chercher ]);)
        edges_end = html.find("]);", edges_start) + 3
        
        # Construire le nouveau contenu
        before = html[:nodes_start]
        after = html[edges_end:]
        
        new_section = f'''{start_marker}
        var nodes = new vis.DataSet({nodes_json});
        var edges = new vis.DataSet({edges_json})'''
        
        html_new = before + new_section + after
        
        with open('index_ai_chat.html', 'w', encoding='utf-8') as f:
            f.write(html_new)
        print(f"✅ Données mises à jour dans index_ai_chat.html")
        print(f"📊 {len(data['nodes'])} concepts et {len(data['edges'])} relations")
    else:
        print("❌ Marqueur edges non trouvé")
else:
    print("❌ Marqueur de début non trouvé")
