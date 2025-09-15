from flask import Flask, render_template, request, jsonify, send_file
import os
import uuid
import json
from datetime import datetime
from werkzeug.utils import secure_filename
import PyPDF2
import pdfplumber
import docx
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Data storage files
NOTES_FILE = 'data/notes.json'
DOCUMENTS_FILE = 'data/documents.json'
WEB_CLIPS_FILE = 'data/web_clips.json'

# Ensure data directory exists
os.makedirs('data', exist_ok=True)

# Initialize data files if they don't exist
def init_data_files():
    for file_path in [NOTES_FILE, DOCUMENTS_FILE, WEB_CLIPS_FILE]:
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                json.dump([], f)

init_data_files()

# Helper functions to read/write data
def read_json(file_path):
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def write_json(file_path, data):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)

# Text extraction functions
def extract_text_from_pdf(filepath):
    text = ""
    try:
        with pdfplumber.open(filepath) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"
    except:
        # Fallback to PyPDF2 if pdfplumber fails
        try:
            with open(filepath, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    text += page.extract_text() + "\n"
        except:
            text = "Could not extract text from PDF"
    return text

def extract_text_from_docx(filepath):
    try:
        doc = docx.Document(filepath)
        return "\n".join([paragraph.text for paragraph in doc.paragraphs])
    except:
        return "Could not extract text from Word document"

def extract_text_from_txt(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except:
        return "Could not extract text from text file"

# Web content extraction
def extract_web_content(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove unwanted elements
        for element in soup(['script', 'style', 'nav', 'footer', 'header']):
            element.decompose()
            
        # Get title
        title = soup.find('title')
        title_text = title.get_text() if title else url
        
        # Get main content
        main_content = soup.find('main') or soup.find('article') or soup.find('body')
        text = main_content.get_text(separator='\n', strip=True) if main_content else soup.get_text(separator='\n', strip=True)
        
        # Clean up text
        text = re.sub(r'\n\s*\n', '\n\n', text)
        
        return {
            'title': title_text,
            'content': text[:5000]  # Limit content length
        }
    except Exception as e:
        return {
            'title': f"Error fetching {url}",
            'content': f"Could not fetch content: {str(e)}"
        }

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<page>')
def page(page):
    valid_pages = ['notes', 'documents', 'web_clip', 'search', 'ai_query']
    if page in valid_pages:
        return render_template(f'{page}.html')
    return render_template('index.html')

# API Routes
@app.route('/api/notes', methods=['GET', 'POST'])
def handle_notes():
    if request.method == 'GET':
        notes = read_json(NOTES_FILE)
        return jsonify(notes)
    
    elif request.method == 'POST':
        new_note = {
            'id': str(uuid.uuid4()),
            'title': request.json.get('title', 'Untitled Note'),
            'content': request.json.get('content', ''),
            'tags': request.json.get('tags', []),
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        
        notes = read_json(NOTES_FILE)
        notes.append(new_note)
        write_json(NOTES_FILE, notes)
        
        return jsonify(new_note), 201

@app.route('/api/notes/<note_id>', methods=['PUT', 'DELETE'])
def handle_note(note_id):
    notes = read_json(NOTES_FILE)
    
    if request.method == 'PUT':
        for note in notes:
            if note['id'] == note_id:
                note['title'] = request.json.get('title', note['title'])
                note['content'] = request.json.get('content', note['content'])
                note['tags'] = request.json.get('tags', note['tags'])
                note['updated_at'] = datetime.now().isoformat()
                write_json(NOTES_FILE, notes)
                return jsonify(note)
        
        return jsonify({'error': 'Note not found'}), 404
    
    elif request.method == 'DELETE':
        notes = [note for note in notes if note['id'] != note_id]
        write_json(NOTES_FILE, notes)
        return jsonify({'message': 'Note deleted'})

@app.route('/api/documents', methods=['GET', 'POST'])
def handle_documents():
    if request.method == 'GET':
        documents = read_json(DOCUMENTS_FILE)
        return jsonify(documents)
    
    elif request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if file:
            # Save the file
            filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4().hex}_{filename}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(filepath)
            
            # Extract text based on file type
            text_content = ""
            if filename.lower().endswith('.pdf'):
                text_content = extract_text_from_pdf(filepath)
            elif filename.lower().endswith(('.doc', '.docx')):
                text_content = extract_text_from_docx(filepath)
            elif filename.lower().endswith('.txt'):
                text_content = extract_text_from_txt(filepath)
            
            # Create document record
            new_doc = {
                'id': str(uuid.uuid4()),
                'filename': unique_filename,
                'original_name': filename,
                'text_content': text_content,
                'tags': request.form.getlist('tags[]'),
                'uploaded_at': datetime.now().isoformat()
            }
            
            documents = read_json(DOCUMENTS_FILE)
            documents.append(new_doc)
            write_json(DOCUMENTS_FILE, documents)
            
            return jsonify(new_doc), 201

@app.route('/api/documents/<doc_id>', methods=['DELETE'])
def handle_document(doc_id):
    documents = read_json(DOCUMENTS_FILE)
    
    for doc in documents:
        if doc['id'] == doc_id:
            # Remove the file
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], doc['filename'])
            if os.path.exists(filepath):
                os.remove(filepath)
            
            # Remove from documents list
            documents = [d for d in documents if d['id'] != doc_id]
            write_json(DOCUMENTS_FILE, documents)
            
            return jsonify({'message': 'Document deleted'})
    
    return jsonify({'error': 'Document not found'}), 404

@app.route('/api/web_clips', methods=['GET', 'POST'])
def handle_web_clips():
    if request.method == 'GET':
        web_clips = read_json(WEB_CLIPS_FILE)
        return jsonify(web_clips)
    
    elif request.method == 'POST':
        url = request.json.get('url', '')
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        # Extract web content
        content = extract_web_content(url)
        
        new_clip = {
            'id': str(uuid.uuid4()),
            'url': url,
            'title': content['title'],
            'content': content['content'],
            'tags': request.json.get('tags', []),
            'clipped_at': datetime.now().isoformat()
        }
        
        web_clips = read_json(WEB_CLIPS_FILE)
        web_clips.append(new_clip)
        write_json(WEB_CLIPS_FILE, web_clips)
        
        return jsonify(new_clip), 201

@app.route('/api/web_clips/<clip_id>', methods=['DELETE'])
def handle_web_clip(clip_id):
    web_clips = read_json(WEB_CLIPS_FILE)
    web_clips = [clip for clip in web_clips if clip['id'] != clip_id]
    write_json(WEB_CLIPS_FILE, web_clips)
    return jsonify({'message': 'Web clip deleted'})

@app.route('/api/search')
def search():
    query = request.args.get('q', '').lower()
    
    if not query:
        return jsonify({'error': 'Query parameter is required'}), 400
    
    results = []
    
    # Search in notes
    notes = read_json(NOTES_FILE)
    for note in notes:
        if (query in note['title'].lower() or 
            query in note['content'].lower() or 
            any(query in tag.lower() for tag in note['tags'])):
            results.append({
                'type': 'note',
                'data': note
            })
    
    # Search in documents
    documents = read_json(DOCUMENTS_FILE)
    for doc in documents:
        if (query in doc['original_name'].lower() or 
            query in doc['text_content'].lower() or 
            any(query in tag.lower() for tag in doc['tags'])):
            results.append({
                'type': 'document',
                'data': doc
            })
    
    # Search in web clips
    web_clips = read_json(WEB_CLIPS_FILE)
    for clip in web_clips:
        if (query in clip['title'].lower() or 
            query in clip['content'].lower() or 
            query in clip['url'].lower() or 
            any(query in tag.lower() for tag in clip['tags'])):
            results.append({
                'type': 'web_clip',
                'data': clip
            })
    
    return jsonify(results)

@app.route('/api/ai_query', methods=['POST'])
def ai_query():
    question = request.json.get('question', '')
    
    if not question:
        return jsonify({'error': 'Question is required'}), 400
    
    # Get all knowledge data
    notes = read_json(NOTES_FILE)
    documents = read_json(DOCUMENTS_FILE)
    web_clips = read_json(WEB_CLIPS_FILE)
    
    # Simple keyword matching for demo purposes
    # In a real application, you would use more sophisticated NLP techniques
    relevant_items = []
    
    # Check notes
    for note in notes:
        if any(word.lower() in note['content'].lower() for word in question.split()):
            relevant_items.append({
                'type': 'note',
                'data': note
            })
    
    # Check documents
    for doc in documents:
        if any(word.lower() in doc['text_content'].lower() for word in question.split()):
            relevant_items.append({
                'type': 'document',
                'data': doc
            })
    
    # Check web clips
    for clip in web_clips:
        if any(word.lower() in clip['content'].lower() for word in question.split()):
            relevant_items.append({
                'type': 'web_clip',
                'data': clip
            })
    
    # Generate response based on relevant items
    if relevant_items:
        response_text = f"I found {len(relevant_items)} items relevant to your question: '{question}'.\n\n"
        
        for i, item in enumerate(relevant_items[:3], 1):  # Limit to 3 items
            if item['type'] == 'note':
                preview = item['data']['content'][:100] + '...' if len(item['data']['content']) > 100 else item['data']['content']
                response_text += f"{i}. Note: {item['data']['title']} - {preview}\n"
            elif item['type'] == 'document':
                response_text += f"{i}. Document: {item['data']['original_name']}\n"
            elif item['type'] == 'web_clip':
                response_text += f"{i}. Web Clip: {item['data']['title']} ({item['data']['url']})\n"
    else:
        response_text = f"I couldn't find any information related to your question: '{question}'. Try adding more notes, documents, or web clips on this topic."
    
    return jsonify({
        'question': question,
        'response': response_text,
        'sources': relevant_items[:3]  # Return top 3 sources
    })

if __name__ == '__main__':
    app.run(debug=True)