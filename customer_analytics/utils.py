# Importer les bibliothèques nécessaires
import os            # Pour gérer les dossiers et chemins
import logging       # Pour écrire des logs (journalisation)
import pandas as pd  # Pour manipuler les DataFrames

# Créer un dossier "reports" 
os.makedirs("reports", exist_ok=True)

# Configurer le logger pour enregistrer les messages dans un fichier
logging.basicConfig(
    filename="reports/data_pipeline.log",  # Fichier de log
    level=logging.INFO,                    # Niveau d'information (INFO)
    format="%(asctime)s - %(levelname)s - %(message)s"  # Format des messages
)

# Fonction pour concaténer plusieurs DataFrames en un seul
def concat_dataframes(dfs: list[pd.DataFrame]) -> pd.DataFrame:
    """
    Concatène une liste de DataFrames en un seul DataFrame.
    """
    logging.info("Concaténation de plusieurs DataFrames.")
    concatenated_df = pd.concat(dfs, ignore_index=True)  # Réinitialiser les index
    logging.info(f"DataFrame concaténé avec {concatenated_df.shape[0]} lignes et {concatenated_df.shape[1]} colonnes.")
    return concatenated_df

# Fonction pour enregistrer un résumé d’un DataFrame dans le fichier de log
def log_summary(df: pd.DataFrame, description: str):
    """
    Enregistre dans le log les informations de base d'un DataFrame.
    """
    logging.info(f"Résumé - {description}")
    logging.info(f"Nombre de lignes : {df.shape[0]}")
    logging.info(f"Nombre de colonnes : {df.shape[1]}")
    logging.info(f"Colonnes : {df.columns.tolist()}")
    logging.info(f"Aperçu des données :\n{df.head(3).to_string(index=False)}\n")

# Fonction pour sauvegarder un DataFrame dans un fichier CSV dans le dossier "reports"
def save_dataframe(df: pd.DataFrame, filename: str):
    """
    Sauvegarde un DataFrame dans un fichier CSV dans le dossier reports.
    """
    output_path = os.path.join("reports", filename)  # Chemin de sortie
    df.to_csv(output_path, index=False)              # Sauvegarder sans les index
    logging.info(f"DataFrame sauvegardé dans : {output_path}")
