from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import List
from pydantic import BaseModel
from datetime import datetime

# --- DATABASE CONFIGURATION ---
# Replace 'your_password' with your actual PostgreSQL password
DATABASE_URL = (
    "postgresql+psycopg2://postgres:6364@localhost:5432/pipeline_db"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define the ScrapedItem model to match your database table
class ScrapedItem(Base):
    __tablename__ = "scraped_items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    company_or_source = Column(String(255))
    location = Column(String(255))
    url = Column(Text, nullable=False, unique=True)
    description = Column(Text)
    created_at = Column(DateTime)

# --- FASTAPI APP ---
app = FastAPI(title="Python Data Pipeline API")

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic Schema for Response Validation
class ScrapedItemSchema(BaseModel):
    id: int
    title: str
    company_or_source: str | None = None
    location: str | None = None
    url: str
    description: str | None = None
    created_at: datetime | None = None

    class Config:
        from_attributes = True

# --- API ENDPOINTS ---
@app.get("/")
def root():
    return {"status": "ok", "message": "Pipeline API is running smoothly"}

@app.get("/api/items", response_model=List[ScrapedItemSchema])
def get_scraped_items(limit: int = 100, db: Session = Depends(get_db)):
    """Fetch all scraped items from pipeline_db."""
    items = db.query(ScrapedItem).order_by(ScrapedItem.id.desc()).limit(limit).all()
    return items

@app.get("/api/stats")
def get_pipeline_stats(db: Session = Depends(get_db)):
    """Get summary statistics for dashboard key cards."""
    total_count = db.query(ScrapedItem).count()
    return {
        "total_items": total_count,
        "database": "pipeline_db",
        "table": "scraped_items"
    }