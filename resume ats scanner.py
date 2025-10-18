import re
import spacy
from PyPDF2 import PdfReader
from docx import Document

# Load NLP model
nlp = spacy.load("en_core_web_sm")

# -------- Resume Reader Functions --------

def extract_text_from_pdf(file_path):
    text = ""
    try:
        reader = PdfReader(file_path)
        for page in reader.pages:
            text += page.extract_text() or ""
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return text

def extract_text_from_docx(file_path):
    text = ""
    try:
        doc = Document(file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
    except Exception as e:
        print(f"Error reading DOCX: {e}")
    return text

# -------- Resume Parsing --------

def extract_email(text):
    match = re.search(r'[\w\.-]+@[\w\.-]+', text)
    return match.group(0) if match else "Not Found"

def extract_phone(text):
    match = re.search(r'\b\d{10}\b', text)
    return match.group(0) if match else "Not Found"

def extract_skills(text):
    skills_list = [
        'python', 
    ]
    found = [skill for skill in skills_list if skill.lower() in text.lower()]
    return list(set(found))

def extract_education(text):
    edu_keywords = ['b.tech', 'btech', 'm.tech', 'mtech', 'be', 'b.e', 'msc', 'bsc', 'computer science']
    found = [edu for edu in edu_keywords if edu.lower() in text.lower()]
    return list(set(found))

def extract_projects(text):
    lines = [line for line in text.split('\n') if 'project' in line.lower()]
    return lines[:3] if lines else ["Not Found"]

# -------- Resume Scoring --------

def score_resume(skills_found):
    score = 0
    must_have_skills = ['python', ]
    optional_skills = ['machine learning', 'ai', 'flask', 'django', 'cloud']

    for skill in must_have_skills:
        if skill in skills_found:
            score += 10
    for skill in optional_skills:
        if skill in skills_found:
            score += 5

    return min(score, 100)

# -------- Main Function --------

def analyze_resume(file_path):
    if file_path.endswith(".pdf"):
        text = extract_text_from_pdf(file_path)
    elif file_path.endswith(".docx"):
        text = extract_text_from_docx(file_path)
    else:
        print("Unsupported file format")
        return

    email = extract_email(text)
    phone = extract_phone(text)
    skills = extract_skills(text)
    education = extract_education(text)
    projects = extract_projects(text)
    score = score_resume(skills)

    print("\n===== RESUME SCANNER REPORT =====")
    print(f"📧 Email: {email}")
    print(f"📞 Phone: {phone}")
    print(f"🎓 Education: {', '.join(education) if education else 'Not Found'}")
    print(f"🧠 Skills Found: {', '.join(skills) if skills else 'None'}")
    print(f"💼 Projects: {', '.join(projects)}")
    print(f"⭐ Resume Score: {score}/100")

    # Suggestions
    print("\nSuggestions:")
    if score < 60:
        print("- Add more core programming languages (Python, Java, etc.)")
        print("- Include technical projects or internships.")
        print("- Highlight certifications or skills in AI/ML.")
    else:
        print("- Great job! Your resume looks technically strong.")

# -------- Run Example --------

if __name__ == "__main__":
    file_path = input("Enter your resume file path (.pdf or .docx): ")
    analyze_resume(file_path)
