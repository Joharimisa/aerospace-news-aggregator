from flask import Blueprint, render_template, jsonify, request
from app.models import Article, db
from datetime import datetime, timedelta

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Render main page"""
    return render_template('index.html')

@main_bp.route('/api/articles')
def get_articles():
    """API endpoint to fetch articles with filtering and pagination"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    category = request.args.get('category', '')
    search_query = request.args.get('q', '')
    
    # Build query
    query = Article.query
    
    # Apply category filter
    if category and category != 'all':
        query = query.filter(Article.category == category)
    
    # Apply search filter
    if search_query:
        search_term = f'%{search_query}%'
        query = query.filter(
            (Article.title.ilike(search_term)) |
            (Article.summary.ilike(search_term))
        )
    
    # Order by publication date (newest first)
    query = query.order_by(Article.publication_date.desc())
    
    # Paginate
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    articles = [article.to_dict() for article in pagination.items]
    
    return jsonify({
        'articles': articles,
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page,
        'has_next': pagination.has_next,
        'has_prev': pagination.has_prev
    })

@main_bp.route('/api/breaking')
def get_breaking_news():
    """Get breaking news (most recent articles)"""
    breaking_articles = Article.query.order_by(
        Article.publication_date.desc()
    ).limit(10).all()
    
    return jsonify([article.to_dict() for article in breaking_articles])

@main_bp.route('/api/categories')
def get_categories():
    """Get all available categories"""
    categories = db.session.query(Article.category).distinct().all()
    return jsonify([cat[0] for cat in categories])

@main_bp.route('/api/stats')
def get_stats():
    """Get statistics about articles"""
    total_articles = Article.query.count()
    categories = db.session.query(
        Article.category,
        db.func.count(Article.id)
    ).group_by(Article.category).all()
    
    # Get articles from last 24 hours
    yesterday = datetime.utcnow() - timedelta(days=1)
    recent_articles = Article.query.filter(
        Article.publication_date >= yesterday
    ).count()
    
    return jsonify({
        'total_articles': total_articles,
        'recent_articles': recent_articles,
        'categories': {cat[0]: cat[1] for cat in categories}
    })

@main_bp.route('/api/trigger-scrape', methods=['POST'])
def trigger_scrape():
    """Manually trigger scraping (for testing)"""
    from scrapers.rss_scraper import scrape_all_sources
    try:
        added = scrape_all_sources()
        return jsonify({'success': True, 'articles_added': added})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
