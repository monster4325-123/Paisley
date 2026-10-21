from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import protein, mutation

app = FastAPI(
    title="Paisley API",
    description="Backend API for Paisley: Explainable AI Platform for Protein Structure Prediction and Mutation Analysis",
    version="1.0.0"
)

# Allow frontend (React/Vite) to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(protein.router)
app.include_router(mutation.router)


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