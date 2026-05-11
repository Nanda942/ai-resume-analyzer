import streamlit as st
from utils import *
from fpdf import FPDF

st.set_page_config(page_title="AI Resume Analyzer PRO", layout="wide")
st.title("🚀 AI Resume Analyzer PRO+")

files = st.file_uploader("Upload Resumes", type="pdf", accept_multiple_files=True)
job_desc = st.text_area("Paste Job Description")

results = []

if files:
    for f in files:
        text = extract_text(f)
        skills = extract_skills(text)

        results.append({
            "name": f.name,
            "email": extract_email(text),
            "phone": extract_phone(text),
            "skills": skills,
            "ats": ats_score(text, job_desc),
            "match": job_match(text, job_desc),
            "matched": matched_skills(skills, job_desc),
            "text": text
        })

    # 🔥 ranking
    results = sorted(results, key=lambda x: x["ats"] + x["match"], reverse=True)

    st.subheader("🏆 Ranking")

    for i, r in enumerate(results):
        st.markdown(f"### {i+1}. {r['name']}")
        col1, col2 = st.columns(2)
        col1.metric("ATS", r["ats"])
        col2.metric("Match", r["match"])

        st.write("Skills:", r["skills"])
        st.write("Matched:", r["matched"])
        st.success(", ".join(basic_feedback(r["text"])))
        st.divider()

# 🔥 PDF
if results and st.button("📥 Generate Report"):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=10)

    for i, r in enumerate(results):
        pdf.add_page()

        # header
        pdf.set_fill_color(20,20,40)
        pdf.rect(0,0,210,25,'F')
        pdf.set_text_color(255,255,255)
        pdf.set_font("Arial","B",16)
        pdf.set_xy(10,8)
        pdf.cell(0,10,"AI Resume Report")

        pdf.ln(15)
        pdf.set_text_color(0,0,0)

        pdf.set_font("Arial","B",14)
        pdf.cell(0,10,f"{i+1}. {r['name']}", ln=True)

        def bar(label,val):
            pdf.set_font("Arial","B",11)
            pdf.cell(0,6,f"{label}: {val}", ln=True)
            pdf.set_fill_color(200,200,200)
            pdf.rect(pdf.get_x(), pdf.get_y(),180,6,'F')
            pdf.set_fill_color(0,150,255)
            pdf.rect(pdf.get_x(), pdf.get_y(),180*(val/100),6,'F')
            pdf.ln(8)

        bar("ATS", r["ats"])
        bar("Match", r["match"])

        pdf.set_font("Arial","B",12)
        pdf.cell(0,8,"Skills", ln=True)
        pdf.set_font("Arial", size=11)
        pdf.multi_cell(0,6,", ".join(r["skills"]))

        pdf.ln(3)

        pdf.set_font("Arial","B",12)
        pdf.cell(0,8,"Suggestions", ln=True)
        pdf.set_font("Arial", size=11)
        for f in basic_feedback(r["text"]):
            pdf.multi_cell(0,6,f"- {f}")

    pdf.output("report.pdf")

    with open("report.pdf","rb") as f:
        st.download_button("Download Report", f, file_name="report.pdf")