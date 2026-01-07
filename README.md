# Représentation graphique d'une ontologie

Ce script Python lit un fichier CSV contenant une ontologie et génère une visualisation graphique sous forme de graphe.

## Prérequis

- Python 3.x
- Graphviz installé (pour convertir le .dot en PNG)

## Configuration

1. Créez un fichier `ontologie.csv` dans le même dossier, avec les colonnes :
   - `id` : identifiant unique de l'entité.
   - `label` : nom de l'entité.
   - `connections` : IDs des entités connectées, séparés par `;` (ex: 2;3).

Exemple de `ontologie.csv` :
```
id,label,connections
1,Concept A,2;3
2,Concept B,3
3,Concept C,
```

## Exécution

Exécutez le script :
```bash
python main.py
```

Cela génère `ontologie_graph.dot`. Pour l'image PNG :
```bash
dot -Tpng ontologie_graph.dot -o ontologie_graph.png
```

## Exécution

Exécutez le script avec :

```bash
python main.py
```

Ou si vous utilisez un environnement virtuel :

```bash
source .venv/bin/activate
python main.py
```

Le graphe s'affichera dans une fenêtre Matplotlib.

## Notes

- Assurez-vous que votre base Airtable est accessible via l'API.
- Si la structure diffère, modifiez le code en conséquence.