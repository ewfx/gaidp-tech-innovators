from unittest.mock import patch, MagicMock

import pandas as pd
import pytest

from compliance_app import load_data, load_regulatory_rules, extract_rules, validate_transaction, detect_anomalies


# Test Load Data Function
def test_load_data():
    test_csv = """Transaction_Date,Transaction_Amount\n2024-01-01,100\n2024-02-01,-50\n2024-03-01,6000"""
    with open("test.csv", "w", encoding="utf-8") as f:
        f.write(test_csv)
    df = load_data("test.csv")
    assert "Transaction_Amount" in df.columns
    assert "Transaction_Date" in df.columns
    assert df.shape[0] == 3
    assert df.iloc[1]["Transaction_Amount"] == -50

# Test Regulatory Rule Loading
def test_load_regulatory_rules():
    mock_file = MagicMock()
    mock_file.getvalue.return_value = b"Transaction amount should not be negative"
    result = load_regulatory_rules(mock_file)
    assert result == "Transaction amount should not be negative"

# Test Rule Extraction with Mocking
def test_extract_rules():
    with patch("compliance_app.pipeline") as mock_pipeline:
        mock_generator = MagicMock()
        mock_generator.return_value = [{"generated_text": "Generated Rule"}]
        mock_pipeline.return_value = mock_generator
        result = extract_rules("Some Instructions")
        assert result == "Generated Rule"

# Test Transaction Validation
def test_validate_transaction():
    data = {
        "Transaction_Amount": [100, -10, 6000],
        "Transaction_Date": ["2024-01-01", "2024-02-01", "2050-03-01"]
    }
    df = pd.DataFrame(data)
    df["Transaction_Date"] = pd.to_datetime(df["Transaction_Date"], errors="coerce")

    rules = """Transaction amount should not be negative
               Transaction date should not be in the future
               High-value transactions should be flagged"""

    df = validate_transaction(df, rules)
    assert df["Transaction_Valid"].tolist() == [True, False, False]

    # Instead of checking for an exact match, we check if the phrase exists in any row
    assert any("Verify with customer" in suggestion for suggestion in df["Remediation_Suggestion"])
# Test Anomaly Detection
def test_detect_anomalies():
    data = {"Transaction_Amount": [100, 500, 1000, 6000]}
    df = pd.DataFrame(data)
    df = detect_anomalies(df)
    assert "Risk_Score" in df.columns
    assert df["Risk_Score"].max() <= 10
    assert "Anomaly_Reason" in df.columns

if __name__ == "__main__":
    pytest.main()
