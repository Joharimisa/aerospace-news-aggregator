from app import create_app
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = create_app()

if __name__ == '__main__':
    # For development, run with scheduler
    from apscheduler.schedulers.background import BackgroundScheduler
    from apscheduler.triggers.interval import IntervalTrigger
    from scrapers.rss_scraper import scrape_all_sources
    import atexit
    
    logger.info("Starting Aerospace News Aggregator (development mode)...")
    
    with app.app_context():
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
        
        # Shut down the scheduler when exiting the app
        atexit.register(lambda: scheduler.shutdown())
    
    # Run Flask app
    app.run(host='0.0.0.0', port=5000, debug=True)
