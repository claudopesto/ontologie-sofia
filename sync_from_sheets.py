import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json

# Configuration simple avec accès public
def sync_from_public_sheet(sheet_url):
    """
    Synchronise les données depuis un Google Sheet public
    
    Args:
        sheet_url: URL du Google Sheet (ex: https://docs.google.com/spreadsheets/d/XXXXX/edit)
    """
    try:
        # Extraire l'ID du sheet depuis l'URL
        if '/d/' in sheet_url:
            sheet_id = sheet_url.split('/d/')[1].split('/')[0]
        else:
            sheet_id = sheet_url
        
        # Accéder au sheet en mode public
        gc = gspread.service_account_from_dict({
            "type": "service_account",
            "project_id": "public-sheets",
            "private_key_id": "",
            "private_key": "",
            "client_email": "public@example.com",
            "client_id": "",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
        })
        
        # Ouvrir le sheet
        sheet = gc.open_by_key(sheet_id)
        worksheet = sheet.sheet1  # Première feuille
        
        # Récupérer toutes les données
        data = worksheet.get_all_records()
        
        # Sauvegarder en CSV local
        import pandas as pd
        df = pd.DataFrame(data)
        csv_path = '/Users/elsa/Downloads/Concepts-Grid view (3).csv'
        df.to_csv(csv_path, index=False)
        
        print(f"✅ Données synchronisées avec succès!")
        print(f"📄 {len(data)} lignes importées")
        print(f"💾 Sauvegardé dans: {csv_path}")
        
        # Régénérer le HTML
        import subprocess
        subprocess.run(['python', 'interactive_graph.py'], check=True)
        print("🎨 HTML regénéré avec succès!")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        print("\n💡 Solution alternative: exportez manuellement votre Google Sheet en CSV")
        return False


def sync_from_csv_export():
    """
    Méthode simple : utilise le CSV exporté manuellement de Google Sheets
    """
    print("📋 Méthode simple activée:")
    print("1. Ouvrez votre Google Sheet")
    print("2. Fichier > Télécharger > Valeurs séparées par des virgules (.csv)")
    print("3. Placez le fichier dans /Users/elsa/Downloads/")
    print("4. Renommez-le 'Concepts-Grid view (3).csv'")
    print("5. Relancez ce script")
    
    import subprocess
    try:
        subprocess.run(['python', 'interactive_graph.py'], check=True)
        print("✅ HTML regénéré avec succès!")
    except Exception as e:
        print(f"❌ Erreur: {e}")


if __name__ == "__main__":
    print("🔄 Synchronisation de l'ontologie depuis Google Sheets")
    print("=" * 60)
    
    # Méthode simple recommandée
    print("\n🎯 MÉTHODE RECOMMANDÉE (la plus simple):")
    print("-" * 60)
    sync_from_csv_export()
    
    print("\n" + "=" * 60)
    print("📖 Pour automatiser complètement, utilisez Google Sheets API")
    print("   Je peux vous aider à configurer si besoin!")
