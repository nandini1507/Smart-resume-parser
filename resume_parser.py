import re
import json
import pandas as pd
import spacy
import fitz  # PyMuPDF
from docx import Document
import streamlit as st

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(file_path):
    """Extract text from PDF using PyMuPDF."""
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_text_from_docx(file_path):
    """Extract text from DOCX using python-docx."""
    doc = Document(file_path)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

def preprocess_text(text):
    """Clean and preprocess text: remove extra spaces, normalize."""
    text = re.sub(r'\s+', ' ', text)  # Remove extra whitespace
    text = text.strip()
    return text

def extract_skills(text):
    """Extract skills using regex and spaCy (e.g., nouns after 'Skills')."""
    skills_section = re.search(r'Skills?:?\s*(.*?)(?:\n\n|Experience|Education|$)', text, re.IGNORECASE | re.DOTALL)
    if skills_section:
        skills_text = skills_section.group(1)
        doc = nlp(skills_text)
        skills = [token.text for token in doc if token.pos_ in ['NOUN', 'PROPN'] and len(token.text) > 2]
        return list(set(skills))  # Remove duplicates
    return []

def extract_experience(text):
    """Extract experience using regex for job titles and dates."""
    experience = []
    exp_pattern = r'(\w+ \d{4} - \w+ \d{4}|\w+ \d{4} - Present)\s*(.*?)(?:\n\n|Education|Skills|$)'
    matches = re.findall(exp_pattern, text, re.IGNORECASE | re.DOTALL)
    for match in matches:
        experience.append({"period": match[0], "description": match[1].strip()})
    return experience

def extract_education(text):
    """Extract education using regex for degrees and institutions."""
    education = []
    edu_pattern = r'(Bachelor|Master|PhD|B\.S\.|M\.S\.|MBA)\s+in\s+(.*?)\s*from\s+(.*?)(?:\n\n|Experience|Skills|$)'
    matches = re.findall(edu_pattern, text, re.IGNORECASE | re.DOTALL)
    for match in matches:
        education.append({"degree": match[0], "field": match[1], "institution": match[2]})
    return education

def parse_resume(file_path):
    """Main parser function."""
    if file_path.endswith('.pdf'):
        text = extract_text_from_pdf(file_path)
    elif file_path.endswith('.docx'):
        text = extract_text_from_docx(file_path)
    else:
        raise ValueError("Unsupported file type")
    
    text = preprocess_text(text)
    
    skills = extract_skills(text)
    experience = extract_experience(text)
    education = extract_education(text)
    
    return {
        "skills": skills,
        "experience": experience,
        "education": education
    }

# Streamlit UI integration (see below for full app)