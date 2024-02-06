import re

import fitz  # PyMuPDF
import spacy
from docx import Document

# Load the spaCy model
nlp = spacy.load("en_core_web_trf")


def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF file.

    :param pdf_path: Path to the PDF file
    :return: Extracted text as a string
    """
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text


def extract_text_from_docx(docx_path):
    """
    Extracts text from a DOCX file.

    :param docx_path: Path to the DOCX file
    :return: Extracted text as a string
    """
    doc = Document(docx_path)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)


def extract_orgs_and_dates(text):
    doc = nlp(text)
    orgs_and_dates = []

    for ent in doc.ents:
        if ent.label_ == "ORG":
            # Initialize a variable to hold the closest year found after the organization
            closest_year = None
            post_org_text = text[ent.end_char:]  # Text after the organization

            # Search for the years mentioned after the organization
            year_matches = re.findall(r'\b\d{4}\b', post_org_text)
            for year in year_matches:
                if 1900 <= int(year) <= 2100:  # Validate it's a plausible year
                    closest_year = year
                    break  # Stop at the first plausible year found

            if closest_year:
                orgs_and_dates.append((ent.text, closest_year))

    return orgs_and_dates


def extract_latest_org_with_date(orgs_and_dates):
    if not orgs_and_dates:
        return None, None

    # Filter out organizations with the label "SKILLS" (incorrectly extracted)
    orgs_and_dates = [(org, year) for org, year in orgs_and_dates if org != "SKILLS"]

    if not orgs_and_dates:
        return None, None

    # Find the latest year mentioned
    latest_year = max(orgs_and_dates, key=lambda x: int(x[1]))[1]

    # Filter organizations with the latest year
    latest_orgs = [org for org, year in orgs_and_dates if year == latest_year]

    # If there are multiple organizations with the same latest year, choose the first one
    latest_org = latest_orgs[0]

    return latest_org, latest_year


def extract_information(text):
    """
    Enhanced information extraction from text using custom rules.
    """
    name = None
    latest_organization = None
    education_details = []

    # Attempt to extract name from the first few lines
    for ent in nlp(text.split('\n')[0]).ents:
        if ent.label_ == "PERSON":
            name = ent.text
            break  # Assuming the first PERSON entity in the first line is the name

    orgs_and_dates = extract_orgs_and_dates(text)
    latest_organization, latest_year = extract_latest_org_with_date(orgs_and_dates)

    # Extract education details using custom logic
    lines = text.split('\n')
    for line in lines:
        if "EDUCATION" in line:
            education_start = lines.index(line)
            break

    if education_start:
        education_text = '\n'.join(lines[education_start + 1:])
        education_details = [edu.strip() for edu in education_text.split('\n') if edu.strip()]

    # Refine this approach to better match your data and requirements
    return name, latest_organization, education_details
