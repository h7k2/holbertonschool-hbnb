// ============================================================================
// HBnB Application - Main JavaScript
// ============================================================================

// API Configuration
const API_BASE_URL = 'http://127.0.0.1:5000/api/v1';

// ============================================================================
// Utility Functions
// ============================================================================

/**
 * Get cookie value by name
 * @param {string} name - Cookie name
 * @returns {string|null} Cookie value or null if not found
 */
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) {
        return parts.pop().split(';').shift();
    }
    return null;
}

/**
 * Set secure cookie with SameSite and path
 * @param {string} name - Cookie name
 * @param {string} value - Cookie value
 * @param {number} days - Expiration in days (default: 1)
 */
function setCookie(name, value, days = 1) {
    const expires = new Date();
    expires.setTime(expires.getTime() + (days * 24 * 60 * 60 * 1000));
    document.cookie = `${name}=${value}; expires=${expires.toUTCString()}; path=/; SameSite=Lax`;
}

/**
 * Delete cookie
 * @param {string} name - Cookie name
 */
function deleteCookie(name) {
    document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/; SameSite=Lax`;
}

/**
 * Get place ID from URL query parameters
 * @returns {string|null} Place ID or null
 */
function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('id');
}

/**
 * Show message to user
 * @param {string} elementId - Element ID to show message
 * @param {string} message - Message text
 * @param {string} type - Message type ('success' or 'error')
 */
function showMessage(elementId, message, type = 'success') {
    const element = document.getElementById(elementId);
    if (!element) return;
    
    element.textContent = message;
    element.className = type === 'success' ? 'success-message' : 'error-message';
    element.style.display = 'block';
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        element.style.display = 'none';
    }, 5000);
}

// ============================================================================
// Authentication Functions
// ============================================================================

/**
 * Check if user is authenticated
 * @returns {string|null} JWT token or null
 */
function checkAuthentication() {
    return getCookie('token');
}

/**
 * Check authentication or redirect to index
 * @returns {string} JWT token
 */
function checkAuthOrRedirect() {
    const token = checkAuthentication();
    if (!token) {
        window.location.href = 'index.html';
    }
    return token;
}

/**
 * Update login link visibility based on authentication status
 */
function updateLoginLink() {
    const token = checkAuthentication();
    const loginLink = document.getElementById('login-link');
    
    if (loginLink) {
        if (token) {
            loginLink.style.display = 'none';
        } else {
            loginLink.style.display = 'inline-block';
        }
    }
}

// ============================================================================
// Login Page Functions
// ============================================================================

/**
 * Handle login form submission
 */
function initLoginForm() {
    const loginForm = document.getElementById('login-form');
    if (!loginForm) return;

    loginForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        try {
            const response = await fetch(`${API_BASE_URL}/auth/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email, password })
            });

            if (response.ok) {
                const data = await response.json();
                setCookie('token', data.access_token, 1); // Cookie expires in 1 day
                window.location.href = 'index.html';
            } else {
                const errorData = await response.json().catch(() => ({}));
                const errorMsg = errorData.message || response.statusText || 'Login failed';
                showMessage('error-message', `Login failed: ${errorMsg}`, 'error');
            }
        } catch (error) {
            showMessage('error-message', `Network error: ${error.message}`, 'error');
        }
    });
}

// ============================================================================
// Index Page Functions (Places List)
// ============================================================================

let allPlaces = []; // Store all places for filtering

/**
 * Fetch all places from API
 */
async function fetchPlaces() {
    const token = checkAuthentication();
    
    try {
        const headers = {};
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        const response = await fetch(`${API_BASE_URL}/places`, {
            headers: headers
        });

        if (response.ok) {
            const data = await response.json();
            allPlaces = data;
            displayPlaces(allPlaces);
        } else {
            document.getElementById('places-list').innerHTML = 
                '<p class="error-message">Error loading places. Please try again later.</p>';
        }
    } catch (error) {
        document.getElementById('places-list').innerHTML = 
            '<p class="error-message">Network error. Please check your connection.</p>';
    }
}

/**
 * Display places in the list
 * @param {Array} places - Array of place objects
 */
function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    if (!placesList) return;

    placesList.innerHTML = '';

    if (!places || places.length === 0) {
        placesList.innerHTML = '<p>No places available.</p>';
        return;
    }

    places.forEach(place => {
        const card = document.createElement('div');
        card.className = 'place-card';
        card.dataset.price = place.price;
        
        const title = document.createElement('h3');
        title.textContent = place.title || place.name || 'Unnamed Place';
        
        const description = document.createElement('p');
        description.textContent = place.description || 'No description available';
        
        const location = document.createElement('p');
        location.textContent = `Location: ${place.location || 'Not specified'}`;
        
        const price = document.createElement('p');
        price.textContent = `Price per night: $${place.price}`;
        price.style.fontWeight = 'bold';
        
        const detailsButton = document.createElement('button');
        detailsButton.className = 'details-button';
        detailsButton.textContent = 'View Details';
        detailsButton.addEventListener('click', () => {
            window.location.href = `place.html?id=${place.id}`;
        });
        
        card.appendChild(title);
        card.appendChild(description);
        card.appendChild(location);
        card.appendChild(price);
        card.appendChild(detailsButton);
        
        placesList.appendChild(card);
    });
}

