import pandas as pd

# Chemin vers le fichier CSV
csv_file = '/Users/elsa/Downloads/Concepts-Grid view.csv'

# Lire le fichier CSV
df = pd.read_csv(csv_file)

# Créer le contenu du fichier .dot
dot_content = 'digraph Ontologie {\n'

# Ensemble pour suivre tous les nœuds
nodes = set()

# Ajouter les nœuds et les arêtes
for index, row in df.iterrows():
    label = row['label']
    connections = row['connections']
    
    # Ajouter le nœud principal
    nodes.add(label)
    
    # Si connections n'est pas vide, ajouter les arêtes
    if pd.notna(connections):
        # Supprimer les espaces et diviser par virgule
        connected_nodes = [conn.strip() for conn in connections.split(',')]
        for conn in connected_nodes:
            nodes.add(conn)
            dot_content += f'    "{label}" -> "{conn}";\n'

# Ajouter tous les nœuds isolés
for node in nodes:
    dot_content += f'    "{node}";\n'

dot_content += '}\n'

# Écrire dans le fichier .dot
with open('ontologie_graph.dot', 'w') as f:
    f.write(dot_content)

print("Fichier ontologie_graph.dot généré avec succès.")