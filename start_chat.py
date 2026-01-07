#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour lancer à la fois le backend API et le serveur web frontend
"""

import subprocess
import time
import signal
import sys
import os

processes = []

def signal_handler(sig, frame):
    print("\n🛑 Arrêt des serveurs...")
    for p in processes:
        p.terminate()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 DÉMARRAGE DE SOFIA AI CHAT")
    print("=" * 60)
    print()
    
    # Vérifier la clé API
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("⚠️  Chargement de .env...")
        try:
            with open('.env', 'r') as f:
                for line in f:
                    if line.strip() and not line.startswith('#'):
                        key, value = line.strip().split('=', 1)
                        os.environ[key] = value
        except FileNotFoundError:
            print("❌ Fichier .env non trouvé")
            sys.exit(1)
    
    print("✅ Configuration chargée")
    print()
    
    # Démarrer le backend API
    print("🔧 Démarrage du backend API (port 5000)...")
    backend = subprocess.Popen(
        ['python', 'chat_backend.py'],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True
    )
    processes.append(backend)
    time.sleep(2)
    
    # Démarrer le serveur web frontend
    print("🌐 Démarrage du serveur web (port 8000)...")
    frontend = subprocess.Popen(
        ['python', '-m', 'http.server', '8000'],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True
    )
    processes.append(frontend)
    time.sleep(1)
    
    print()
    print("=" * 60)
    print("✨ SERVEURS DÉMARRÉS")
    print("=" * 60)
    print()
    print("📱 Ouvrez votre navigateur à l'adresse :")
    print("   👉 http://localhost:8000/index_ai_chat.html")
    print()
    print("💡 Appuyez sur Ctrl+C pour arrêter les serveurs")
    print("=" * 60)
    print()
    
    # Ouvrir automatiquement le navigateur
    import webbrowser
    webbrowser.open('http://localhost:8000/index_ai_chat.html')
    
    # Garder le script actif
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        signal_handler(None, None)
