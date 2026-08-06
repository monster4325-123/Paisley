from fastapi import FastAPI
from app.routes import protein

app = FastAPI(
    title="Paisley API",
    description="Backend API for Paisley: Explainable AI Platform for Protein Structure Prediction and Mutation Analysis",
    version="1.0.0"
)
app.include_router(protein.router)

@app.get("/")
def root():
    return {
        "message": "Welcome to Paisley API 🚀"
    }

@app.get("/health")
def health():
    return {
        "status": "Backend is running successfully"
    }