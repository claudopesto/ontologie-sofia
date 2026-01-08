#!/usr/bin/env python3
import requests, csv, json
from io import StringIO

SHEET_ID = '1iIjx0cpG_inITgsoxR8hSSRDMt2uZMYlyD4KEhZSpiY'
CSV_URL = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv'

response = requests.get(CSV_URL, allow_redirects=True, timeout=10)
response.encoding = 'utf-8'
reader = csv.DictReader(StringIO(response.text))
concepts = list(reader)

nodes = []
edges = []

for i, concept in enumerate(concepts):
    concept_id = concept.get('id', '').strip() or str(i + 1)
    label = concept.get('label', '').strip()
    if label:
        nodes.append({'id': concept_id, 'label': label})
        relations_str = concept.get('', '').strip()
        if relations_str:
            for related in [r.strip() for r in relations_str.split(',')]:
                if related:
                    edges.append({'from': concept_id, 'to': related})

print(f'✅ {len(nodes)} concepts et {len(edges)} relations')
print(json.dumps({'nodes': nodes[:2], 'edges': edges[:3]}, indent=2, ensure_ascii=False))
