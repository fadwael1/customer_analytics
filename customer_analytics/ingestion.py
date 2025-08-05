# Importer le module os pour accéder aux variables d’environnement et aux chemins de fichiers
import os

# Importer pandas pour manipuler les données
import pandas as pd

# Importer la fonction load_dotenv pour charger les variables d’environnement depuis un fichier .env
from dotenv import load_dotenv

# Charger les variables d’environnement définies dans le fichier .env
load_dotenv()

# Fonction pour charger les données depuis un fichier CSV
def load_data() -> pd.DataFrame:
    # Récupérer le chemin du fichier à partir de la variable d’environnement DATA_PATH
    path = os.getenv("DATA_PATH")

    # Vérifier si le fichier existe, sinon lever une erreur
    if not os.path.exists(path):
        raise FileNotFoundError(f"Fichier non trouvé : {path}")

    # Lire le fichier CSV et le stocker dans un DataFrame
    df = pd.read_csv(path, chunksize=100_000)

    # Retourner le DataFrame contenant les données
    return df
