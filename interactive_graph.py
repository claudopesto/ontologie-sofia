import pandas as pd
import json

# Chemin vers le fichier CSV
csv_file = 'ontologie.csv'  # Chemin relatif pour GitHub Actions

# Lire le fichier CSV
df = pd.read_csv(csv_file)

# Créer un dictionnaire label -> type pour les infos
label_to_type = {}
label_to_category = {}
category_colors = {
    'individu': '#f878cd',      # Rose vif
    'cognitif': '#7c81fd',      # Bleu violet
    'normes externes': '#080d94', # Bleu marine
}

for index, row in df.iterrows():
    label = row['label']
    type_info = row['type'] if pd.notna(row['type']) else 'Aucune info'
    category = row.get('catégorie', row.get('categorie', 'Autre'))
    if pd.isna(category):
        category = 'Autre'
    else:
        # Si plusieurs catégories, prendre la première
        category = str(category).split(',')[0].strip()
    label_to_type[label] = type_info
    label_to_category[label] = category
    
# Ajouter couleur par défaut pour catégories inconnues
default_color = '#eea5b2'  # Rose poudré

# Dictionnaires pour nœuds et arêtes
nodes = []
edges = []
node_id = 0
node_map = {}

# Ajouter les nœuds et les arêtes
for index, row in df.iterrows():
    label = row['label']
    connections = row['connections']
    
    # Ajouter le nœud si pas déjà présent
    if label not in node_map:
        node_map[label] = node_id
        category = label_to_category.get(label, 'Autre')
        color = category_colors.get(category, default_color)
        # Texte blanc pour le bleu marine foncé
        font_color = 'white' if color == '#080d94' else '#333'
        nodes.append({
            "id": node_id, 
            "label": label, 
            "title": label_to_type.get(label, 'Aucune info'),
            "color": color,
            "font": {"color": font_color}
        })
        node_id += 1
    
    # Si connections n'est pas vide, ajouter les arêtes
    if pd.notna(connections):
        # Supprimer les espaces et diviser par virgule
        connected_nodes = [conn.strip() for conn in connections.split(',')]
        for conn in connected_nodes:
            if conn not in node_map:
                node_map[conn] = node_id
                category = label_to_category.get(conn, 'Autre')
                color = category_colors.get(category, default_color)
                # Texte blanc pour le bleu marine foncé
                font_color = 'white' if color == '#080d94' else '#333'
                nodes.append({
                    "id": node_id, 
                    "label": conn, 
                    "title": label_to_type.get(conn, 'Aucune info'),
                    "color": color,
                    "font": {"color": font_color}
                })
                node_id += 1
            edges.append({"from": node_map[label], "to": node_map[conn]})

# Générer le HTML
html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>La philo c'est la vie</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <script type="text/javascript" src="https://unpkg.com/vis-network@9.1.2/dist/vis-network.min.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
            overflow: hidden;
        }
        header {
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 10px;
            background: #f5f5f5;
            border-bottom: 1px solid #ddd;
        }
        h1 {
            font-size: 1.5rem;
            margin: 0;
            font-weight: bold;
        }
        h2 {
            font-size: 0.9rem;
            margin: 5px 0 0 0;
            color: #666;
            font-weight: normal;
        }
        #logo {
            position: fixed;
            top: 10px;
            right: 10px;
            height: 60px;
            width: auto;
            z-index: 200;
            background: white;
            padding: 5px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.15);
        }
        #network {
            width: 100%;
            height: calc(100vh - 70px);
        }
        #legend {
            position: fixed;
            bottom: 10px;
            right: 10px;
            background: white;
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 10px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.2);
            z-index: 100;
            max-height: 70vh;
            overflow-y: auto;
        }
        #legend h3 {
            font-size: 0.9rem;
            margin-bottom: 8px;
            text-align: center;
        }
        .legend-item {
            display: flex;
            align-items: center;
            margin: 5px 0;
            font-size: 0.85rem;
        }
        .legend-color {
            width: 15px;
            height: 15px;
            border-radius: 50%;
            margin-right: 8px;
            flex-shrink: 0;
        }
        #popup {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: white;
            border: 1px solid black;
            border-radius: 8px;
            padding: 20px;
            display: none;
            z-index: 1000;
            max-width: 90%;
            max-height: 80vh;
            overflow-y: auto;
            word-wrap: break-word;
        }
        #popup-content {
            font-size: 0.95rem;
            line-height: 1.5;
            margin-bottom: 15px;
        }
        button {
            width: 100%;
            padding: 12px;
            background: #007bff;
            color: white;
            border: none;
            border-radius: 5px;
            font-size: 1rem;
            cursor: pointer;
        }
        button:active {
            background: #0056b3;
        }
        #overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.5);
            display: none;
            z-index: 999;
        }
        @media (min-width: 768px) {
            header {
                padding: 15px;
            }
            h1 {
                font-size: 2rem;
            }
            h2 {
                font-size: 1.1rem;
            }
            #logo {
                height: 80px;
                top: 15px;
                right: 15px;
            }
            #popup {
                max-width: 500px;
            }
        }
    </style>
