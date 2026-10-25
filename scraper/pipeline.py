import logging
from config.database import SessionLocal
from models.data_models import ScrapedItem
from scraper.parser import fetch_html, parse_items, BASE_URL

logger = logging.getLogger(__name__)

def run_pipeline():
    """Executes the full extraction, transformation, and load (ETL) process."""
    logger.info("Starting pipeline execution...")
    
    # 1. Fetch & Parse
    html = fetch_html(BASE_URL)
    items = parse_items(html)

    if not items:
        logger.warning("No items retrieved. Exiting pipeline.")
        return

    # 2. Save to Database
    db = SessionLocal()
    new_records_count = 0

    try:
        for item in items:
            # Check if URL already exists to prevent duplicate entries
            existing = db.query(ScrapedItem).filter(ScrapedItem.url == item["url"]).first()
            if not existing:
                db_item = ScrapedItem(
                    title=item["title"],
                    company_or_source=item["company_or_source"],
                    location=item["location"],
                    url=item["url"],
                    description=item["description"]
                )
                db.add(db_item)
                new_records_count += 1

        db.commit()
        logger.info(f"Pipeline finished! Saved {new_records_count} new records to the database.")
    except Exception as e:
        db.rollback()
        logger.error(f"Error during database transaction: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    run_pipeline()
