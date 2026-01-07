import requests
import pydot
import csv

# Pour lire le CSV exporté d'Airtable
def get_entities_from_csv(filename='ontologie.csv'):
    entities = []
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            label = row.get('label', '').strip()
            if not label:
                continue
            connections = [c.strip() for c in row.get('connections', '').split(',') if c.strip()]
            entity = {
                'id': label,  # Utiliser label comme ID unique
                'fields': {
                    'label': label,
                    'connections': connections
                }
            }
            entities.append(entity)
    return entities

entities = get_entities_from_csv()

print(f"Nombre d'entités lues : {len(entities)}")
for e in entities[:3]:  # Afficher les 3 premières
    print(f"ID: {e['id']}, Connections: {e['fields']['connections']}")

# Créer un graphe avec pydot
graph = pydot.Dot(graph_type='digraph')

# Ajouter les nœuds (entités) avec 'label'
for entity in entities:
    entity_id = entity['id']
    fields = entity['fields']
    label = fields.get('label', entity_id)
    node = pydot.Node(entity_id, label=label)
    graph.add_node(node)

# Ajouter les arêtes basées sur 'connections'
for entity in entities:
    entity_id = entity['id']
    fields = entity['fields']
    connections = fields.get('connections', [])
    if isinstance(connections, list):
        for conn_id in connections:
            edge = pydot.Edge(entity_id, conn_id)
            graph.add_edge(edge)

# Générer et sauvegarder le graphe en format DOT
with open('ontologie_graph.dot', 'w') as f:
    f.write(graph.to_string())
print("Graphe sauvegardé dans ontologie_graph.dot")
print("Pour générer l'image PNG, installez Graphviz et exécutez : dot -Tpng ontologie_graph.dot -o ontologie_graph.png")