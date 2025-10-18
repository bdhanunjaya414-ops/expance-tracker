import re

def clean_text(text):
    """Remove special characters and convert to lowercase."""
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return text.lower()

def extract_keywords(text):
    """Split text into individual words."""
    words = text.split()
    return set(words)

def calculate_ats_score(resume_text, jd_text):
    """Calculate keyword match percentage between resume and job description."""
    resume_clean = clean_text(resume_text)
    jd_clean = clean_text(jd_text)

    resume_keywords = extract_keywords(resume_clean)
    jd_keywords = extract_keywords(jd_clean)

    matched_keywords = resume_keywords.intersection(jd_keywords)
    missing_keywords = jd_keywords.difference(resume_keywords)

    match_score = (len(matched_keywords) / len(jd_keywords)) * 100 if jd_keywords else 0

    return match_score, matched_keywords, missing_keywords


# ---------------- Main Program ---------------- #
if __name__ == "__main__":
    # Read resume and job description files
    with open("resume . txt", "r", encoding="utf-8") as file:
        resume_text = file.read()

    with open("job_description.txt", "r", encoding="utf-8") as file:
        jd_text = file.read()

    score, matched, missing = calculate_ats_score(resume_text, jd_text)

    print("\n=============================")
    print("📄 ATS Resume Match Report")
    print("=============================")
    print(f"✅ Match Score: {score:.2f}%")
    print(f"\n✅ Matched Keywords ({len(matched)}):")
    print(", ".join(list(matched)[:30]))  # show top 30

    print(f"\n❌ Missing Keywords ({len(missing)}):")
    print(", ".join(list(missing)[:30]))  # show top 30
    print("\n=============================")
