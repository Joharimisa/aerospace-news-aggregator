import feedparser
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import logging
from app.models import Article, db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# RSS Feed URLs for aerospace sources
RSS_SOURCES = {
    'Reuters': {
        'url': 'https://www.reuters.com/news/archive/aerospace-and-defense?view=rss',
        'category': 'Defense/Military'
    },
    'FlightGlobal': {
        'url': 'https://www.flightglobal.com/rss',
        'category': 'Commercial Aviation'
    },
    'SpaceNews': {
        'url': 'https://spacenews.com/feed/',
        'category': 'Space Exploration'
    },
    'Aviation Week': {
        'url': 'https://aviationweek.com/rss.xml',
        'category': 'Commercial Aviation'
    }
}

# Fallback sources if RSS feeds are not available
FALLBACK_SOURCES = {
    'Air & Cosmos': {
        'url': 'https://www.aircosmos.com/en/feed/',
        'category': 'General'
    }
}

def clean_summary(summary):
    """Clean HTML tags from summary"""
    if not summary:
        return ""
    soup = BeautifulSoup(summary, 'html.parser')
    text = soup.get_text()
    return ' '.join(text.split())[:500]  # Limit to 500 chars

def extract_image_url(entry, source_name):
    """Extract image URL from RSS entry"""
    # Try different common image fields
    if hasattr(entry, 'enclosures') and entry.enclosures:
        return entry.enclosures[0].get('href', '')
    
    if hasattr(entry, 'media_content') and entry.media_content:
        return entry.media_content[0].get('url', '')
    
    # Try to extract from summary HTML
    if hasattr(entry, 'summary'):
        soup = BeautifulSoup(entry.summary, 'html.parser')
        img = soup.find('img')
        if img and img.get('src'):
            return img['src']
    
    return ''

def categorize_article(title, summary, default_category):
    """Categorize article based on keywords"""
    title_lower = title.lower()
    summary_lower = summary.lower() if summary else ""
    text = title_lower + " " + summary_lower
    
    categories = {
        'Commercial Aviation': ['airline', 'boeing', 'airbus', 'passenger', 'commercial', 'flight', 'airport'],
        'Defense/Military': ['defense', 'military', 'fighter', 'weapon', 'army', 'navy', 'air force', 'combat'],
        'Space Exploration': ['space', 'nasa', 'spacex', 'rocket', 'satellite', 'orbit', 'mars', 'launch'],
        'Business Aviation': ['business jet', 'private aviation', 'corporate jet', 'charter', 'executive']
    }
    
    for category, keywords in categories.items():
        if any(keyword in text for keyword in keywords):
            return category
    
    return default_category

def scrape_rss_feed(source_name, source_config):
    """Scrape articles from a single RSS feed"""
    articles_added = 0
    articles_skipped = 0
    
    try:
        logger.info(f"Scraping {source_name}...")
        feed = feedparser.parse(source_config['url'])
        
        if feed.bozo and feed.bozo_exception:
            logger.warning(f"Feed parsing warning for {source_name}: {feed.bozo_exception}")
        
        default_category = source_config.get('category', 'General')
        
        for entry in feed.entries:
            try:
                # Extract basic information
                title = entry.get('title', '')
                url = entry.get('link', '')
                
                if not title or not url:
                    continue
                
                # Generate URL hash for deduplication
                url_hash = Article.generate_url_hash(url)
                
                # Check if article already exists
                existing = Article.query.filter_by(url_hash=url_hash).first()
                if existing:
                    articles_skipped += 1
                    continue
                
                # Parse publication date
                pub_date = None
                if hasattr(entry, 'published_parsed') and entry.published_parsed:
                    pub_date = datetime(*entry.published_parsed[:6])
                elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                    pub_date = datetime(*entry.updated_parsed[:6])
                else:
                    pub_date = datetime.utcnow()
                
                # Clean and extract content
                summary = clean_summary(entry.get('summary', entry.get('description', '')))
                image_url = extract_image_url(entry, source_name)
                
                # Categorize article
                category = categorize_article(title, summary, default_category)
                
                # Create article
                article = Article(
                    title=title,
                    url=url,
                    url_hash=url_hash,
                    source=source_name,
                    summary=summary,
                    publication_date=pub_date,
                    image_url=image_url,
                    category=category
                )
                
                db.session.add(article)
                articles_added += 1
                
            except Exception as e:
                logger.error(f"Error processing entry from {source_name}: {e}")
                continue
        
        db.session.commit()
        logger.info(f"{source_name}: Added {articles_added} articles, skipped {articles_skipped} duplicates")
        
    except Exception as e:
        logger.error(f"Error scraping {source_name}: {e}")
        db.session.rollback()
    
    return articles_added

def scrape_all_sources():
    """Scrape all configured RSS sources"""
    logger.info("Starting RSS feed scraping...")
    total_added = 0
    
    # Combine primary and fallback sources
    all_sources = {**RSS_SOURCES, **FALLBACK_SOURCES}
    
    for source_name, source_config in all_sources.items():
        added = scrape_rss_feed(source_name, source_config)
        total_added += added
    
    logger.info(f"Scraping complete. Total articles added: {total_added}")
    return total_added

if __name__ == '__main__':
    # Test scraper
    scrape_all_sources()
