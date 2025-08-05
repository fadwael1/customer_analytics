import os
import pandas as pd
import tempfile
import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from customer_analytics.ingestion import load_data

def test_load_data_reads_csv(monkeypatch):
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as temp_file:
        temp_file.write("purchase_id,purchase_amount,customer_age,country_code,purchase_date\n")
        temp_file.write("1,100,25,FR,2024-01-01\n")
        temp_path = temp_file.name

    monkeypatch.setenv("DATA_PATH", temp_path)

    df = load_data()
    assert isinstance(df, pd.DataFrame)
    assert df.shape[0] == 1
    assert "purchase_amount" in df.columns

    os.remove(temp_path)

def test_load_data_file_not_found(monkeypatch):
    monkeypatch.setenv("DATA_PATH", "non_existent_path.csv")
    with pytest.raises(FileNotFoundError):
        load_data()
