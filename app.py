import os
from flask import Flask, flash, redirect, render_template, request, session, url_for
from config import Config
from modules.file_handler import handle_file_upload, extract_text_from_pdf, extract_text_from_docx
from modules.openai_handler import extract_information_with_gpt, generate_summary

# Initialize Flask app
app = Flask(__name__)

# Configure the upload folder and allowed extensions
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB upload limit
app.config['SECRET_KEY'] = Config.SECRET_KEY  # Secret key for session management

# Helper function to check allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Render the upload page."""
    return render_template('upload.html')

@app.route('/extract_info', methods=['POST'])
def extract_info():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(url_for('index'))
    
    file = request.files['file']
    if file.filename == '' or not allowed_file(file.filename):
        flash('No selected file or unsupported file format')
        return redirect(url_for('index'))

    # Save the uploaded file
    try:
        filename, filepath = handle_file_upload(file, app.config['UPLOAD_FOLDER'])
        print(f"File uploaded successfully: {filename}, saved at: {filepath}")
    except Exception as e:
        flash(f"Error saving the file: {e}")
        print(f"Error: Could not save file: {e}")
        return redirect(url_for('index'))

    # Extract text from the uploaded file
    try:
        if filename.endswith('.pdf'):
            text = extract_text_from_pdf(filepath)
        elif filename.endswith('.docx'):
            text = extract_text_from_docx(filepath)
        else:
            flash('Unsupported file format.')
            print("Error: Unsupported file format.")
            return redirect(url_for('index'))
    except Exception as e:
        flash(f"Error extracting text: {e}")
        print(f"Error extracting text from file: {e}")
        return redirect(url_for('index'))

    # Extract information using GPT
    try:
        extracted_info = extract_information_with_gpt(text)
        print(f"Extracted Info: {extracted_info}")
    except Exception as e:
        flash(f"Error extracting information: {e}")
        print(f"Error extracting information: {e}")
        if os.path.exists(filepath):
            os.remove(filepath)
        return redirect(url_for('index'))

    # Ensure file cleanup after processing
    if os.path.exists(filepath):
        os.remove(filepath)
    else:
        print(f"File not found for deletion: {filepath}")

    # Parse GPT's structured response
    parsed_data = parse_gpt_response(extracted_info)
    store_extracted_info_in_session(parsed_data)

    # Redirect to the extracted information page for review
    return render_template('extracted_info.html', **session)


@app.route('/generate_summary', methods=['POST'])
def generate_summary_route():
    """Generate a professional summary based on the reviewed/corrected information."""
    # Retrieve corrected information from the form submission
    name = request.form.get('name', 'N/A')
    location = request.form.get('location', 'N/A')
    nationality = request.form.get('nationality', 'N/A')
    useful_links = request.form.get('useful_links', '').split(',')

    # Job 1 Information
    job1 = {
        "organization": request.form.get('job1', 'N/A'),
        "job_title": request.form.get('job1_title', 'N/A'),
        "start_date": "N/A",
        "end_date": "N/A",
        "responsibilities": request.form.get('responsibilities1', '').split(',')
    }
    job1_timeline = request.form.get('job1_timeline', 'N/A')
    if " - " in job1_timeline:
        job1["start_date"], job1["end_date"] = job1_timeline.split(" - ", 1)

    # Job 2 Information
    job2 = {
        "organization": request.form.get('job2', 'N/A'),
        "job_title": request.form.get('job2_title', 'N/A'),
        "start_date": "N/A",
        "end_date": "N/A",
        "responsibilities": request.form.get('responsibilities2', '').split(',')
    }
    job2_timeline = request.form.get('job2_timeline', 'N/A')
    if " - " in job2_timeline:
        job2["start_date"], job2["end_date"] = job2_timeline.split(" - ", 1)

    # Other extracted information
    education = request.form.get('education', '').split(',')
    hard_skills = request.form.get('hard_skills', '').split(',')
    soft_skills = request.form.get('soft_skills', '').split(',')
    tools = request.form.get('tools', '').split(',')
    projects = request.form.get('projects', '').split(',')
    other_info = request.form.get('other_info', 'N/A')

    # Use the summarizer to generate a summary
    summary_text = generate_summary(
        name,
        job1,
        job2,
        education,
        hard_skills,
        soft_skills,
        tools,
        projects,
        other_info
    )

    # Render the summary template with the generated summary
    return render_template('generate_summary.html', summary=summary_text)

def parse_gpt_response(response_text):
    """Parse the structured GPT response and return a dictionary with relevant fields."""
    lines = response_text.split('\n')
    parsed_data = {}
    for line in lines:
        if ": " in line:
            key, value = line.split(": ", 1)
            parsed_data[key.strip()] = value.strip()
    return parsed_data

def store_extracted_info_in_session(parsed_data):
    """Store extracted information in session for later use."""
    session['name'] = parsed_data.get("Name", "N/A")
    session['location'] = parsed_data.get("Location", "N/A")
    session['nationality'] = parsed_data.get("Nationality", "N/A")
    session['useful_links'] = parsed_data.get("Useful Links", "").split(',') if parsed_data.get("Useful Links") else []

    # Job 1 Information
    session['job1'] = {
        "organization": "N/A",
        "job_title": "N/A",
        "start_date": "N/A",
        "end_date": "N/A",
        "responsibilities": []
    }
    if "Job 1" in parsed_data:
        job1_details = parsed_data["Job 1"].split(', ')
        if len(job1_details) >= 3:
            session['job1']['organization'] = job1_details[0]
            session['job1']['job_title'] = job1_details[1]
            session['job1']['start_date'], session['job1']['end_date'] = job1_details[2].split(' - ') if ' - ' in job1_details[2] else ("N/A", "N/A")
        session['job1']['responsibilities'] = parsed_data.get("Responsibilities 1", "").split(', ')

    # Job 2 Information
    session['job2'] = {
        "organization": "N/A",
        "job_title": "N/A",
        "start_date": "N/A",
        "end_date": "N/A",
        "responsibilities": []
    }
    if "Job 2" in parsed_data:
        job2_details = parsed_data["Job 2"].split(', ')
        if len(job2_details) >= 3:
            session['job2']['organization'] = job2_details[0]
            session['job2']['job_title'] = job2_details[1]
            session['job2']['start_date'], session['job2']['end_date'] = job2_details[2].split(' - ') if ' - ' in job2_details[2] else ("N/A", "N/A")
        session['job2']['responsibilities'] = parsed_data.get("Responsibilities 2", "").split(', ')

    session['education'] = parsed_data.get("Education", "").split(', ') if parsed_data.get("Education") else []
    session['hard_skills'] = parsed_data.get("Hard Skills", "").split(', ') if parsed_data.get("Hard Skills") else []
    session['soft_skills'] = parsed_data.get("Soft Skills", "").split(', ') if parsed_data.get("Soft Skills") else []
    session['tools'] = parsed_data.get("Tools", "").split(', ') if parsed_data.get("Tools") else []
    session['projects'] = parsed_data.get("Projects", "").split(', ') if parsed_data.get("Projects") else []
    session['other_info'] = parsed_data.get("Other Relevant Info", "N/A")

if __name__ == "__main__":
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True, port=5001)
