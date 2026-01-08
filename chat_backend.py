#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Backend API pour le chat Sofia avec intégration d'une IA
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys
from anthropic import Anthropic
from dotenv import load_dotenv
import requests
import csv
from io import StringIO

# Force UTF-8 encoding
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

# Charger le fichier .env
load_dotenv()

app = Flask(__name__)

# Configuration CORS - permissive en développement
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Configuration de l'API Anthropic (Claude)
client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# Configuration Google Sheets
SHEET_ID = "1iIjx0cpG_inITgsoxR8hSSRDMt2uZMYlyD4KEhZSpiY"
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

def load_concepts_from_gsheet():
    """Charge les concepts depuis Google Sheets"""
    try:
        response = requests.get(CSV_URL, allow_redirects=True, timeout=10)
        response.encoding = 'utf-8'
        reader = csv.DictReader(StringIO(response.text))
        return list(reader)
    except Exception as e:
        print(f"❌ Erreur chargement Google Sheets: {e}")
        return []

# Contexte pour Sofia - Philosophie incarnée
CONCEPTS_CONTEXT = """
Tu es Sofia, une assistante philosophique qui aide à comprendre le vécu grâce aux concepts.

Concepts disponibles avec définitions :
- Aliénation : Ne plus s'appartenir, être dépossédé de soi-même
- Émancipation : Se libérer d'une contrainte, d'une servitude
- Liberté : N'être soumis qu'aux obligations qu'on se choisit
- Identité : Ce qui permet de reconnaître quelqu'un dans son unité et dans le temps
- Différence : Ce qui permet de distinguer les choses
- Société : Groupement qui place l'individu au centre
- Communauté : Groupement réuni autour d'une culture et d'une identité communes
- Culture : Connaissances et comportements propres à une communauté
- Morale : Recherche d'un idéal de conduite
- Éthique : Principes régulateurs de l'action humaine
- État : Institutions qui gouvernent un pays
- Autorité : Pouvoir de commander
- Pouvoir : Capacité d'agir, de contraindre
- Conscience : Connaissance de soi et du monde
- Inconscient : Ce qui échappe à la conscience
- Attention : Concentration de l'esprit sur quelque chose
- Mémoire : Conservation et rappel du passé
- Perception : Saisie du monde par les sens
- Temps : Durée dans laquelle se succèdent les événements
- Travail : Activité transformatrice
- Technique : Savoir-faire pratique
- Religion : Croyance en une réalité transcendante
- Croyance : Adhésion à une idée sans preuve
- Devoir : Obligation morale
- Mort : Fin de la vie
- Amour : Sentiment d'attachement profond
- Vérité : Conformité de la pensée avec la réalité
- Philosophie : Désir de sagesse et de connaissance

Concepts associés (pour l'étape 4) :
- Aliénation ↔ Émancipation, Liberté
- Identité ↔ Différence
- Société ↔ Communauté
- Morale ↔ Éthique
- Conscience ↔ Inconscient
- Attention ↔ Perception, Mémoire
- Travail ↔ Liberté, Technique
- Croyance ↔ Religion, Vérité

Ta méthode en 4 étapes STRICTES :

ÉTAPE 1 (premier message uniquement) :
Message d'accueil : "Hello ! Content de te voir ! Quelle idée te parle le plus aujourd'hui ?"

ÉTAPE 2 (après le choix du concept) :
"À quelle expérience que tu as vécue cette idée te fait-elle penser ? Ça peut être un cours, un voyage, une dispute, etc."

ÉTAPE 3 (après le récit de l'expérience) :
- Reformule l'expérience EN UTILISANT la définition du concept choisi
- Exemple avec Émancipation : "Tu parles de te libérer d'une contrainte. De quelle contrainte s'agissait-il ?"
- Exemple avec Liberté : "Tu décris un moment où tu n'étais soumis qu'à tes propres choix. Comment as-tu ressenti ça ?"

ÉTAPE 4 (creuser l'analyse) :
- Propose UN concept associé pour approfondir
- Exemple : "Cette expérience te parle aussi d'[autre concept]. Comment ces deux idées se relient dans ton vécu ?"

RÈGLES ABSOLUES :
- MAXIMUM 2 phrases par réponse (jamais plus)
- Ta DERNIÈRE phrase doit TOUJOURS être une question
- Phrases courtes et directes
- Ton sympathique, jamais de flatterie ni de condescendance
- TOUJOURS reformuler avec les définitions des concepts

Objectif : philosophie incarnée = comprendre son vécu par les concepts.
"""

