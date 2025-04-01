import os
import re
import spacy
import docx2txt
import pandas as pd
from pdfminer.high_level import extract_text
import nltk

# ✅ Ensure NLTK data is downloaded
nltk.download('punkt')

# ✅ Load NLP model
nlp = spacy.load("en_core_web_sm")

# ✅ Load predefined skill set from CSV
SKILLS_DF = pd.read_csv("/Users/murthis/VScode/skills_dataset.csv")
SKILLS_LIST = set(SKILLS_DF["Skill"].str.lower().tolist())

# ✅ Extract text from resumes (PDF or DOCX)
def extract_resume_text(file_path):
    try:
        ext = os.path.splitext(file_path)[1].lower()
        if ext == ".pdf":
            return extract_text(file_path)
        elif ext == ".docx":
            return docx2txt.process(file_path)
        else:
            print("❌ Unsupported file format:", ext)
            return ""
    except Exception as e:
        print(f"❌ Error extracting text from {file_path}: {e}")
        return ""

# ✅ Extract Name (Only from Email)
def extract_name(text, email=""):
    try:
        if email:
            return extract_name_from_email(email)  # ✅ Extract and return name from email immediately
    except Exception as e:
        print(f"❌ Error extracting name: {e}")
    return None  # Return None if email is missing

# ✅ Extract Name from Email
def extract_name_from_email(email):
    try:
        email_prefix = email.split("@")[0]  # Get part before "@"
        name_parts = re.split(r"[\.\d_]", email_prefix)  # Remove numbers & dots
        name_parts = [part.capitalize() for part in name_parts if part.isalpha()]  # Format as Title Case

        if len(name_parts) >= 2:
            return " ".join(name_parts)  # ✅ Return full name (First + Last)
        elif len(name_parts) == 1:
            return name_parts[0]  # ✅ Return just the first name if no last name

    except Exception as e:
        print(f"❌ Error extracting name from email: {e}")

    return None  # Return None if email is empty or invalid


# ✅ Extract Phone Number
def extract_phone_number(text):
    phone_pattern = re.compile(r'\+?\d{1,3}?[-.\s]?\(?\d{2,4}?\)?[-.\s]?\d{3,4}[-.\s]?\d{3,4}')
    matches = phone_pattern.findall(text)
    return matches[0] if matches else None

# ✅ Extract Email
def extract_email(text):
    email_pattern = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
    matches = email_pattern.findall(text)
    return matches[0] if matches else None

# ✅ Extract Skills
def extract_skills(text):
    try:
        text_lower = text.lower()
        found_skills = [skill for skill in SKILLS_LIST if re.search(rf"\b{re.escape(skill)}\b", text_lower)]
        return list(set(found_skills))
    except Exception as e:
        print(f"❌ Error extracting skills: {e}")
    return []

# ✅ Extract Education
def extract_education(text):
    try:
        EDUCATION_KEYWORDS = ["bachelor", "master", "phd", "degree", "university", "college"]
        sentences = text.split("\n")
        
        education = [sentence.strip() for sentence in sentences if any(keyword in sentence.lower() for keyword in EDUCATION_KEYWORDS)]
        return education
    except Exception as e:
        print(f"❌ Error extracting education: {e}")
    return []

# ✅ Main Resume Parsing Function
def parse_resume(file_path):
    text = extract_resume_text(file_path)
    
    email = extract_email(text)  # ✅ Extract email first
    name = extract_name(text, email)  # ✅ Name is only taken from email
    
    return {
        "Name": name,
        "Phone": extract_phone_number(text),
        "Email": email,
        "Skills": extract_skills(text),
        "Education": extract_education(text),
    }

# ✅ Test Case
if __name__ == "__main__":
    resume_path = input("\n📂 Enter the path of the resume file: ").strip()
    result = parse_resume(resume_path)

    # Print final output
    import json
    print("\n📜 Final Parsed Resume Data:")
    print(json.dumps(result, indent=4))