/**
 * Filter places by price
 */
function filterPlacesByPrice() {
    const priceFilter = document.getElementById('price-filter');
    if (!priceFilter) return;

    const maxPrice = priceFilter.value;

    if (!maxPrice || maxPrice === '') {
        // Show all places
        displayPlaces(allPlaces);
    } else {
        // Filter places by max price
        const filteredPlaces = allPlaces.filter(place => 
            parseFloat(place.price) <= parseFloat(maxPrice)
        );
        displayPlaces(filteredPlaces);
    }
}

/**
 * Initialize price filter
 */
function initPriceFilter() {
    const priceFilter = document.getElementById('price-filter');
    if (!priceFilter) return;

    priceFilter.addEventListener('change', filterPlacesByPrice);
}

/**
 * Initialize index page
 */
function initIndexPage() {
    updateLoginLink();
    initPriceFilter();
    fetchPlaces();
}

// ============================================================================
// Place Details Page Functions
// ============================================================================

/**
 * Fetch place details by ID
 * @param {string} placeId - Place ID
 */
async function fetchPlaceDetails(placeId) {
    if (!placeId) {
        document.getElementById('place-details').innerHTML = 
            '<p class="error-message">Place ID is missing from URL.</p>';
        return;
    }

    const token = checkAuthentication();
    
    try {
        const headers = {};
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        const response = await fetch(`${API_BASE_URL}/places/${placeId}`, {
            headers: headers
        });

        if (response.ok) {
            const place = await response.json();
            displayPlaceDetails(place);
            await fetchPlaceReviews(placeId);
        } else {
            document.getElementById('place-details').innerHTML = 
                '<p class="error-message">Error loading place details.</p>';
        }
    } catch (error) {
        document.getElementById('place-details').innerHTML = 
            '<p class="error-message">Network error.</p>';
    }
}

/**
 * Display place details
 * @param {Object} place - Place object
 */
function displayPlaceDetails(place) {
    const placeDetails = document.getElementById('place-details');
    if (!placeDetails) return;

    placeDetails.innerHTML = '';

    const title = document.createElement('h2');
    title.textContent = place.title || place.name || 'Unnamed Place';
    
    const description = document.createElement('p');
    description.textContent = place.description || 'No description available';
    
    const price = document.createElement('p');
    price.textContent = `Price per night: $${place.price}`;
    price.style.fontWeight = 'bold';
    price.style.fontSize = '1.2em';
    price.style.color = '#28a745';
    
    const location = document.createElement('p');
    location.textContent = `Location: ${place.location || 'Not specified'}`;
    
    // Display host information if available
    if (place.owner_id) {
        const host = document.createElement('p');
        host.textContent = `Host ID: ${place.owner_id}`;
        placeDetails.appendChild(host);
    }
    
    // Display amenities if available
    if (place.amenities && place.amenities.length > 0) {
        const amenitiesTitle = document.createElement('h3');
        amenitiesTitle.textContent = 'Amenities:';
        amenitiesTitle.style.marginTop = '20px';
        
        const amenitiesList = document.createElement('ul');
        place.amenities.forEach(amenity => {
            const li = document.createElement('li');
            li.textContent = typeof amenity === 'string' ? amenity : amenity.name;
            amenitiesList.appendChild(li);
        });
        
        placeDetails.appendChild(amenitiesTitle);
        placeDetails.appendChild(amenitiesList);
    }
    
    placeDetails.insertBefore(location, placeDetails.firstChild);
    placeDetails.insertBefore(price, placeDetails.firstChild);
    placeDetails.insertBefore(description, placeDetails.firstChild);
    placeDetails.insertBefore(title, placeDetails.firstChild);
}

/**
 * Fetch reviews for a place
 * @param {string} placeId - Place ID
 */
async function fetchPlaceReviews(placeId) {
    const token = checkAuthentication();
    
    try {
        const headers = {};
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        const response = await fetch(`${API_BASE_URL}/places/${placeId}/reviews`, {
            headers: headers
        });

        if (response.ok) {
            const reviews = await response.json();
            displayReviews(reviews);
        } else {
            document.getElementById('reviews').innerHTML = 
                '<h2>User Reviews</h2><p>Unable to load reviews.</p>';
        }
    } catch (error) {
        document.getElementById('reviews').innerHTML = 
            '<h2>User Reviews</h2><p>Network error loading reviews.</p>';
    }
}

/**
 * Display reviews
 * @param {Array} reviews - Array of review objects
 */
