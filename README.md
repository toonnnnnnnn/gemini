# OCR Web Application

A web application built with FastHTML and Google GenAI for OCR (Optical Character Recognition) from uploaded images and PDF files.

## Features

- Upload images (PNG, JPG, JPEG, GIF) and PDF files
- Extract text using Google Gemini AI OCR capabilities
- Clean, responsive web interface built with Bootstrap
- Docker support for easy deployment

## Requirements

- Python 3.11+
- Google GenAI API key (configured in app.py)
- Docker (optional, for containerized deployment)

## Installation

### Local Development

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Update the API key in `app.py` (replace "AIzaSyB-xxx-k" with your actual Google GenAI API key)
4. Run the application:
   ```bash
   python app.py
   ```
5. Open your browser to `http://localhost:8001`

### Docker Deployment

1. Build the Docker image:
   ```bash
   docker build -t ocr-app .
   ```
2. Run the container:
   ```bash
   docker run -p 8001:8001 ocr-app
   ```
3. Open your browser to `http://localhost:8001`

## API Endpoints

- `GET /` - Main upload page
- `POST /upload` - Upload and process files for OCR
- `GET /health` - Health check endpoint

## Usage

1. Navigate to the web application
2. Select an image or PDF file using the file input
3. Click "Process OCR" to extract text
4. View the extracted text results
5. Upload another file or start over

## Configuration

The application uses port 8001 as specified in the FastHTML documentation. The Google GenAI API key should be configured in the `app.py` file.

## Dependencies

- FastHTML: Web framework
- Google GenAI: AI/OCR processing
- Python-multipart: File upload handling
- Pathlib2: File path utilities

## Docker Details

The Dockerfile uses:
- Debian-based Python 3.11 image
- libxrender1 system dependency (as specified)
- Port 8001 exposure
- Optimized layer caching for requirements
