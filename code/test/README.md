# 📜 README: Test Suite for Compliance App

This test suite ensures the **Regulatory Compliance Assistant** works correctly by validating its functions for **transaction processing, anomaly detection, and rule validation**.

## 🛠️ Setup & Installation

### 1️⃣ Install Dependencies
Ensure you have the required libraries installed:
```bash
pip install pandas numpy scikit-learn streamlit transformers pytest
```

If `pytest` is not installed, install it separately:
```bash
pip install pytest
```

### 2️⃣ Run Tests
To execute all test cases, run:
```bash
pytest -v
```
This will show **detailed test results** in the console.

To run a **specific test file**, use:
```bash
pytest test_compliance.py -v
```

To run a **single test function**, use:
```bash
pytest test_compliance.py::test_validate_transaction -v
```

## 🧪 Test Coverage

| Test Function | Purpose |
|--------------|---------|
| `test_load_data()` | Ensures transaction CSV files are loaded correctly. |
| `test_load_regulatory_rules()` | Checks if regulatory rule files are correctly processed. |
| `test_extract_rules()` | Validates AI-generated rule extraction. |
| `test_validate_transaction()` | Confirms transaction validation logic based on compliance rules. |
| `test_detect_anomalies()` | Ensures anomaly detection and risk scoring work as expected. |

## 🛠️ Troubleshooting

### 🚨 Common Issues & Fixes

1️⃣ **Module Not Found Error (`ModuleNotFoundError`)**
✅ Ensure you are using the correct virtual environment:
```bash
source venv/bin/activate  # macOS/Linux  
venv\Scripts\activate     # Windows  
```

2️⃣ **Streamlit Not Found (`ModuleNotFoundError: No module named 'streamlit'`)**
✅ Run:
```bash
pip install streamlit
```

3️⃣ **Test Assertion Fails (`AssertionError`)**
✅ Check the **expected vs actual output** in pytest logs.  
✅ Update the test case if necessary.

## 🎯 Next Steps
- ✅ Add **mocked AI model responses** for `extract_rules()` testing.
- ✅ Improve test coverage with **edge cases** (e.g., missing transaction columns).
- ✅ Automate tests in CI/CD pipelines (e.g., GitHub Actions).


