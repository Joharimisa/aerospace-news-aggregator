// State management
let currentPage = 1;
let currentCategory = 'all';
let currentSearch = '';
let isLoading = false;
let hasMore = true;

// DOM Elements
const articlesGrid = document.getElementById('articles-grid');
const loadingIndicator = document.getElementById('loading');
const noResults = document.getElementById('no-results');
const loadMoreContainer = document.getElementById('load-more-container');
const loadMoreBtn = document.getElementById('load-more');
const searchInput = document.getElementById('search-input');
const categoryBtns = document.querySelectorAll('.category-btn');
const tickerContent = document.getElementById('ticker-content');
const totalArticlesEl = document.getElementById('total-articles');
const lastUpdatedEl = document.getElementById('last-updated');

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    loadBreakingNews();
    loadStats();
    loadArticles();
    setupEventListeners();
});

// Setup event listeners
function setupEventListeners() {
    // Search input with debounce
    let searchTimeout;
    searchInput.addEventListener('input', (e) => {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(() => {
            currentSearch = e.target.value.trim();
            currentPage = 1;
            hasMore = true;
            articlesGrid.innerHTML = '';
            loadArticles();
        }, 300);
    });

    // Category filters
    categoryBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            categoryBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            currentCategory = btn.dataset.category;
            currentPage = 1;
            hasMore = true;
            articlesGrid.innerHTML = '';
            loadArticles();
        });
    });

    // Load more button
    loadMoreBtn.addEventListener('click', () => {
        if (!isLoading && hasMore) {
            currentPage++;
            loadArticles();
        }
    });
}

// Load articles from API
async function loadArticles() {
    if (isLoading) return;
    
    isLoading = true;
    loadingIndicator.classList.remove('hidden');
    noResults.classList.add('hidden');
    
    try {
        const params = new URLSearchParams({
            page: currentPage,
            per_page: 12,
            category: currentCategory,
            q: currentSearch
        });
        
        const response = await fetch(`/api/articles?${params}`);
        const data = await response.json();
        
        loadingIndicator.classList.add('hidden');
        
        if (data.articles.length === 0 && currentPage === 1) {
            noResults.classList.remove('hidden');
            articlesGrid.classList.add('hidden');
            loadMoreContainer.classList.add('hidden');
        } else {
            articlesGrid.classList.remove('hidden');
            data.articles.forEach(article => {
                articlesGrid.appendChild(createArticleCard(article));
            });
            
            hasMore = data.has_next;
            loadMoreContainer.classList.toggle('hidden', !hasMore);
        }
        
        // Update last updated time
        lastUpdatedEl.textContent = new Date().toLocaleString();
        
    } catch (error) {
        console.error('Error loading articles:', error);
        loadingIndicator.classList.add('hidden');
        noResults.innerHTML = '<p class="text-red-500">Error loading articles. Please try again.</p>';
        noResults.classList.remove('hidden');
    }
    
    isLoading = false;
}

// Create article card element
function createArticleCard(article) {
    const card = document.createElement('article');
    card.className = 'article-card bg-white rounded-xl shadow-md overflow-hidden transition-all duration-300';
    
    const imageHtml = article.image_url 
        ? `<img src="${article.image_url}" alt="${article.title}" class="w-full h-48 object-cover" loading="lazy">`
        : `<div class="w-full h-48 bg-gradient-to-br from-blue-100 to-blue-200 flex items-center justify-center">
            <svg class="w-16 h-16 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064"></path>
            </svg>
           </div>`;
    
    const pubDate = article.publication_date 
        ? new Date(article.publication_date).toLocaleDateString('en-US', { 
            year: 'numeric', 
            month: 'short', 
            day: 'numeric' 
          })
        : 'Unknown date';
    
    card.innerHTML = `
        ${imageHtml}
        <div class="p-5">
            <div class="flex items-center justify-between mb-3">
                <span class="px-3 py-1 bg-blue-100 text-blue-800 text-xs font-medium rounded-full">
                    ${article.category}
                </span>
                <span class="text-sm text-gray-500">${article.source}</span>
            </div>
            <h3 class="text-lg font-semibold text-gray-900 mb-2 line-clamp-2 hover:text-blue-600">
                <a href="${article.url}" target="_blank" rel="noopener noreferrer">${article.title}</a>
            </h3>
            <p class="text-gray-600 text-sm mb-4 line-clamp-3">${article.summary || 'No summary available.'}</p>
            <div class="flex items-center justify-between">
                <span class="text-xs text-gray-400">${pubDate}</span>
                <a href="${article.url}" target="_blank" rel="noopener noreferrer" 
                   class="text-blue-600 hover:text-blue-800 text-sm font-medium flex items-center">
                    Read more
                    <svg class="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
                    </svg>
                </a>
            </div>
        </div>
    `;
    
    return card;
}

// Load breaking news for ticker
async function loadBreakingNews() {
    try {
        const response = await fetch('/api/breaking');
        const articles = await response.json();
        
        if (articles.length > 0) {
            const tickerHtml = articles.map(article => 
                `<span class="mx-8">📰 ${article.title.substring(0, 100)}...</span>`
            ).join('');
            
            // Duplicate content for seamless loop
            tickerContent.innerHTML = tickerHtml + tickerHtml;
        }
    } catch (error) {
        console.error('Error loading breaking news:', error);
    }
}

// Load statistics
async function loadStats() {
    try {
        const response = await fetch('/api/stats');
        const stats = await response.json();
        
        totalArticlesEl.textContent = `${stats.total_articles.toLocaleString()} articles`;
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}
