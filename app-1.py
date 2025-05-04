from flask import Flask, request, render_template_string
import pytesseract
import fitz  # PyMuPDF
from PIL import Image
import io
import os
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


from analyzer import analyze_report  # Make sure analyzer.py exists with analyze_report()

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Uncomment below if Tesseract is installed in a non-default location (Windows users)
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    full_text = ""
    for page in doc:
        pix = page.get_pixmap()
        img = Image.open(io.BytesIO(pix.tobytes("png")))
        text = pytesseract.image_to_string(img)
        full_text += text + "\n"
    return full_text

@app.route('/', methods=['GET', 'POST'])
def index():
    analysis_result = None
    if request.method == 'POST':
        file = request.files['pdf']
        if file:
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)

            extracted_text = extract_text_from_pdf(filepath)
            analysis_result = analyze_report(extracted_text)

    return render_template_string("""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Report Analyzer | AI Healthmate+</title>
  <style>
    body {
      font-family: 'Segoe UI', sans-serif;
      background: #f0f4f8;
      margin: 0;
      padding: 0;
    }

    .container {
      max-width: 800px;
      margin: 60px auto;
      padding: 30px;
      background: #fff;
      border-radius: 12px;
      box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
    }

    h1 {
      text-align: center;
      color: #004080;
      margin-bottom: 20px;
    }

    form {
      text-align: center;
      margin-bottom: 30px;
    }

    input[type="file"] {
      padding: 10px;
      margin-bottom: 20px;
      border: 2px dashed #004080;
      border-radius: 6px;
      cursor: pointer;
    }

    button {
      background-color: #004080;
      color: white;
      padding: 10px 25px;
      border: none;
      border-radius: 6px;
      font-size: 16px;
      cursor: pointer;
      transition: background 0.3s;
    }

    button:hover {
      background-color: #002f66;
    }

    .result {
      margin-top: 30px;
      background: #f9f9f9;
      padding: 20px;
      border-left: 4px solid #004080;
      white-space: pre-wrap;
      font-size: 15px;
      color: #333;
      border-radius: 6px;
    }

    .footer {
      text-align: center;
      margin-top: 50px;
      font-size: 13px;
      color: #777;
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>🩺 Report Analyzer</h1>
    <form method="post" enctype="multipart/form-data">
      <input type="file" name="pdf" accept=".pdf" required>
      <br>
      <button type="submit">Analyze Report</button>
    </form>

    {% if analysis_result %}
    <div class="result">
      <strong>🔍 Analysis Result:</strong><br>
      {{ analysis_result }}
    </div>
    {% endif %}
  </div>

  <div class="footer">AI Healthmate+ &copy; 2025 | Powered by Flask & Tesseract OCR</div>
</body>
</html>
""", analysis_result=analysis_result)

if __name__ == '__main__':
    app.run(host='127.0.0.2', port=3000, debug=True)
