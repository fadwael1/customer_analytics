from dotenv import load_dotenv
load_dotenv()  # Charger les variables d’environnement (comme DATA_PATH) avant leur utilisation

import os
import pandas as pd
import logging

from customer_analytics.cleaning import clean_data
from customer_analytics.transformation import compute_kpis, profile_memory, optimize_memory
from customer_analytics.utils import log_summary

def main():
    os.makedirs("reports", exist_ok=True)

    logging.basicConfig(
        filename="reports/data_pipeline.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        encoding="utf-8"
    )

    logging.info("=== DÉMARRAGE DE LA PIPELINE AVEC CHUNKS ===")
    print("Pipeline avec chunks...")

    chunk_size = 100000
    data_path = os.getenv("DATA_PATH")
    if data_path is None:
        raise ValueError("La variable d'environnement DATA_PATH n'est pas définie.")

    # Liste pour stocker tous les chunks optimisés
    optimized_chunks = []

    for i, chunk in enumerate(pd.read_csv(data_path, chunksize=chunk_size)):
        logging.info(f">>> Chunk {i+1} chargé ({chunk.shape[0]} lignes)")

        log_summary(chunk, f"Chunk {i+1} - brut")
        profile_memory(chunk, f"Chunk {i+1} - brut")

        chunk_clean = clean_data(chunk)

        if chunk_clean.empty:
            logging.warning(f"Chunk {i+1} nettoyé est vide, passage au chunk suivant.")
            continue

        chunk_optimized = optimize_memory(chunk_clean, cat_threshold=0.5)

        profile_memory(chunk_optimized, f"Chunk {i+1} - optimisé")
        log_summary(chunk_optimized, f"Chunk {i+1} - optimisé")

        # Sauvegarde partielle par chunk (optionnel, tu peux garder ou supprimer)
        mode = 'w' if i == 0 else 'a'
        header = i == 0
        chunk_optimized.to_csv("reports/optimized_data.csv", mode=mode, index=False, header=header)

        chunk_kpis = compute_kpis(chunk_optimized)
        chunk_kpis.to_csv("reports/kpi_summary.csv", mode=mode, index=False, header=header)

        # Stocker le chunk optimisé pour concaténation finale
        optimized_chunks.append(chunk_optimized)

    # Concaténer tous les chunks optimisés en un seul DataFrame final
    if optimized_chunks:
        full_clean_df = pd.concat(optimized_chunks, ignore_index=True)
        # Sauvegarder le fichier clean_data.csv pour drift.py
        full_clean_df.to_csv("reports/clean_data.csv", index=False)
        logging.info(f"Fichier clean_data.csv sauvegardé avec {full_clean_df.shape[0]} lignes.")
    else:
        logging.warning("Aucun chunk optimisé à concaténer, clean_data.csv non généré.")

    logging.info("=== FIN DE LA PIPELINE PAR CHUNKS ===")

if __name__ == "__main__":
    main()
