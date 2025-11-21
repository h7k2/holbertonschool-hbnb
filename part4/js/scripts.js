document.addEventListener('DOMContentLoaded', () => {
        if (document.getElementById('review-form') && window.location.pathname.endsWith('add_review.html')) {
          const token = checkAuthOrRedirect();
          const placeId = getPlaceIdFromURL();
          populateRatingOptions();
          const reviewForm = document.getElementById('review-form');
          reviewForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const reviewText = document.getElementById('review').value;
            const rating = document.getElementById('rating').value;
            if (!placeId) {
              alert('Place ID manquant dans l’URL.');
              return;
            }
            try {
              const response = await fetch(`http://127.0.0.1:5000/places/${placeId}/reviews`, {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json',
                  'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({ text: reviewText, rating: rating, place_id: placeId })
              });
              if (response.ok) {
                alert('Review submitted successfully!');
                reviewForm.reset();
              } else {
                const errorData = await response.json().catch(() => ({}));
                alert('Failed to submit review: ' + (errorData.message || response.statusText));
              }
            } catch (error) {
              alert('Erreur réseau: ' + error.message);
            }
          });
        }

        function checkAuthOrRedirect() {
          const token = getCookie('token');
          if (!token) {
            window.location.href = 'index.html';
          }
          return token;
        }

        function populateRatingOptions() {
          const ratingSelect = document.getElementById('rating');
          if (!ratingSelect) return;
          ratingSelect.innerHTML = '';
          const placeholder = document.createElement('option');
          placeholder.value = '';
          placeholder.disabled = true;
          placeholder.selected = true;
          placeholder.hidden = true;
          placeholder.textContent = 'Choisir une note';
          ratingSelect.appendChild(placeholder);
          for (let i = 1; i <= 5; i++) {
            const opt = document.createElement('option');
            opt.value = i;
            opt.textContent = i;
            ratingSelect.appendChild(opt);
          }
        }
      if (document.getElementById('place-details')) {
        const placeId = getPlaceIdFromURL();
        const token = getCookie('token');
        checkReviewForm(token);
        fetchPlaceDetails(token, placeId);
      }

      function getPlaceIdFromURL() {
        const params = new URLSearchParams(window.location.search);
        return params.get('id');
      }

      function checkReviewForm(token) {
        const addReviewSection = document.getElementById('add-review');
        if (!addReviewSection) return;
        if (!token) {
          addReviewSection.style.display = 'none';
        } else {
          addReviewSection.style.display = 'block';
        }
      }

      async function fetchPlaceDetails(token, placeId) {
        if (!placeId) {
          document.getElementById('place-details').innerHTML = '<p>Place ID manquant dans l’URL.</p>';
          return;
        }
        try {
          const response = await fetch(`http://127.0.0.1:5000/places/${placeId}`, {
            headers: token ? { 'Authorization': `Bearer ${token}` } : {}
          });
          if (response.ok) {
            const data = await response.json();
            displayPlaceDetails(data);
            displayReviews(data.reviews || []);
          } else {
            document.getElementById('place-details').innerHTML = '<p>Erreur lors du chargement du lieu.</p>';
          }
        } catch (error) {
          document.getElementById('place-details').innerHTML = '<p>Erreur réseau.</p>';
        }
      }

      function displayPlaceDetails(place) {
        const placeDetails = document.getElementById('place-details');
        if (!placeDetails) return;
        placeDetails.innerHTML = '';
        const name = document.createElement('h2');
        name.textContent = place.name;
        const desc = document.createElement('p');
        desc.textContent = place.description || '';
        const price = document.createElement('p');
        price.textContent = `Price per night: $${place.price}`;
        const amenities = document.createElement('ul');
        amenities.textContent = 'Amenities:';
        (place.amenities || []).forEach(a => {
          const li = document.createElement('li');
          li.textContent = a;
          amenities.appendChild(li);
        });
        placeDetails.appendChild(name);
        placeDetails.appendChild(desc);
        placeDetails.appendChild(price);
        placeDetails.appendChild(amenities);
      }

      function displayReviews(reviews) {
        const reviewsSection = document.getElementById('reviews');
        if (!reviewsSection) return;
        reviewsSection.innerHTML = '';
        if (!reviews.length) {
          reviewsSection.innerHTML = '<p>No reviews yet.</p>';
          return;
        }
        reviews.forEach(r => {
          const card = document.createElement('div');
          card.className = 'review-card';
          card.innerHTML = `<p>${r.text}</p><span>User: ${r.user || ''}</span><span>Rating: ${r.rating || ''}</span>`;
          reviewsSection.appendChild(card);
        });
      }
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
      loginForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        try {
          const response = await fetch('http://127.0.0.1:5000/auth/login', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
          });

          if (response.ok) {
            const data = await response.json();
            document.cookie = `token=${data.access_token}; path=/`;
            window.location.href = 'index.html';
          } else {
            const errorData = await response.json().catch(() => ({}));
            const errorMsg = errorData.message || response.statusText || 'Login failed';
            alert('Login failed: ' + errorMsg);
          }
        } catch (error) {
          alert('Login failed: ' + error.message);
        }
      });
    }

    if (document.getElementById('places-list')) {
      checkAuthentication();
      populatePriceFilter();
    }
    function getCookie(name) {
      const value = `; ${document.cookie}`;
      const parts = value.split(`; ${name}=`);
      if (parts.length === 2) return parts.pop().split(';').shift();
      return null;
    }

    function checkAuthentication() {
      const token = getCookie('token');
      const loginLink = document.getElementById('login-link');
      if (!loginLink) return;
      if (!token) {
        loginLink.style.display = 'block';
      } else {
        loginLink.style.display = 'none';
        fetchPlaces(token);
      }
    }

    function populatePriceFilter() {
      const priceFilter = document.getElementById('price-filter');
      if (!priceFilter) return;
      const options = [10, 50, 100, 'All'];
      priceFilter.innerHTML = '';
      options.forEach(opt => {
        const option = document.createElement('option');
        option.value = opt === 'All' ? '' : opt;
        option.textContent = opt;
        priceFilter.appendChild(option);
      });
      priceFilter.addEventListener('change', filterPlacesByPrice);
    }

    let allPlaces = [];

    async function fetchPlaces(token) {
      try {
        const response = await fetch('http://127.0.0.1:5000/places', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        if (response.ok) {
          const data = await response.json();
          allPlaces = data;
          displayPlaces(allPlaces);
        } else {
          document.getElementById('places-list').innerHTML = '<p>Erreur lors du chargement des places.</p>';
        }
      } catch (error) {
        document.getElementById('places-list').innerHTML = '<p>Erreur réseau.</p>';
      }
    }

    function displayPlaces(places) {
      const placesList = document.getElementById('places-list');
      if (!placesList) return;
      placesList.innerHTML = '';
      places.forEach(place => {
        const card = document.createElement('div');
        card.className = 'place-card';
        card.innerHTML = `
          <h3>${place.name}</h3>
          <p>${place.description || ''}</p>
          <p>Location: ${place.location || ''}</p>
          <p>Price per night: $${place.price}</p>
        `;
        card.dataset.price = place.price;
        placesList.appendChild(card);
      });
    }

    function filterPlacesByPrice() {
      const priceFilter = document.getElementById('price-filter');
      const selected = priceFilter.value;
      const cards = document.querySelectorAll('.place-card');
      cards.forEach(card => {
        const price = parseFloat(card.dataset.price);
        if (!selected || price <= parseFloat(selected)) {
          card.style.display = '';
        } else {
          card.style.display = 'none';
        }
      });
    }
  });