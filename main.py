import os
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from database import db, create_document, get_documents
from schemas import Profile as ProfileSchema, Project as ProjectSchema

app = FastAPI(title="Portfolio API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Helper to get collection names from schema class name

def collection_name(model_cls: type) -> str:
    return model_cls.__name__.lower()

# Public endpoints (read-only)

class ProfileOut(BaseModel):
    name: str
    title: str
    summary: str
    location: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    github: Optional[str] = None
    linkedin: Optional[str] = None
    skills: List[str] = []

class ProjectOut(BaseModel):
    title: str
    description: str
    purpose: Optional[str] = None
    languages: List[str] = []
    frameworks: List[str] = []
    timeframe: Optional[str] = None
    repo_url: Optional[str] = None
    live_url: Optional[str] = None
    highlights: List[str] = []

@app.get("/")
def root():
    return {"message": "Portfolio backend running"}

@app.get("/api/profile", response_model=Optional[ProfileOut])
def get_profile():
    if db is None:
        return None
    docs = get_documents(collection_name(ProfileSchema), limit=1)
    if not docs:
        return None
    doc = docs[0]
    # Remove Mongo _id
    doc.pop("_id", None)
    return ProfileOut(**doc)

@app.get("/api/projects", response_model=List[ProjectOut])
def list_projects():
    if db is None:
        return []
    docs = get_documents(collection_name(ProjectSchema))
    for d in docs:
        d.pop("_id", None)
    return [ProjectOut(**d) for d in docs]

# Simple owner-side endpoints to create content (no auth for demo; can add later)
@app.post("/api/profile", response_model=str)
def create_profile(profile: ProfileSchema):
    cid = create_document(collection_name(ProfileSchema), profile)
    return cid

@app.post("/api/projects", response_model=str)
def create_project(project: ProjectSchema):
    cid = create_document(collection_name(ProjectSchema), project)
    return cid

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available" if db is None else "✅ Connected",
        "database_url": "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set",
        "database_name": "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set",
    }
    try:
        if db is not None:
            response["collections"] = db.list_collection_names()
    except Exception as e:
        response["database"] = f"⚠️ Error: {str(e)[:80]}"
    return response

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
