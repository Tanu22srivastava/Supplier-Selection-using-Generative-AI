# Supplier Evaluation & Ranking System

📊 A Streamlit-based tool for evaluating and ranking suppliers using AI-powered insights, custom criteria, and machine learning techniques.

---

## 📌 Overview

This application helps businesses:

- **Upload supplier datasets (CSV)**
- **Rank suppliers** based on selected criteria or AI-driven clustering
- **Visualize supplier comparisons**
- **Generate AI-powered evaluation reports**
- **Export results to CSV and PDF**

It supports both **supervised** (if a `Label` column is present) and **unsupervised** methods for supplier evaluation.

---

## 🧰 Features

- ✅ Upload and preview supplier data
- 🎯 Choose between:
  - AI-powered ranking using Google Gemini
  - Manual ranking with custom criteria and filters
- 📊 Interactive charts comparing top suppliers
- 🤖 AI-generated supplier evaluation reports
- 📄 Export rankings and reports to CSV and PDF formats

---

## 📁 Folder Structure

```
supplier-evaluation-tool/
│
├── app.py                  # Main entry point
├── requirements.txt        # Python dependencies
│
├── core/                   # Data processing and ML logic
│   ├── data_loader.py
│   ├── data_preprocessor.py
│   └── model_handler.py
│
├── utils/                  # Utility modules
│   ├── chart_generator.py
│   ├── report_generator.py
│   └── pdf_exporter.py
│
├── ui/                     # UI components
│   ├── header.py
│   └── sidebar.py
│
└── config/                 # Configuration and secrets
    └── secrets.py          # ⚠️ API keys (NOT committed)
```

---

## 🔐 API Keys

This project uses **Google Gemini API** for generating AI-powered supplier reports. You must provide your own API key:

1. Get an API key from [Google AI Studio](https://makersuite.google.com/app/apikey) 
2. Paste it in `config/secrets.py`:

```python
GEMINI_API_KEY = "your-api-key-here"
```

> 💡 Add `config/secrets.py` to `.gitignore` to protect your key!

---

## 📦 Requirements

Install required packages via:

```bash
pip install -r requirements.txt
```

### `requirements.txt`

```
streamlit==1.24.0
pandas==2.0.3
scikit-learn==1.3.0
matplotlib==3.7.2
google-generativeai==0.3.1
fpdf==1.7.2
numpy==1.25.2
```

---

## 🚀 How to Run

```bash
streamlit run app.py
```

Then open your browser and go to the URL shown in the terminal.

---

## 📝 How to Use

1. **Upload** your supplier dataset (CSV format)
2. Choose a **ranking method**:
   - AI-powered evaluation (uses Gemini AI)
   - Custom criteria (select columns and sort directions)
3. Apply optional **filters** to narrow down suppliers
4. Click **"Process and Rank Suppliers"**
5. View the ranked list and **download results**
6. Generate an **AI-powered supplier report** (optional)
7. Export everything as **PDF**

---

## 📄 Sample Report Output

The AI-generated report includes:

- Supplier comparison table
- Pros and cons of each supplier
- Final recommendation with justification
- Visual bar charts (in PDF)

---

## 📁 Sample CSV Format

Your dataset should be a CSV file with headers. Example:

```csv
Supplier_ID,Quality,Delivery_Time,Cost,Reliability,Label
S001,9.2,5,850,0.95,1
S002,7.8,10,620,0.82,0
S003,8.5,7,750,0.88,1
...
```

- `Label` column is **optional** (for supervised learning).
- Any numeric, categorical, or text column can be used for filtering/ranking.


---

## 📜 License

MIT License – see `LICENSE` for details.
