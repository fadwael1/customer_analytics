# Importer la bibliothèque pandas
import pandas as pd

# Fonction pour nettoyer les données
def clean_data(df: pd.DataFrame) -> pd.DataFrame:
   
    # Supprimer les doublons basés sur l'identifiant d'achat
    df = df.drop_duplicates(subset="purchase_id")

    # Supprimer les lignes avec des valeurs manquantes dans les colonnes importantes
    df = df.dropna(subset=["purchase_amount", "customer_age", "country_code", "purchase_date"])

    # Supprimer les lignes avec un montant d'achat négatif
    df = df[df["purchase_amount"] > 0]

    # Supprimer les lignes où l'âge du client est inférieur à 10 ans
    df = df[df["customer_age"] >= 10]

    # Convertir l'âge en entier
    df["customer_age"] = df["customer_age"].astype(int)

    # Retourner les données nettoyées
    return df
