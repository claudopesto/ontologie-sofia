#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Backend API pour le chat Sofia avec intégration d'une IA
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from anthropic import Anthropic
from dotenv import load_dotenv

# Charger le fichier .env
load_dotenv()

app = Flask(__name__)

# Configuration CORS adaptée pour production
CORS(app, resources={
    r"/*": {
        "origins": [
            "https://*.vercel.app",
            "http://localhost:8000",
            "http://127.0.0.1:8000"
        ],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Configuration de l'API Anthropic (Claude)
client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# Contexte des concepts philosophiques (sera enrichi dynamiquement depuis MongoDB)
CONCEPTS_CONTEXT = """
Tu es Sofia, une assistante philosophique experte. Tu as accès aux concepts suivants :

- Aliénation : Être aliéné, c'est ne plus s'appartenir. C'est avoir le sentiment d'être dépossédé de soi-même.
- Identité : Ce qui permet de reconnaître quelqu'un ou quelque chose. Selon le principe d'identité, l'identité est le fait d'être égal à soi.
- Émancipation : Être émancipé, c'est sentir qu'on a réussi à se libérer d'une contrainte, d'une servitude.
- Liberté : État d'un individu qui n'est soumis qu'aux obligations qu'il se choisit.
- Société : La société place l'individu au centre des préoccupations.
- Communauté : Un groupement d'individus réunis autour d'une culture et d'une identité communes.
- Culture : L'ensemble des connaissances et des comportements propres à une communauté humaine.
- Morale : La recherche d'un idéal de conduite, qui définit des règles comportementales idéales.
- Éthique : Une branche philosophique qui cherche à connaître et à déterminer les principes régulateurs de l'action humaine.
- Bonheur : État de satisfaction complète et durable.

Réponds de manière pédagogique, concise et engageante. Utilise des exemples concrets. 
Si on te pose une question sur un concept que tu ne connais pas, dis-le honnêtement.
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
            model="claude-3-5-sonnet-20241022",
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