</head>
<body>
    <img id="logo" src="sofia_logo.png" alt="Sofia Logo">
    <header>
        <div>
            <h1>La philo c'est la vie</h1>
            <h2>Découvrez l'ontologie interactive de Sofia</h2>
        </div>
    </header>
    <div id="network"></div>
    <div id="legend">
        <h3>Légende</h3>
        <div class="legend-item"><div class="legend-color" style="background: #f878cd;"></div><span>Individu</span></div>
        <div class="legend-item"><div class="legend-color" style="background: #7c81fd;"></div><span>Cognitif</span></div>
        <div class="legend-item"><div class="legend-color" style="background: #080d94;"></div><span>Normes externes</span></div>
        <div class="legend-item"><div class="legend-color" style="background: #eea5b2;"></div><span>Autre</span></div>
    </div>
    <div id="overlay" onclick="hidePopup()"></div>
    <div id="popup">
        <p id="popup-content"></p>
        <button onclick="hidePopup()">Fermer</button>
    </div>
    <script type="text/javascript">
        var nodes = new vis.DataSet(""" + json.dumps(nodes, ensure_ascii=False) + """);
        var edges = new vis.DataSet(""" + json.dumps(edges) + """);
        var container = document.getElementById('network');
        var data = {
            nodes: nodes,
            edges: edges
        };
        var options = {
            physics: {
                enabled: true
            },
            edges: {
                width: 1,
                smooth: {
                    type: 'continuous'
                }
            },
            interaction: {
                hover: true,
                tooltipDelay: 200
            },
            nodes: {
                shape: 'circle',
                size: 25,
                font: {
                    size: 14,
                    color: '#333'
                },
                borderWidth: 2,
                borderWidthSelected: 3,
                shadow: {
                    enabled: true,
                    color: 'rgba(0,0,0,0.15)',
                    size: 8,
                    x: 2,
                    y: 2
                }
            }
        };
        var network = new vis.Network(container, data, options);
        function showPopup(content) {
            document.getElementById('popup-content').innerText = content;
            document.getElementById('overlay').style.display = 'block';
            document.getElementById('popup').style.display = 'block';
        }
        function hidePopup() {
            document.getElementById('overlay').style.display = 'none';
            document.getElementById('popup').style.display = 'none';
        }
        network.on('click', function(properties) {
            if (properties.nodes.length > 0) {
                var nodeId = properties.nodes[0];
                var node = nodes.get(nodeId);
                showPopup(node.title);
            }
        });
        
        network.on('hoverNode', function(params) {
            var nodeId = params.node;
            nodes.update({id: nodeId, font: {size: 20}, size: 30});
        });
        
        network.on('blurNode', function(params) {
            var nodeId = params.node;
            nodes.update({id: nodeId, font: {size: 14}, size: 25});
        });
    </script>
</body>
</html>"""

# Écrire le fichier HTML
with open('ontologie_interactive.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Fichier ontologie_interactive.html généré avec succès. Ouvrez-le dans un navigateur pour voir le graphe interactif.")