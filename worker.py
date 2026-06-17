"""
Worker process for running the background scheduler in production.
This can be run as a separate process on Render/Railway.
"""
from app import create_app
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import logging
from scrapers.rss_scraper import scrape_all_sources

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = create_app()

def start_scheduler():
    """Start the background scheduler for periodic scraping"""
    scheduler = BackgroundScheduler()
    
    # Get scrape interval from config
    interval_minutes = app.config.get('SCRAPE_INTERVAL_MINUTES', 30)
    
    # Schedule scraping job
    scheduler.add_job(
        func=scrape_all_sources,
        trigger=IntervalTrigger(minutes=interval_minutes),
        id='scrape_articles',
        name='Scrape aerospace news articles',
        replace_existing=True
    )
    
    scheduler.start()
    logger.info(f"Scheduler started. Scraping every {interval_minutes} minutes.")
    
    # Run initial scrape
    logger.info("Running initial scrape...")
    scrape_all_sources()
    
    # Keep the process running
    try:
        while True:
            import time
            time.sleep(60)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        logger.info("Scheduler shutdown.")

if __name__ == '__main__':
    with app.app_context():
        start_scheduler()
