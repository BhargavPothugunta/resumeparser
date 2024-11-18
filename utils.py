import os
import re
from werkzeug.utils import secure_filename
from typing import List

# Allowed file extensions for uploads
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}

# Check if the file extension is allowed
def allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Function to extract text from a PDF file (using PyPDF2)
def extract_text_from_pdf(pdf_path: str) -> str:
    import PyPDF2
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    return text

# Function to extract text from a DOCX file (using python-docx)
def extract_text_from_docx(docx_path: str) -> str:
    import docx
    doc = docx.Document(docx_path)
    text = ""
    for para in doc.paragraphs:
        text += para.text + '\n'
    return text

# Function to extract email addresses from text using regex
def extract_email(text: str) -> str:
    email_regex = r"[a-zA-Z0-9._%+-]+@[a-zAZ0-9.-]+\.[a-zA-Z]{2,}"
    emails = re.findall(email_regex, text)
    return emails[0] if emails else None

# Function to extract phone numbers from text using regex
def extract_phone_number(text: str) -> str:
    phone_regex = r"\(?\+?[0-9]*\)?[-.\s]?[0-9]+[-.\s]?[0-9]+[-.\s]?[0-9]+"
    phones = re.findall(phone_regex, text)
    return phones[0] if phones else None

# Function to extract skills from the resume text based on a predefined list
def extract_skills(text: str, skill_keywords: List[str]) -> List[str]:
    skills = []
    for skill in skill_keywords:
        if skill.lower() in text.lower():
            skills.append(skill)
    return skills

# Function to extract name using spaCy's Named Entity Recognition (NER)
def extract_name(text: str) -> str:
    import spacy
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == 'PERSON':
            return ent.text
    return "Unknown"

# Function to extract work experience using specific keywords
def extract_work_experience(text: str) -> list:
    work_keywords = ['experience', 'worked at', 'position', 'role', 'company', 'employed at']
    experiences = []
    for line in text.splitlines():
        for keyword in work_keywords:
            if keyword.lower() in line.lower():
                experiences.append(line.strip())
    return experiences

# Function to extract education details using specific keywords
def extract_education(text: str) -> list:
    education_keywords = ['degree', 'bachelor', 'master', 'phd', 'graduated', 'university', 'college', 'school']
    education = []
    for line in text.splitlines():
        for keyword in education_keywords:
            if keyword.lower() in line.lower():
                education.append(line.strip())
    return education

# Function to extract certifications details using specific keywords
def extract_certifications(text: str) -> list:
    certification_keywords = ['certified', 'certification', 'certificate', 'license']
    certifications = []
    for line in text.splitlines():
        for keyword in certification_keywords:
            if keyword.lower() in line.lower():
                certifications.append(line.strip())
    return certifications

# Function to extract project-related information
def extract_projects(text: str) -> list:
    project_keywords = ['project', 'worked on', 'developed', 'built', 'designed', 'created']
    projects = []
    for line in text.splitlines():
        for keyword in project_keywords:
            if keyword.lower() in line.lower():
                projects.append(line.strip())
    return projects

# Function to extract languages from the resume text
def extract_languages(text: str) -> list:
    language_keywords = ['languages', 'fluent in', 'spoken', 'proficiency']
    languages = []
    for line in text.splitlines():
        for keyword in language_keywords:
            if keyword.lower() in line.lower():
                languages.append(line.strip())
    return languages

# Function to save an uploaded file to a specific folder
def save_file(file, upload_folder: str) -> str:
    filename = secure_filename(file.filename)
    file_path = os.path.join(upload_folder, filename)
    file.save(file_path)
    return file_path

# Function to create a folder if it doesn't exist
def create_folder_if_not_exists(folder_path: str):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

# Function to extract components (this can be called in `parse_resume()` from parser.py)
def extract_components(text: str, skill_keywords: List[str]) -> dict:
    name = extract_name(text)
    email = extract_email(text)
    phone = extract_phone_number(text)
    skills = extract_skills(text, skill_keywords)
    work_experience = extract_work_experience(text)
    education = extract_education(text)
    certifications = extract_certifications(text)
    projects = extract_projects(text)
    languages = extract_languages(text)

    components = {
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
    
    return components
