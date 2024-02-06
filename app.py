import os

from flask import Flask, flash, redirect, render_template, request, session, url_for
from werkzeug.utils import secure_filename

from resume_parser import extract_information, extract_text_from_docx, extract_text_from_pdf
from summary_generator import generate_summary

app = Flask(__name__)

# Configure the upload folder and allowed extensions
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB upload limit
app.config['SECRET_KEY'] = 'your_secret_key'  # Needed for session management


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
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

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    # Process the file based on its extension
    if filename.endswith('.pdf'):
        text = extract_text_from_pdf(filepath)
    elif filename.endswith('.docx'):
        text = extract_text_from_docx(filepath)
    else:
        text = "Unsupported file format."

    if text != "Unsupported file format.":
        name, organization, education = extract_information(text)
        # Store extracted info in session for use in the summary generation
        session['name'] = name
        session['organization'] = organization
        session['education'] = education
    else:
        flash('Failed to extract information from the uploaded file.')

    # Optionally, delete the file after processing
    os.remove(filepath)

    # Redirect to the extracted information page for review and corrections
    return render_template('extracted_info.html', name=name, organization=organization, education=education)


@app.route('/generate_summary', methods=['POST'])
def generate_summary_route():
    # Retrieve corrected information from form submission
    name = request.form['name']
    organization = request.form.get('organization', '')
    education = request.form.get('education', '').split(',')

    # Use the summarizer to generate a summary
    summary_text = generate_summary(name, organization, education)

    # Render the summary template with the generated summary
    return render_template('generate_summary.html', summary=summary_text)


if __name__ == "__main__":
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True, port=5001)  # Change the port to a different number
