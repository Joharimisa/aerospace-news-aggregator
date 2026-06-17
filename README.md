# Aerospace News Aggregator Platform

A production-ready, responsive web application that automatically scrapes, parses, and centralizes news articles from major aviation and aerospace sources.

## Features

- **Automatic Scraping**: Background scheduler fetches RSS feeds every 30 minutes
- **Data Deduplication**: URL hashing prevents duplicate articles
- **Modern UI**: Clean, responsive interface built with Tailwind CSS
- **Category Filtering**: Filter by Commercial Aviation, Defense/Military, Space Exploration, Business Aviation
- **Real-time Search**: Instant keyword search across all articles
- **Lazy Loading**: Optimized image loading for better performance
- **Mobile Responsive**: Fully optimized for all screen sizes

## News Sources

- Reuters (Aerospace & Defense)
- FlightGlobal
- Aviation Week
- SpaceNews
- Air & Cosmos

## Tech Stack

- **Backend**: Python Flask
- **Database**: SQLite (development) / PostgreSQL (production)
- **Scheduler**: APScheduler
- **Frontend**: HTML5, Tailwind CSS, JavaScript
- **Deployment**: Render/Railway compatible

## Local Development

### Prerequisites

- Python 3.12+
- pip

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd aerospace-news-aggregator
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python app.py
```

5. Open your browser to `http://localhost:5000`

## Environment Variables

Create a `.env` file based on `.env.example`:

```
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///aerospace_news.db
SCRAPE_INTERVAL_MINUTES=30
```

## Deployment

### Render

1. Push your code to GitHub
2. Create a new Web Service on Render
3. Connect your GitHub repository
4. Render will automatically detect the Flask app
5. Set environment variables in Render dashboard
6. Deploy!

### Railway

1. Push your code to GitHub
2. Create a new project on Railway
3. Add a PostgreSQL database
4. Add your repository as a service
5. Set environment variables
6. Deploy!

## API Endpoints

- `GET /` - Main page
- `GET /api/articles` - Fetch articles with pagination and filtering
- `GET /api/breaking` - Get breaking news
- `GET /api/categories` - Get all categories
- `GET /api/stats` - Get statistics
- `POST /api/trigger-scrape` - Manually trigger scraping (for testing)

## License

MIT License
