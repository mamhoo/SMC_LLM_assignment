## Features
- User authentication (JWT)
- SQL Agent for structured financial data (numbers, net income, growth)
- Pinecone RAG for 10-K qualitative/strategy questions
- No hallucination (grounded answers)
- LangGraph dynamic routing
- Docker Compose for local Postgres + Pinecone

# 1. Start databases
- docker compose up -d

# 2. Install dependencies
- cd backend
- pip install -r app/requirements.txt

# 3. Load data (only once on new PC)
- cd ..
- python scripts/load_sql.py
- python scripts/load_pinecone.py

# 4. Run backend
- cd backend
- uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 5. Run frontend (new terminal):
- cd frontend
- pip install streamlit requests
- streamlit run app.py
