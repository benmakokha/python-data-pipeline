from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Float
from config.database import Base, engine

class ScrapedItem(Base):
    """
    ORM Model representing a scraped job posting or product listing.
    """
    __tablename__ = "scraped_items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    company_or_source = Column(String(255), nullable=True)
    location = Column(String(255), nullable=True)
    url = Column(Text, unique=True, nullable=False)  # Unique to prevent duplicate entries
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

def init_db():
    """Creates the database tables based on defined models."""
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
    print("Database tables created successfully!")
