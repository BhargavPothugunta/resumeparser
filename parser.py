import re
import PyPDF2
import docx
import spacy
from typing import Dict

# Load spaCy's small English model for Named Entity Recognition (NER)
nlp = spacy.load("en_core_web_sm")

# Function to extract text from PDF files
def extract_text_from_pdf(pdf_path: str) -> str:
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text

# Function to extract text from DOCX files
def extract_text_from_docx(docx_path: str) -> str:
    doc = docx.Document(docx_path)
    text = ""
    for para in doc.paragraphs:
        text += para.text + '\n'
    return text

# Function to extract emails using regex
def extract_email(text: str) -> str:
    email_regex = r"[a-zA-Z0-9._%+-]+@[a-zAZ0-9.-]+\.[a-zA10]{2,}"
    emails = re.findall(email_regex, text)
    return emails[0] if emails else None

# Function to extract phone numbers using regex
def extract_phone_number(text: str) -> str:
    phone_regex = r"\(?\+?[0-9]*\)?[-.\s]?[0-9]+[-.\s]?[0-9]+[-.\s]?[0-9]+"
    phones = re.findall(phone_regex, text)
    return phones[0] if phones else None

# Function to extract skills using a predefined list
def extract_skills(text: str, skill_keywords: list) -> list:
    skills = []
    for skill in skill_keywords:
        if skill.lower() in text.lower():
            skills.append(skill)
    return skills

# Function to extract name using spaCy's Named Entity Recognition
def extract_name(text: str) -> str:
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == 'PERSON':
            return ent.text
    return "Unknown"

# Extract Work Experience
def extract_work_experience(text: str) -> list:
    work_keywords = ['experience', 'worked at', 'position', 'role', 'company', 'employed at']
    experiences = []
    for line in text.splitlines():
        for keyword in work_keywords:
            if keyword.lower() in line.lower():
                experiences.append(line.strip())
    return experiences

# Extract Education
def extract_education(text: str) -> list:
    education_keywords = ['degree', 'bachelor', 'master', 'phd', 'graduated', 'university', 'college', 'school']
    education = []
    for line in text.splitlines():
        for keyword in education_keywords:
            if keyword.lower() in line.lower():
                education.append(line.strip())
    return education

# Extract Certifications
def extract_certifications(text: str) -> list:
    certification_keywords = ['certified', 'certification', 'certificate', 'license']
    certifications = []
    for line in text.splitlines():
        for keyword in certification_keywords:
            if keyword.lower() in line.lower():
                certifications.append(line.strip())
    return certifications

# Extract Projects
def extract_projects(text: str) -> list:
    project_keywords = ['project', 'worked on', 'developed', 'built', 'designed', 'created']
    projects = []
    for line in text.splitlines():
        for keyword in project_keywords:
            if keyword.lower() in line.lower():
                projects.append(line.strip())
    return projects

# Extract Languages
def extract_languages(text: str) -> list:
    language_keywords = ['languages', 'fluent in', 'spoken', 'proficiency']
    languages = []
    for line in text.splitlines():
        for keyword in language_keywords:
            if keyword.lower() in line.lower():
                languages.append(line.strip())
    return languages

# Main function to parse the resume and extract relevant information
def parse_resume(file_path: str, file_type: str) -> dict:
    if file_type.lower() == 'pdf':
        text = extract_text_from_pdf(file_path)
    elif file_type.lower() == 'docx':
        text = extract_text_from_docx(file_path)
    else:
        raise ValueError("Unsupported file type")

    # Extract data
    name = extract_name(text)
    email = extract_email(text)
    phone = extract_phone_number(text)

    # Skills
    skill_keywords = ['Python', 'Java', 'C++', 'JavaScript', 'SQL', 'Machine Learning', 'Data Science']
    skills = extract_skills(text, skill_keywords)

    # Extract other details
    work_experience = extract_work_experience(text)
    education = extract_education(text)
    certifications = extract_certifications(text)
    projects = extract_projects(text)
    languages = extract_languages(text)

    resume_data = {
        'Name': name,
        'Email': email,
        'Phone': phone,
        'Skills': ', '.join(skills),
        'Work Experience': '\n'.join(work_experience),
        'Education': '\n'.join(education),
        'Certifications': '\n'.join(certifications),
        'Projects': '\n'.join(projects),
        'Languages': '\n'.join(languages),
    }

    return resume_data
