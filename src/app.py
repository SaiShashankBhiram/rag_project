from fastapi import FastAPI, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.rag_project.components.model_trainer import query_rag

app = FastAPI()

# Enable CORS to allow browser-based requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust if needed
    allow_credentials=True,
    allow_methods=["*"],  # Allow GET, POST, etc.
    allow_headers=["*"],  # Allow all headers
)

# Default top_k value
TOP_K = 3  # 👈 You can change this globally

# Input schema for JSON requests
class QueryRequest(BaseModel):
    question: str

# Health check
@app.get("/")
def health_check():
    return {"status": "✅ API is up and running"}

# Main query endpoint (JSON-based requests)
@app.post("/query-json")
def run_query_json(request: QueryRequest):
    try:
        result = query_rag(request.question, top_k=TOP_K)
        return {"response": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# New endpoint for handling form submissions
@app.post("/query")
def run_query_form(question: str = Form(...)):
    try:
        result = query_rag(question, top_k=TOP_K)
        return {"response": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))