@app.route('/chat', methods=['POST'])
def chat():
    """
    Endpoint pour recevoir les messages et générer des réponses avec Claude
    """
    try:
        data = request.json
        user_message = data.get('message', '')
        conversation_history = data.get('history', [])
        
        if not user_message:
            return jsonify({'error': 'Message requis'}), 400
        
        # Construction de l'historique de conversation pour Claude
        messages = []
        for msg in conversation_history[-10:]:  # Garder les 10 derniers messages
            messages.append({
                "role": msg['role'],
                "content": msg['content']
            })
        
        # Ajout du message actuel
        messages.append({
            "role": "user",
            "content": user_message
        })
        
        # Appel à l'API Claude
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1024,
            system=CONCEPTS_CONTEXT,
            messages=messages
        )
        
        assistant_message = response.content[0].text
        
        return jsonify({
            'response': assistant_message,
            'success': True
        })
        
    except Exception as e:
        error_msg = repr(e)  # Utiliser repr() au lieu de str() pour éviter les problèmes d'encodage
        print(f"Erreur dans /chat: {error_msg}", file=sys.stderr)
        return jsonify({
            'error': error_msg,
            'success': False
        }), 500

@app.route('/api/concepts', methods=['GET'])
def get_concepts():
    """
    Endpoint pour récupérer tous les concepts depuis Google Sheets
    Retourne les nœuds et les relations pour le graphe vis.js
    """
    try:
        # Charger les concepts depuis Google Sheets
        concepts = load_concepts_from_gsheet()
        
        if not concepts:
            return jsonify({
                'error': 'Impossible de charger les concepts',
                'success': False
            }), 503
        
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
            color = CATEGORY_COLORS.get(categorie, '#97C2FC')
            
            # Couleur de police (blanc pour Politique et Sciences)
            font_color = 'white' if categorie in ['Politique', 'Sciences'] else '#333'
            
            if not label:  # Skip empty rows
                continue
            
            # Enregistrer le mapping
            label_to_id[label] = concept_id
            
            # Créer le nœud
            node = {
                'id': concept_id,
                'label': label,
                'title': f"{definition}\n\nCatégorie: {categorie}",
                'color': color,
                'group': categorie,
                'font': {'color': font_color}
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
                relations_str = concept.get('', '').strip()
            
            if relations_str:
                related_concepts = [r.strip() for r in relations_str.split(',')]
                for related_label in related_concepts:
                    if related_label and related_label in label_to_id:
                        edge = {
                            'from': concept_id,
                            'to': label_to_id[related_label]
                        }
                        edges.append(edge)
        
        return jsonify({
            'nodes': nodes,
            'edges': edges,
            'success': True
        })
        
    except Exception as e:
        error_msg = repr(e)
        print(f"Erreur dans /api/concepts: {error_msg}", file=sys.stderr)
        return jsonify({
            'error': str(e),
            'success': False
        }), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    # Vérifier que la clé API est configurée
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("⚠️  ANTHROPIC_API_KEY n'est pas configurée")
        print("📋 Créez un fichier .env avec : ANTHROPIC_API_KEY=votre_clé")
    else:
        print("✅ API configurée")
    
    # Utiliser le port fourni par Railway ou 5001 en local
    port = int(os.environ.get("PORT", 5001))
    app.run(host='0.0.0.0', port=port, debug=False)
