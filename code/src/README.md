# Regulatory Compliance Assistant

This project is a **Regulatory Compliance Assistant** that processes financial transactions, applies **regulatory reporting rules**, detects **anomalies**, and assigns **risk scores** to transactions.

It combines:
- **Uploaded Regulatory Reporting Instructions** (from a `.txt` file)
- **AI-Generated Rules** (via Hugging Face's `facebook/opt-1.3b`)
- **Transaction Validation & Risk Scoring**
- **Anomaly Detection** (using Isolation Forest)
- **Streamlit Web UI**

---

## 🛠️ **Setup & Installation**

### **1️⃣ Install Dependencies**
Run the following command to install required libraries:
```bash
pip install pandas numpy scikit-learn transformers streamlit
```
If you face issues with Hugging Face models, install PyTorch:
```bash
pip install torch
```

---

### **2️⃣ Running the Application**
Start the Streamlit web app with:
```bash
streamlit run app.py
```
Then open your browser and navigate to the displayed **local URL** (e.g., `http://localhost:8501`).

---

## 📂 **How to Use**

1️⃣ **Upload Transaction Data** (CSV format)
   - Ensure columns like `Transaction_Amount`, `Transaction_Date` exist.

2️⃣ **Upload Regulatory Rules** (TXT format)
   - The system reads **custom compliance rules** from this file.

3️⃣ **Automated AI Rule Extraction**
   - If no rules are uploaded, AI-generated rules are applied.

4️⃣ **Transaction Processing & Risk Scoring**
   - The system validates transactions using **both rule sets**.
   - Anomalies are detected and **Risk Scores** assigned.

5️⃣ **Review Results**
   - Processed transaction data with **flags, explanations, and risk scores** is displayed in the UI.

---

## 🚀 **Deployment**

### **Deploy with Docker**

1️⃣ **Build the Docker Image**:
```bash
docker build -t compliance-assistant .
```

2️⃣ **Run the Container**:
```bash
docker run -p 8501:8501 compliance-assistant
```
Now, access the app at `http://localhost:8501`.

---

### **Deploy on Cloud (AWS, GCP, Azure)**
- **AWS**: Deploy using **Elastic Beanstalk** or **Lambda**.
- **GCP**: Use **App Engine** or **Cloud Run**.
- **Azure**: Deploy with **Azure Web Apps**.

For cloud deployments, ensure dependencies are listed in `requirements.txt`.

---

## 📌 **Troubleshooting**
- **`KeyError: 'Transaction_Amount'`** → Ensure CSV headers are correct.
- **`ModuleNotFoundError: No module named 'transformers'`** → Run `pip install transformers`.
- **`RuntimeError: Model size too large`** → Try a smaller model like `distilgpt2`.


