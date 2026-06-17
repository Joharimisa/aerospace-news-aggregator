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

## API Endpoints

- `GET /` - Main page
- `GET /api/articles` - Fetch articles with pagination and filtering
- `GET /api/breaking` - Get breaking news
- `GET /api/categories` - Get all categories
- `GET /api/stats` - Get statistics
- `POST /api/trigger-scrape` - Manually trigger scraping (for testing)


