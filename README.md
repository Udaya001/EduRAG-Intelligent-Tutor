# EduRAG: Intelligent Tutor Using RAG and LangChain

##  Overview

EduRAG is an AI-powered intelligent tutoring system that leverages Retrieval-Augmented Generation (RAG), Large Language Model APIs, LangChain, and PostgreSQL to deliver smart, context-aware educational responses. Designed for flexibility and efficiency, EduRAG combines dynamic language workflows with scalable data retrieval mechanisms.

##  Features

* Retrieval-Augmented Generation (RAG) for accurate, context-aware answers
* LangChain integration for dynamic and modular LLM workflows
* PostgreSQL + pgvector for fast, vector-based document retrieval
* FastAPI backend for scalable and simple API interaction
* Nginx-based deployment support for local hosting

##  Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/Udaya001/EduRAG-Intelligent-Tutor.git
cd EduRAG-Intelligent-Tutor
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

```bash
cp .env.example .env
# Then update .env with your keys and config
```

### 4. Run the Server

```bash
uvicorn main:app --reload
```

##  Deployment with Nginx (Local)

### 1. Install Nginx

* Download and unzip [Nginx for Windows](https://nginx.org/en/download.html).

### 2. Replace Nginx Configuration

* Replace `nginx/conf/nginx.conf` in the Nginx folder with the provided `nginx/nginx.conf` from this repo.

### 3. Setup Frontend (Optional)

* Copy your frontend files (e.g., `index.html`, `styles.css`, etc.) to:

```bash
C:\nginx\html\
```

### 4. Run FastAPI Server

```bash
uvicorn main:app --host 127.0.0.1 --port 8000
```

### 5. Start or Reload Nginx

```bash
cd C:\nginx
start nginx
nginx -s reload
```

### 6. Test Application

Visit [http://localhost](http://localhost) in your browser to ensure everything is running.

---
