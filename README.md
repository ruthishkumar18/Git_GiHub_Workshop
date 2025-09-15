# AI-Powered Personal Knowledge Assistant

A comprehensive Flask-based web application that helps you capture,
organize, and retrieve information from various sources using AI-powered
capabilities.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Flask-2.3.3-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🌟 Features

### 📝 Note-Taking System

-   Create and manage rich text notes
-   Organize notes with custom tags
-   Edit and delete existing notes
-   Clean, responsive interface for note management

### 📄 Document Management

-   Upload PDF, Word (.doc, .docx), and text files
-   Automatic text extraction from uploaded documents
-   Document metadata storage and organization
-   Tag-based categorization of documents

### 🌐 Web Content Clipping

-   Save web content by providing URLs
-   Automatic content extraction from web pages
-   Title and content preservation
-   Tagging system for web clips

### 🔍 Advanced Search

-   Full-text search across all content types
-   Tag-based filtering and search
-   Unified search results interface
-   Real-time search functionality

### 🤖 AI-Powered Query System

-   Natural language queries about your knowledge base
-   AI-generated responses based on your content
-   Source attribution for AI responses
-   Intelligent content analysis

## 🚀 Installation

### Prerequisites

-   Python 3.8 or higher
-   pip (Python package manager)
-   Git

### Step-by-Step Setup

1.  **Clone the Repository**

    ``` bash
    git clone https://github.com/ruthishkumar18/Git_GiHub_Workshop.git
    cd Git_GiHub_Workshop
    ```

2.  **Create a Virtual Environment**

    ``` bash
    # On Windows
    python -m venv venv
    venv\Scripts\activate

    # On macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Dependencies**

    ``` bash
    pip install -r requirements.txt
    ```

4.  **Run the Application**

    ``` bash
    python app.py
    ```

5.  **Access the Application** Open your web browser and navigate to:

    ``` text
    http://localhost:5000
    ```

## 📁 Project Structure

    Git_GiHub_Workshop/
    │
    ├── app.py                 # Main Flask application
    ├── requirements.txt       # Python dependencies
    ├── README.md              # Project documentation
    │
    ├── data/                  # JSON data storage
    │   ├── notes.json         # User notes
    │   ├── documents.json     # Document metadata
    │   └── web_clips.json     # Web clip content
    │
    ├── static/                # Static files
    │   └── uploads/           # Uploaded document storage
    │
    └── templates/             # HTML templates
        ├── base.html          # Base template with common elements
        ├── index.html         # Home page
        ├── notes.html         # Notes management interface
        ├── documents.html     # Document upload and management
        ├── web_clip.html      # Web content clipping interface
        ├── search.html        # Search functionality
        └── ai_query.html      # AI query interface

## 🛠️ Technology Stack

### Backend

-   Flask: Lightweight web framework
-   PyPDF2 & pdfplumber: PDF text extraction
-   python-docx: Word document processing
-   BeautifulSoup4: Web scraping and content extraction
-   Requests: HTTP requests for web content

### Frontend

-   HTML5: Page structure
-   CSS3: Styling and responsive design
-   JavaScript: Interactive functionality
-   Modern CSS Features: Flexbox, Grid, Variables

### Data Storage

-   JSON files: Simple, file-based data storage
-   File system: Document storage in uploads directory

## 📋 API Endpoints

  Method   Endpoint                       Description
  -------- ------------------------------ ----------------------------
  GET      /api/notes                     Retrieve all notes
  POST     /api/notes                     Create a new note
  PUT      /api/notes/`<id>`{=html}       Update a specific note
  DELETE   /api/notes/`<id>`{=html}       Delete a specific note
  GET      /api/documents                 Retrieve all documents
  POST     /api/documents                 Upload a new document
  DELETE   /api/documents/`<id>`{=html}   Delete a specific document
  GET      /api/web_clips                 Retrieve all web clips
  POST     /api/web_clips                 Create a new web clip
  DELETE   /api/web_clips/`<id>`{=html}   Delete a specific web clip
  GET      /api/search                    Search across all content
  POST     /api/ai_query                  Process AI-powered queries

## 🎯 Usage Guide

### Creating Notes

1.  Navigate to the "Notes" tab
2.  Enter a title for your note (optional)
3.  Type your content in the text area
4.  Add comma-separated tags for organization
5.  Click "Save Note" to store your content

### Uploading Documents

1.  Go to the "Documents" tab
2.  Drag and drop files or click to browse
3.  Add relevant tags for the document
4.  The system will automatically extract text content
5.  View your uploaded documents in the list below

### Clipping Web Content

1.  Access the "Web Clipper" tab
2.  Enter the URL of the webpage you want to save
3.  Add appropriate tags for organization
4.  Click "Clip Content" to save the webpage
5.  View your clipped content in the list below

### Searching Your Knowledge Base

1.  Go to the "Search" tab
2.  Enter keywords or tags in the search box
3.  Press Enter or click "Search"
4.  View results from notes, documents, and web clips
5.  Results are categorized by content type

### Using AI Queries

1.  Navigate to the "AI Query" tab
2.  Ask a natural language question about your content
3.  Click "Ask AI" to get a response
4.  The AI will analyze your knowledge base and provide answers
5.  View the sources used for the response
