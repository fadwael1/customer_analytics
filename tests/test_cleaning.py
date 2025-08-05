import pandas as pd
import os 
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from customer_analytics.cleaning import clean_data

def test_clean_data_removes_duplicates():
    df = pd.DataFrame({
        "purchase_id": [1, 1, 2],
        "purchase_amount": [100, 100, 200],
        "customer_age": [25, 25, 30],
        "country_code": ["FR", "FR", "US"],
        "purchase_date": ["2024-01-01", "2024-01-01", "2024-01-02"]
    })
    cleaned = clean_data(df)
    assert cleaned.shape[0] == 2  # Un doublon supprimé

def test_clean_data_removes_missing_and_invalid():
    df = pd.DataFrame({
        "purchase_id": [1, 2],
        "purchase_amount": [100, None],
        "customer_age": [9, 25],
        "country_code": ["FR", None],
        "purchase_date": ["2024-01-01", "2024-01-02"]
    })
    cleaned = clean_data(df)
    assert cleaned.empty  # Toutes les lignes devraient être supprimées
