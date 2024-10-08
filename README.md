# Resume Information Extractor and Summarizer

This Python project extracts crucial information from resumes and generates a concise summary through a user-friendly Flask frontend. It leverages open-source libraries for efficient information extraction and natural language processing.

## Features
- **Resume Parsing:** Accepts resumes in PDF and DOCX formats.
- **Information Extraction:** Utilizes LLM to identify key information.
- **Summarization:** Converts extracted information into concise summaries.
- **Flask Frontend:** Provides a web interface for parsing/summarizing resumes.

## Getting Started
1. Install requirements using this command: `pip install -r requirements.txt`
2. Update `config.py` and set your own `OPENAI_API_KEY`. Sample `OPENAI_API_KEY` can be found [here](https://docs.google.com/document/d/18WNb90tY7YsknNiHssgemMxb2DyAaTonKi6L2EhjkuA/edit?usp=sharing), it has rate limits.
5. Run `app.py`.
6. Upload a resume (PDF or DOCX).
7. Review extracted information (name, organization, education).
8. Click "Generate Summary" to get a summary of the resume.
9. Upload another resume or continue using the app.

## Acknowledgments
- Built with Flask, openai, and PyMuPDF.
- Inspired by the need for efficient and intellingent ATS systems.
