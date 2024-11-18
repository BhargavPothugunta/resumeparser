import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from parser import parse_resume
from utils import allowed_file

app = Flask(__name__)

# Set the upload folder path (absolute or relative)
UPLOAD_FOLDER = 'uploads'  # This can be a relative or absolute path
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Optionally, you can limit the size of the uploaded file (e.g., 16 MB)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

# Create the upload folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Define the route for the homepage (index.html)
@app.route('/')
def index():
    return render_template('index.html')

# Define the route for handling the file upload
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return render_template('index.html', error="No file part")

    file = request.files['file']

    if file.filename == '':
        return render_template('index.html', error="No selected file")

    if not allowed_file(file.filename):
        return render_template('index.html', error="Invalid file type. Only PDF and DOCX are allowed.")

    # Secure the filename and save the file
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    try:
        # Parse the uploaded resume
        resume_data = parse_resume(file_path, file.filename.split('.')[-1])

        # Ensure that resume_data is not None or empty
        if not resume_data:
            return render_template('index.html', error="Error processing the resume. Please try again.")

        # Render the result page with parsed resume information
        return render_template('result.html', resume_data=resume_data)

    except Exception as e:
        # Handle any exceptions that occur during parsing
        return render_template('index.html', error=f"Error processing the file: {str(e)}")

# Start the Flask app
if __name__ == '__main__':
    app.run(debug=True)
