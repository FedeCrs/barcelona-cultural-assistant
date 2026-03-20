# 🎭 Barcelona Cultural Assistant (AI)

AI-powered assistant to discover independent cultural spaces in Barcelona using semantic search and embeddings.

---

## 📌 Overview

Many small cultural venues in Barcelona lack visibility and digital presence.
This project aims to solve that by building an intelligent assistant that allows users to explore cultural spaces through natural language queries.

---

## 🚀 What this project does

* 🔎 Search cultural spaces by name or location (SQL)
* 🧠 Perform semantic search using embeddings
* 💬 Answer user questions using AI (Google Gemini)
* 🔄 Manage cultural data via CRUD operations
* 🌐 Provide a REST API for frontend integration

---

## 🛠️ Tech Stack

* Python (FastAPI)
* MySQL (SQLAlchemy)
* Google Gemini (LLM + embeddings)
* ChromaDB (vector database)
* React (frontend)

---

## 🧠 How it works

1. Cultural data is stored in a relational database
2. Embeddings are generated using Google Gemini
3. Stored in ChromaDB
4. User queries are transformed into embeddings
5. Relevant results are retrieved using semantic similarity

---

## 🚀 Project Status

MVP — backend API implemented, data layer in progress

---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/FedeCrs/barcelona-cultural-assistant.git
cd barcelona-cultural-assistant
```

Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # macOS / Linux
venv\Scripts\activate     # Windows
```

Install dependencies:

```bash
pip install -r app/requirements.txt
```

Set environment variables in a `.env` file:

```env
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/database
GEMINI_API_KEY=your_api_key
```

Initialize the database:

```bash
python -c "from app import models, database; models.Base.metadata.create_all(bind=database.engine)"
```

Run the backend:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Run the frontend:

```bash
npm run dev
```

---

## 🧪 Usage

Test if the API is running:

* GET `/ping`

Main endpoint:

* POST `/api/ask`

Example request:

```json
{
  "message": "Where can I find live music in Barcelona?"
}
```

---

## 📂 Project Structure

* `app/main.py` → API entry point
* `app/chat.py` → semantic + SQL query logic
* `app/crud.py` → database operations
* `app/embeddings.py` → embedding generation
* `app/gemini.py` → Gemini interaction
* `app/database.py` → DB configuration
* `app/models.py` → database models
* `app/schemas.py` → Pydantic schemas
* `frontend/` → React frontend

---

## 🎯 Goal

Support local culture and improve the visibility of small cultural spaces that often lack digital presence.

---

## 👤 Author

Fede Caruso

🔗 LinkedIn: https://linkedin.com/in/fede-caruso

---

⭐ Feel free to explore the project and connect!
