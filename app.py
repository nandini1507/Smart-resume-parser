import streamlit as st
import os
import re
from pathlib import Path
import json
import pandas as pd


# -----------------------------
# Configuration
# -----------------------------
UPLOAD_FOLDER = "test resume"

# Ensure folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# -----------------------------
# Resume Parsing Function
# -----------------------------
def parse_resume(text):
    """Enhanced resume parser extracting email, phone, skills, education, experience, LinkedIn."""
    data = {}

    # Extract email
    email_match = re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
    data["email"] = email_match.group() if email_match else "Not found"

    # Extract phone number
    phone_match = re.search(r"\+?\d[\d\s\-]{8,}\d", text)
    data["phone"] = phone_match.group() if phone_match else "Not found"

    # Extract LinkedIn URL
    linkedin_match = re.search(r"(https?://)?(www\.)?linkedin\.com/[a-zA-Z0-9_/\\-]+", text)
    data["linkedin"] = linkedin_match.group() if linkedin_match else "Not found"

    # Extract skills (simple keyword match)
    skills_keywords = [
  "Python", "SQL", "Streamlit", "Pandas", "NumPy", "Tableau", "Git", "Excel",
  "Machine Learning", "Deep Learning", "AWS", "Docker", "Kubernetes",
  "Java", "C++", "Communication", "Leadership", "Power BI", "Hadoop"
]
    data["skills"] = [skill for skill in skills_keywords if skill.lower() in text.lower()]

    # Extract education (look for degrees)
    education_keywords = ["Bachelor", "Master", "B.Tech", "M.Tech", "MBA", "PhD", "B.Sc", "M.Sc"]
    education_matches = [edu for edu in education_keywords if edu.lower() in text.lower()]
    data["education"] = education_matches if education_matches else ["Not found"]

    # Extract experience (look for years of experience)
    roles_keywords = ["Intern", "Trainee", "Engineer", "Developer", "Analyst", "Manager", "Consultant", "Researcher"]
    found_roles = []
    for role in roles_keywords:
        if role.lower() in text.lower():
            found_roles.append(role)
    data["work_roles"] = found_roles if found_roles else ["Not found"]

    return data

# -----------------------------
# Streamlit UI
# -----------------------------
st.title("📄 Smart Resume Parser")
st.write("Upload a PDF or DOCX resume. It will be saved in the **test resume** folder.")

uploaded_file = st.file_uploader("Upload your resume", type=["pdf", "docx"])

if uploaded_file is not None:
    # Save file
    save_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"✅ File saved to `{save_path}`")

    # Extract text
    raw_text = ""
    if uploaded_file.type == "application/pdf":
        try:
            import PyPDF2
            reader = PyPDF2.PdfReader(uploaded_file)
            for page in reader.pages:
                raw_text += page.extract_text() or ""
        except Exception as e:
            st.error(f"Error reading PDF: {e}")

    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        try:
            import docx
            doc = docx.Document(uploaded_file)
            raw_text = "\n".join([para.text for para in doc.paragraphs])
        except Exception as e:
            st.error(f"Error reading DOCX: {e}")

    # Parse resume if text extracted
    if raw_text.strip():
        try:
            data = parse_resume(raw_text)
            st.write("### Parsed Resume Data")
            st.json(data)
        except Exception as e:
            st.error(f"Error parsing resume: {e}")
    else:
        st.error("No text could be extracted from the resume.")
    base_name = Path(uploaded_file.name).stem
    json_path = Path(f"outputs/json/{base_name}.json")
    csv_path = Path(f"outputs/csv/{base_name}.csv")

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    summary = {
        "email": data.get("email", ""),
        "phone": data.get("phone", ""),
        "skills": "; ".join(data.get("skills", [])),
        "education_count": len(data.get("education", [])),
        "experience_count": len(data.get("experience", [])),
    }
    pd.DataFrame([summary]).to_csv(csv_path, index=False)
    with open(json_path, "rb") as f:
        st.download_button("⬇️ Download JSON", f.read(), file_name=json_path.name, mime="application/json")

    with open(csv_path, "rb") as f:
        st.download_button("⬇️ Download CSV summary", f.read(), file_name=csv_path.name, mime="text/csv")