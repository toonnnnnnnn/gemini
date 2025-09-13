from fasthtml.common import *
from pathlib import Path
import tempfile
import os
import base64
from google.genai import types
import google.genai as genai

# Configure the Gemini API
genai.configure(api_key="AIzaSyB-xxx-k")

# Create the FastHTML app
app = FastHTML()

# Configure upload settings
UPLOAD_FOLDER = Path("uploads")
UPLOAD_FOLDER.mkdir(exist_ok=True)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_with_ocr(file_path, file_type):
    """Process file with Google Gemini OCR"""
    try:
        # Read the file as base64
        with open(file_path, 'rb') as f:
            file_data = f.read()
        
        # Convert to base64
        file_base64 = base64.b64encode(file_data).decode('utf-8')
        
        # Create the content for Gemini
        if file_type == 'pdf':
            content = types.Content(
                parts=[
                    types.Part(
                        inline_data=types.InlineData(
                            mime_type="application/pdf",
                            data=file_base64
                        )
                    )
                ]
            )
        else:
            content = types.Content(
                parts=[
                    types.Part(
                        inline_data=types.InlineData(
                            mime_type=f"image/{file_type}",
                            data=file_base64
                        )
                    )
                ]
            )
        
        # Generate content with OCR
        response = genai.GenerativeModel('gemini-1.5-flash').generate_content(
            [content, "Extract all text from this document/image. Provide the text in a clear, readable format."]
        )
        
        return response.text
        
    except Exception as e:
        return f"Error processing file: {str(e)}"

@app.route("/")
def home():
    return Html(
        Head(
            Title("OCR Web Application"),
            Link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css")
        ),
        Body(
            Div(
                H1("OCR Document Reader", class_="text-center mb-4"),
                Div(
                    Form(
                        Div(
                            Label("Upload Image or PDF:", class_="form-label"),
                            Input(type="file", name="file", class="form-control", accept=".png,.jpg,.jpeg,.gif,.pdf", required=True),
                            class_="mb-3"
                        ),
                        Button("Process OCR", type="submit", class_="btn btn-primary"),
                        action="/upload",
                        method="post",
                        enctype="multipart/form-data"
                    ),
                    class_="card p-4"
                ),
                class_="container mt-5"
            ),
            Script(src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js")
        )
    )

@app.route("/upload", methods=["POST"])
def upload_file():
    try:
        # Get the uploaded file
        file = request.files.get('file')
        
        if not file or file.filename == '':
            return redirect('/?error=No file selected')
        
        if not allowed_file(file.filename):
            return redirect('/?error=Invalid file type')
        
        # Save the file temporarily
        filename = file.filename
        file_path = UPLOAD_FOLDER / filename
        file.save(file_path)
        
        # Get file extension for MIME type
        file_ext = filename.rsplit('.', 1)[1].lower()
        
        # Process with OCR
        ocr_result = process_with_ocr(file_path, file_ext)
        
        # Clean up the uploaded file
        os.remove(file_path)
        
        # Display results
        return Html(
            Head(
                Title("OCR Results"),
                Link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css")
            ),
            Body(
                Div(
                    H1("OCR Results", class_="text-center mb-4"),
                    Div(
                        H3("Original File:", class_="mb-2"),
                        P(filename, class_="text-muted"),
                        class_="mb-3"
                    ),
                    Div(
                        H3("Extracted Text:", class_="mb-2"),
                        Div(
                            P(ocr_result, class_="bg-light p-3 rounded", style="white-space: pre-wrap;"),
                            class_="border rounded"
                        ),
                        class_="mb-4"
                    ),
                    A("Upload Another File", href="/", class_="btn btn-primary"),
                    class_="container mt-5"
                ),
                Script(src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js")
            )
        )
        
    except Exception as e:
        return redirect(f'/?error={str(e)}')

@app.route("/health")
def health():
    return {"status": "healthy", "message": "OCR service is running"}

if __name__ == "__main__":
    # Run on port 5001 as specified in the FastHTML documentation
    serve(port=5001)
