import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import streamlit as st
from transformers import pipeline


# Load Data
def load_data(file_path):
    try:
        df = pd.read_csv(file_path, encoding="utf-8")
        print("CSV Columns Found:", df.columns.tolist())
        df.columns = df.columns.str.strip().str.lower()
        df.rename(columns={"transaction_date": "Transaction_Date", "transaction_amount": "Transaction_Amount"},
                  inplace=True)
        if "Transaction_Amount" not in df.columns:
            raise KeyError(
                "Column 'Transaction_Amount' not found. Check CSV headers for hidden spaces or encoding issues.")
        df["Transaction_Date"] = pd.to_datetime(df["Transaction_Date"], errors="coerce")
        return df
    except Exception as e:
        st.error(f"Error loading CSV: {e}")
        return pd.DataFrame()


# Load Regulatory Reporting Instructions from File
def load_regulatory_rules(file):
    try:
        return file.getvalue().decode("utf-8")
    except Exception as e:
        return f"Error loading regulatory instructions: {e}"


# LLM-Based Rule Extraction Using Hugging Face
def extract_rules(text_instructions):
    try:
        generator = pipeline("text-generation", model="facebook/opt-1.3b")
        response = generator(text_instructions, max_length=200, do_sample=True)
        return response[0]['generated_text']
    except Exception as e:
        return f"Error generating rules: {e}"


# Generate Validation Rules with Remediation Suggestions
def validate_transaction(df, consolidated_rules):
    df["Transaction_Valid"] = True
    df["Remediation_Suggestion"] = "No issues detected."
    df["Transaction_Date"] = pd.to_datetime(df["Transaction_Date"], errors="coerce")

    if "Transaction amount should not be negative" in consolidated_rules:
        df.loc[df["Transaction_Amount"] < 0, "Transaction_Valid"] = False
        df.loc[df[
                   "Transaction_Amount"] < 0, "Remediation_Suggestion"] = "Review transaction details. Verify with customer."

    if "Transaction date should not be in the future" in consolidated_rules:
        df.loc[df["Transaction_Date"] > pd.Timestamp.today(), "Transaction_Valid"] = False
        df.loc[df[
                   "Transaction_Date"] > pd.Timestamp.today(), "Remediation_Suggestion"] = "Check if transaction date entry is incorrect."

    if "High-value transactions should be flagged" in consolidated_rules:
        df.loc[df["Transaction_Amount"] > 5000, "Transaction_Valid"] = False
        df.loc[df[
                   "Transaction_Amount"] > 5000, "Remediation_Suggestion"] = "Review high-value transactions for compliance."

    return df


# Anomaly Detection & Risk Scoring
def detect_anomalies(df):
    df["Anomaly_Reason"] = "No anomaly detected."
    df["Risk_Score"] = 1
    df["Transaction_Amount"] = pd.to_numeric(df["Transaction_Amount"], errors="coerce")
    df = df.dropna(subset=["Transaction_Amount"])
    model = IsolationForest(contamination=0.05, random_state=42)
    df["Anomaly_Score"] = model.fit_predict(df[["Transaction_Amount"]])
    df.loc[df["Anomaly_Score"] == -1, "Anomaly_Reason"] = "Unusual transaction amount detected."
    df.loc[df[
               "Anomaly_Score"] == -1, "Remediation_Suggestion"] = "Investigate unusual transaction. Cross-check with customer."

    def calculate_risk(row):
        risk = 1
        if row["Anomaly_Score"] == -1:
            risk = 6
        if row["Transaction_Amount"] > 500:
            risk += 1
        if row["Transaction_Amount"] > 1000:
            risk += 1
        if row["Transaction_Amount"] > 5000:
            risk += 2
        if row["Anomaly_Reason"] == "Unusual transaction amount detected.":
            risk += 1
        return min(risk, 10)

    df["Risk_Score"] = df.apply(calculate_risk, axis=1)
    return df


# Interactive Compliance UI
def compliance_ui():
    st.title("Regulatory Compliance Assistant")
    file = st.file_uploader("Upload Transaction Data (CSV)")
    rule_file = st.file_uploader("Upload Regulatory Rules (TXT)", type=["rtf"])
    if file:
        df = load_data(file)
        st.write("Data Preview:", df.head())
        uploaded_rules = "Default rules applied."
        if rule_file:
            uploaded_rules = load_regulatory_rules(rule_file)
        ai_generated_rules = extract_rules(uploaded_rules)
        consolidated_rules = uploaded_rules + "\n" + ai_generated_rules
        st.write("Consolidated Regulatory Rules:", consolidated_rules)
        df = validate_transaction(df, consolidated_rules)
        df = detect_anomalies(df)
        st.write("Processed Data with Risk Score:", df)


if __name__ == "__main__":
    compliance_ui()
