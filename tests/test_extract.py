"""Tests unitarios del modulo de ingesta (pytest)."""
from unittest.mock import MagicMock, patch

import pandas as pd

from ingestion.extract_api import extract


@patch("ingestion.extract_api.requests.get")
def test_extract_returns_flat_dataframe(mock_get):
    mock_resp = MagicMock()
    mock_resp.json.return_value = [
        {"customerID": "001", "customer": {"gender": "Male"}, "Churn": "No"}
    ]
    mock_get.return_value = mock_resp

    df = extract()

    assert isinstance(df, pd.DataFrame)
    assert "customer_gender" in df.columns
    assert len(df) == 1
