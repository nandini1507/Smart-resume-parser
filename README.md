# Smart-Resume-Parser
Smart Resume Parser is a Streamlit-based app that extracts key information from resumes (PDF/DOCX), including contact details, skills, education, experience, and job roles like Intern or Developer. Built with Python, it uses regex and basic NLP to convert unstructured resume text into structured, recruiter-friendly data

# 📄 Smart Resume Parser

A Streamlit app that extracts key information from resumes (PDF/DOCX) including:
- Contact details (Email, Phone, LinkedIn)
- Skills
- Work experience roles (Intern, Developer, Analyst, Manager, etc.)
- Years of experience

This project is designed to help recruiters and job seekers quickly parse resumes into structured data.

---

## 🚀 Features
- Upload resumes in **PDF** or **DOCX** format
- Automatic saving to a `test resume/` folder
- Extracts:
  - 📧 Email
  - 📱 Phone number
  - 🔗 LinkedIn profile
  - 🛠 Skills (Python, SQL, ML, etc.)
  - 🎓 Education (Bachelor, Master, MBA, PhD, etc.)
  - 💼 Work roles (Intern, Developer, Analyst, Manager)
  - ⏳ Years of experience
- Saves parsed data into JSON and CSV logs
- Clean Streamlit interface

---

## 📂 Project Structure
Resume-Parser/
│── app.py # Streamlit app
│── parser.py # Resume parsing logic 
│── requirements.txt # Dependencies 
│── README.md # Project documentation 
│── .gitignore # Ignore uploads/logs 
│── test resume/ # Upload folder


---

## ⚙️ Installation / app working

Clone the repository:
```bash
git clone https://github.com/nandini1507/Smart Resume Parser.git
cd Smart Resume Parse
pip install -r requirements.txt
streamlit run app.py
```

🖼 Demo
Upload a resume and see parsed JSON output instantly.
Example output:
{
  "email": "abc@example.com",
  "phone": "+91 9876543210",
  "linkedin": "linkedin.com/in/abc",
  "skills": ["Python", "SQL", "Machine Learning"],
  "education": ["Bachelor"],
  "experience_years": ["2 years of experience in data analysis"],
  "work_roles": ["Intern", "Developer"]
}

## Tech Stack
Python (Regex, parsing logic)

Streamlit (UI framework)

PyPDF2 (PDF text extraction)

python-docx (DOCX text extraction)

pandas (CSV logging)

## Future Improvements
Add NLP for smarter skill extraction

Support more file formats (TXT, RTF)

Deploy on Streamlit Cloud for live demo

Build recruiter dashboard with filters

## Simply click the below link for the website
https://smart-resume-parser.netlify.app/
