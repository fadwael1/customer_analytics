# Importations
import numpy as np          # Calcul numérique performant
import sys                  # Infos système (taille mémoire)
import pandas as pd         # Manipulation de données tabulaires

# ------------------ KPIs agrégés ------------------
def compute_kpis(df):
    """
    Calcule des KPI par pays et catégorie de produit :
      - chiffre d’affaires total
      - panier moyen
      - nombre de clients uniques
    """
    aggregations = {
        "purchase_amount": [("total_revenue", "sum"),
                            ("average_basket_size", "mean")],
        "customer_id":    [("number_of_unique_customers", "nunique")]
    }
    # Regrouper puis agréger
    grouped = (df
               .groupby(['country_code', 'product_category'])
               .agg(aggregations)
               .reset_index())

    # Aplatir les colonnes multi-niveaux créées par .agg()
    grouped.columns = ['country_code', 'product_category',
                       'total_revenue', 'average_basket_size',
                       'number_of_unique_customers']
    return grouped

# ------------------ Statistiques NumPy ------------------
def numpy_summary_stats(df):
    """Statistiques basées sur NumPy pour purchase_amount."""
    data = df['purchase_amount'].values
    return {
        "mean":           np.mean(data),
        "std_dev":        np.std(data),
        "percentile_25":  np.percentile(data, 25),
        "percentile_50":  np.percentile(data, 50),
        "percentile_75":  np.percentile(data, 75)
    }

# ------------------ Score Z & filtrage des outliers ------------------
def compute_z_scores(df):
    """Calcule les z-scores de purchase_amount."""
    data = df['purchase_amount'].values
    return (data - np.mean(data)) / np.std(data)

def filter_outliers(df):
    """Garde uniquement les achats dont le z-score est entre –3 et 3."""
    mask = np.abs(compute_z_scores(df)) <= 3
    return df[mask]

# ------------------ Profil mémoire ------------------
def profile_memory(df: pd.DataFrame, name: str = "DataFrame"):
    """Affiche la consommation mémoire détaillée."""
    print(f"\nProfil mémoire de {name} :")
    print(df.info(memory_usage='deep'))
    print(f"Taille totale via sys.getsizeof() : {sys.getsizeof(df)} octets")

# ------------------ Optimisation mémoire ------------------
def optimize_memory(df: pd.DataFrame, cat_threshold: float = 0.5) -> pd.DataFrame:
    """
    Réduit l’empreinte mémoire :
      1. Downcast des entiers et floats
      2. Conversion en 'category' si faible cardinalité (< cat_threshold)
    """
    # Downcast des entiers
    for col in df.select_dtypes(include=["int", "int64"]).columns:
        df[col] = pd.to_numeric(df[col], downcast="unsigned")

    # Downcast des floats
    for col in df.select_dtypes(include=["float", "float64"]).columns:
        df[col] = pd.to_numeric(df[col], downcast="float")

    # Conversion des chaînes peu distinctes en 'category'
    for col in df.select_dtypes(include=["object"]).columns:
        if df[col].nunique() / len(df) < cat_threshold:
            df[col] = df[col].astype("category")

    return df
