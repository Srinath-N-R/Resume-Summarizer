# Resume Information Extractor and Summarizer

This Python project extracts crucial information from resumes and generates a concise summary through a user-friendly Flask frontend. It leverages open-source libraries for efficient information extraction and natural language processing.

## Features
- **Resume Parsing:** Accepts resumes in PDF and DOCX formats.
- **Information Extraction:** Utilizes spaCy and regular expressions to identify names, locations, addresses, and education details.
- **Summarization:** Converts extracted information into clear, human-readable summaries.
- **Flask Frontend:** Provides an intuitive web interface for uploading resumes and viewing summaries.

## Getting Started
1. Install requirements using this command: `pip install -r requirements.txt`
2. Install spaCy model using this command: `python -m spacy download en_core_web_trf`
3. Run `app.py`.
4. Upload a resume (PDF or DOCX).
5. Review extracted information (name, organization, education).
6. Click "Generate Summary" to get a summary of the resume.
7. Upload another resume or continue using the app.

## Acknowledgments
- Built with Flask, spaCy, and PyMuPDF.
- Inspired by the need for efficient resume screening and summarization.