function displayReviews(reviews) {
    const reviewsSection = document.getElementById('reviews');
    if (!reviewsSection) return;

    reviewsSection.innerHTML = '<h2>User Reviews</h2>';

    if (!reviews || reviews.length === 0) {
        reviewsSection.innerHTML += '<p>No reviews yet. Be the first to review!</p>';
        return;
    }

    reviews.forEach(review => {
        const card = document.createElement('div');
        card.className = 'review-card';
        
        const text = document.createElement('p');
        text.textContent = `"${review.text}"`;
        text.style.fontStyle = 'italic';
        
        const user = document.createElement('span');
        user.textContent = `User: ${review.user_id || 'Anonymous'}`;
        
        const rating = document.createElement('span');
        rating.textContent = `Rating: ${'⭐'.repeat(review.rating || 0)} (${review.rating}/5)`;
        rating.style.color = '#ffa500';
        
        card.appendChild(text);
        card.appendChild(user);
        card.appendChild(rating);
        
        reviewsSection.appendChild(card);
    });
}

/**
 * Check if review form should be displayed
 */
function checkReviewFormVisibility() {
    const token = checkAuthentication();
    const addReviewSection = document.getElementById('add-review');
    
    if (addReviewSection) {
        if (token) {
            addReviewSection.style.display = 'block';
        } else {
            addReviewSection.style.display = 'none';
        }
    }
}

/**
 * Initialize review form on place details page
 * @param {string} placeId - Place ID
 */
function initPlaceReviewForm(placeId) {
    const reviewForm = document.getElementById('review-form');
    if (!reviewForm) return;

    reviewForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        
        const token = checkAuthOrRedirect();
        const reviewText = document.getElementById('review-text').value;
        const reviewRating = document.getElementById('review-rating').value;

        if (!reviewRating) {
            showMessage('review-message', 'Please select a rating.', 'error');
            return;
        }

        try {
            const response = await fetch(`${API_BASE_URL}/reviews`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({
                    text: reviewText,
                    rating: parseInt(reviewRating),
                    place_id: placeId
                })
            });

            if (response.ok) {
                showMessage('review-message', 'Review submitted successfully!', 'success');
                reviewForm.reset();
                // Reload reviews
                await fetchPlaceReviews(placeId);
            } else {
                const errorData = await response.json().catch(() => ({}));
                showMessage('review-message', 
                    `Failed to submit review: ${errorData.message || response.statusText}`, 
                    'error');
            }
        } catch (error) {
            showMessage('review-message', `Network error: ${error.message}`, 'error');
        }
    });
}

/**
 * Initialize place details page
 */
function initPlaceDetailsPage() {
    const placeId = getPlaceIdFromURL();
    updateLoginLink();
    checkReviewFormVisibility();
    fetchPlaceDetails(placeId);
    initPlaceReviewForm(placeId);
}

// ============================================================================
// Add Review Page Functions
// ============================================================================

/**
 * Initialize add review form (standalone page)
 */
function initAddReviewForm() {
    const token = checkAuthOrRedirect();
    const placeId = getPlaceIdFromURL();
    
    if (!placeId) {
        showMessage('review-message', 'Place ID is missing from URL.', 'error');
        return;
    }

    const reviewForm = document.getElementById('review-form');
    if (!reviewForm) return;

    reviewForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        
        const reviewText = document.getElementById('review').value;
        const rating = document.getElementById('rating').value;

        if (!rating) {
            showMessage('review-message', 'Please select a rating.', 'error');
            return;
        }

        try {
            const response = await fetch(`${API_BASE_URL}/reviews`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({
                    text: reviewText,
                    rating: parseInt(rating),
                    place_id: placeId
                })
            });

            if (response.ok) {
                showMessage('review-message', 'Review submitted successfully!', 'success');
                reviewForm.reset();
                
                // Redirect to place details after 2 seconds
                setTimeout(() => {
                    window.location.href = `place.html?id=${placeId}`;
                }, 2000);
            } else {
                const errorData = await response.json().catch(() => ({}));
                showMessage('review-message', 
                    `Failed to submit review: ${errorData.message || response.statusText}`, 
                    'error');
            }
        } catch (error) {
            showMessage('review-message', `Network error: ${error.message}`, 'error');
        }
    });
}

// ============================================================================
// Page Initialization
// ============================================================================

/**
 * Initialize page based on current path
 */
document.addEventListener('DOMContentLoaded', () => {
    const path = window.location.pathname;
    
    // Determine which page we're on and initialize accordingly
    if (path.endsWith('login.html') || document.getElementById('login-form')) {
        if (path.endsWith('login.html')) {
            initLoginForm();
        }
    } else if (path.endsWith('index.html') || document.getElementById('places-list')) {
        if (document.getElementById('places-list')) {
            initIndexPage();
        }
    } else if (path.endsWith('place.html') || document.getElementById('place-details')) {
        if (document.getElementById('place-details')) {
            initPlaceDetailsPage();
        }
    } else if (path.endsWith('add_review.html')) {
        if (document.getElementById('review-form') && !document.getElementById('place-details')) {
            initAddReviewForm();
        }
    }
});
