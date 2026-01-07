#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Génère une visualisation interactive des notions philosophiques avec vis.js
"""

import pandas as pd
import json

def generate_interactive_graph(csv_file='ontologie.csv', output_file='notions_interactive.html'):
    """
    Génère un fichier HTML avec une visualisation interactive du réseau de notions
    """
    # Lecture du CSV
    df = pd.read_csv(csv_file, encoding='utf-8')
    
    # Création des nœuds
    nodes = []
    label_to_id = {}
    
    for idx, row in df.iterrows():
        label = str(row['label']).strip()
        type_info = str(row['type']) if pd.notna(row['type']) else 'Aucune info'
        
        label_to_id[label] = idx
        
        nodes.append({
            'id': idx,
            'label': label,
            'title': type_info,
            'color': '#7c81fd',  # Couleur unique pour toutes les notions
            'font': {'color': '#333'}
        })
    
    # Création des liens
    edges = []
    for idx, row in df.iterrows():
        if pd.notna(row['connections']) and str(row['connections']).strip():
            connections = str(row['connections']).split(',')
            source_label = str(row['label']).strip()
            
            if source_label in label_to_id:
                source_id = label_to_id[source_label]
                
                for connection in connections:
                    target_label = connection.strip()
                    if target_label and target_label in label_to_id:
                        target_id = label_to_id[target_label]
                        edges.append({
                            'from': source_id,
                            'to': target_id
                        })
    
    # Génération du HTML
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>Notions pour penser</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <script type="text/javascript" src="https://unpkg.com/vis-network@9.1.2/dist/vis-network.min.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
            overflow: hidden;
        }}
        header {{
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 10px;
            background: #f5f5f5;
            border-bottom: 1px solid #ddd;
        }}
        h1 {{
            font-size: 1.5rem;
            margin: 0;
            font-weight: bold;
        }}
        h2 {{
            font-size: 0.9rem;
            margin: 5px 0 0 0;
            color: #666;
            font-weight: normal;
        }}
        #logo {{
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
        }}
        #network {{
            width: 100%;
            height: calc(100vh - 70px);
        }}
        #popup {{
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
        }}
        #popup-content {{
            font-size: 0.95rem;
            line-height: 1.5;
            margin-bottom: 15px;
        }}
        button {{
            width: 100%;
            padding: 12px;
            background: #007bff;
            color: white;
            border: none;
            border-radius: 5px;
            font-size: 1rem;
            cursor: pointer;
        }}
        button:active {{
            background: #0056b3;
        }}
        #overlay {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.5);
            display: none;
            z-index: 999;
        }}
        @media (min-width: 768px) {{
            header {{
                padding: 15px;
            }}
            h1 {{
                font-size: 2rem;
            }}
            h2 {{
                font-size: 1.1rem;
            }}
            #logo {{
                height: 80px;
                top: 15px;
                right: 15px;
            }}
            #popup {{
                max-width: 500px;
            }}
        }}
    </style>
</head>
<body>
    <img id="logo" src="sofia_logo.png" alt="Sofia Logo">
    <header>
        <div>
            <h1>Notions pour penser</h1>
            <h2>Découvrez les notions philosophiques interactives</h2>
        </div>
    </header>
    <div id="network"></div>
    <div id="overlay" onclick="hidePopup()"></div>
    <div id="popup">
        <p id="popup-content"></p>
        <button onclick="hidePopup()">Fermer</button>
    </div>
    <script type="text/javascript">
        var nodes = new vis.DataSet({json.dumps(nodes, ensure_ascii=False)});
        var edges = new vis.DataSet({json.dumps(edges, ensure_ascii=False)});
        var container = document.getElementById('network');
        var data = {{
            nodes: nodes,
            edges: edges
        }};
        var options = {{
            physics: {{
                enabled: true
            }},
            edges: {{
                width: 1,
                smooth: {{
                    type: 'continuous'
                }}
            }},
            interaction: {{
                hover: true,
                tooltipDelay: 200
            }},
            nodes: {{
                shape: 'circle',
                size: 25,
                font: {{
                    size: 14,
                    color: '#333'
                }},
                borderWidth: 2,
                borderWidthSelected: 3,
                shadow: {{
                    enabled: true,
                    color: 'rgba(0,0,0,0.15)',
                    size: 8,
                    x: 2,
                    y: 2
                }}
            }}
        }};
        var network = new vis.Network(container, data, options);
        function showPopup(content) {{
            document.getElementById('popup-content').innerText = content;
            document.getElementById('overlay').style.display = 'block';
            document.getElementById('popup').style.display = 'block';
        }}
        function hidePopup() {{
            document.getElementById('overlay').style.display = 'none';
            document.getElementById('popup').style.display = 'none';
        }}
        network.on('click', function(properties) {{
            if (properties.nodes.length > 0) {{
                var nodeId = properties.nodes[0];
                var node = nodes.get(nodeId);
                showPopup(node.title);
            }}
        }});
        
        network.on('hoverNode', function(params) {{
            var nodeId = params.node;
            nodes.update({{id: nodeId, font: {{size: 20}}, size: 30}});
        }});
        
        network.on('blurNode', function(params) {{
            var nodeId = params.node;
            nodes.update({{id: nodeId, font: {{size: 14}}, size: 25}});
        }});
    </script>
</body>
</html>"""
    
    # Écriture du fichier HTML
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Fichier HTML généré : {output_file}")
    print(f"📊 {len(nodes)} notions et {len(edges)} connexions")

if __name__ == "__main__":
    generate_interactive_graph()
