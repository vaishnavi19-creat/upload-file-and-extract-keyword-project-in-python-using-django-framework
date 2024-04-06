from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename
import os
from langdetect import detect
import PyPDF2
from gensim.summarization import summarize
from gensim.summarization import keywords

app = Flask(__name__)

# Define the directory where uploaded files will be stored
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Route for the home page
@app.route('/')
def home():
    return render_template('index.html', summary='', keywords=[])

# Route to handle file upload
@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'pdf_file' not in request.files:
            return redirect(request.url)

        file = request.files['pdf_file']

        # If the user does not select a file, the browser submits an empty file without a filename
        if file.filename == '':
            return redirect(request.url)

        # If the file is provided and has a filename
        if file:
            # Ensure the filename is secure to prevent directory traversal attacks
            filename = secure_filename(file.filename)

            # Save the file to the upload folder
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Extract text from the PDF file
            text = extract_text_from_pdf(file_path)

            # Extract summary and keywords from the text
            summary = summarize(text)
            keywords_list = keywords(text).split('\n')

            # Pass summary and keywords to the template
            return render_template('index.html', summary=summary, keywords=keywords_list)

def extract_text_from_pdf(pdf_file_path):
    # Function to extract text from PDF file using PyPDF2
    text = ''
    with open(pdf_file_path, 'rb') as f:
        reader = PyPDF2.PdfFileReader(f)
        for page_num in range(reader.numPages):
            text += reader.getPage(page_num).extractText()
    return text

if __name__ == '__main__':
    app.run(debug=True)
