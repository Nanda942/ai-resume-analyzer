# 🚀 AI Resume Analyzer PRO+

An intelligent **AI-powered Resume Screening System** that simulates a real-world **Applicant Tracking System (ATS)**.

It parses resumes, extracts skills, ranks candidates, and evaluates them against job descriptions using **machine learning (TF-IDF similarity)** — all without external APIs.

---

## 🔥 Features

- 📄 Resume Parsing (PDF)
- 🧠 Skill Extraction (NLP-based)
- 🎯 Job Description Matching (TF-IDF)
- 💯 Recruiter-Level ATS Scoring
- 🏆 Multi-Candidate Ranking
- 📊 Visual Score Display
- 📥 Downloadable PDF Reports
- ⚡ No API Required (runs locally)

---

## 🧠 How It Works

1. Extracts text from resumes using **pdfplumber**
2. Identifies skills using keyword + NLP approach
3. Computes **ATS Score** based on:
   - Job relevance (TF-IDF similarity)
   - Skills depth
   - Resume structure
   - Experience indicators
   - Contact completeness
4. Ranks candidates based on ATS + Job Match
5. Generates a structured **PDF report**

---

## 🛠 Tech Stack

- Python
- Streamlit
- Scikit-learn (TF-IDF, Cosine Similarity)
- pdfplumber
- FPDF

---

## ▶️ How to Run

```bash
pip install -r requirements.txt
streamlit run app.py
