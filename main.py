import time
import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from models.data_models import init_db
from scraper.pipeline import run_pipeline

# Configure logging format to monitor pipeline runs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def job():
    """Wrapper function to execute the pipeline from the scheduler."""
    logger.info("Scheduler triggered pipeline execution.")
    run_pipeline()

if __name__ == "__main__":
    logger.info("Initializing database tables...")
    init_db()

    # Initialize the Blocking Scheduler
    scheduler = BlockingScheduler()

    # Schedule the pipeline to run every 1 minute (for testing purposes)
    # You can change this to hours=2, days=1, etc., for production use.
    scheduler.add_job(job, 'interval', minutes=1, id='scraping_job')

    logger.info("Scheduler started. Press Ctrl+C to exit.")
    
    # Run an initial execution immediately on startup
    job()

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Scheduler stopped by user.")
