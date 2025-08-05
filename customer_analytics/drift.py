import pandas as pd
from ydata_profiling import ProfileReport

def generate_profile(df, title, output_file):
    profile = ProfileReport(df, title=title, explorative=True)
    profile.to_file(output_file=output_file)

def simulate_drift(df: pd.DataFrame) -> pd.DataFrame:
    df_drifted = df.copy()

    # 1. Injecter un mode de paiement rare (exemple : "crypto")
    rare_payment = "crypto"
    rare_rows = df_drifted.sample(frac=0.01, random_state=42).index  # 1% aléatoire
    df_drifted.loc[rare_rows, "payment_method"] = rare_payment

    # 2. Décaler le montant moyen d’achat (augmentation de 50%)
    df_drifted["purchase_amount"] *= 1.5

    return df_drifted

def compare_profiles(df_original, df_drifted):
    profile_orig = ProfileReport(df_original, title="Profil - Données Originales", explorative=True)
    profile_drift = ProfileReport(df_drifted, title="Profil - Données Dérivées", explorative=True)

    # Comparaison automatique
    comparison = profile_orig.compare(profile_drift)
    comparison.to_file("reports/compare_report.html")

def main():
    # Charger les données nettoyées finales
    df = pd.read_csv("reports/clean_data.csv")

    # Générer profil initial
    generate_profile(df, "Profil - Données Initiales", "reports/profiling_original.html")

    # Simuler dérive sur ces données
    df_drifted = simulate_drift(df)

    # Générer profil dérivé
    generate_profile(df_drifted, "Profil - Données Dérivées", "reports/profiling_drifted.html")

    # Comparer les deux profils
    compare_profiles(df, df_drifted)

    print(" Rapport de dérive généré avec succès : reports/compare_report.html")

if __name__ == "__main__":
    main()
