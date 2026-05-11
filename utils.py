import pdfplumber
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ---------- TEXT ----------
def extract_text(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text.lower()

# ---------- CONTACT ----------
def extract_email(text):
    match = re.findall(r"\S+@\S+", text)
    return match[0] if match else "Not found"

def extract_phone(text):
    match = re.findall(r"\+?\d[\d\s-]{8,}", text)
    return match[0] if match else "Not found"

# ---------- SKILLS ----------
def extract_skills(text):
    skills_db = [
        "python","java","c++","sql","machine learning","deep learning",
        "ai","data analysis","pandas","numpy","tensorflow","pytorch",
        "html","css","javascript","react","node","flask","django",
        "git","docker","kubernetes","aws","azure","linux"
    ]
    return list(set([s for s in skills_db if s in text]))

# ---------- JOB MATCH ----------
def job_match(resume_text, job_desc):
    if not job_desc.strip():
        return 0
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([resume_text, job_desc.lower()])
    score = cosine_similarity(vectors[0], vectors[1])[0][0]
    return int(score * 100)

def matched_skills(skills, job_desc):
    return [s for s in skills if s in job_desc.lower()]

# ---------- 🔥 RECRUITER ATS ----------
def ats_score(text, job_desc):
    score = 0
    text = text.lower()
    job_desc = job_desc.lower() if job_desc else ""

    # 1. Job relevance (40)
    if job_desc.strip():
        vectorizer = TfidfVectorizer()
        vectors = vectorizer.fit_transform([text, job_desc])
        similarity = cosine_similarity(vectors[0], vectors[1])[0][0]
        score += similarity * 40
    else:
        score += 20

    # 2. Skills depth (20)
    skills = extract_skills(text)
    score += min(len(skills) * 2, 20)

    # 3. Structure (15)
    sections = ["education", "experience", "project", "skills"]
    for sec in sections:
        if sec in text:
            score += 3.75

    # 4. Experience signals (10)
    strong_words = ["developed", "built", "implemented", "designed"]
    if any(w in text for w in strong_words):
        score += 10

    # 5. Contact (5)
    if extract_email(text) != "Not found":
        score += 2.5
    if extract_phone(text) != "Not found":
        score += 2.5

    # 6. Quality (10)
    length = len(text)
    if length > 1500:
        score += 10
    elif length > 800:
        score += 7
    else:
        score += 4

    return int(min(score, 100))

# ---------- FEEDBACK ----------
def basic_feedback(text):
    fb = []
    if "project" not in text:
        fb.append("Add more projects.")
    if "experience" not in text:
        fb.append("Include work experience.")
    if "skills" not in text:
        fb.append("Add a skills section.")
    if len(text) < 800:
        fb.append("Resume is too short.")
    return fb if fb else ["Great Resume!"]