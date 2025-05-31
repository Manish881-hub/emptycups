// State management for shortlisted items
let shortlistedStudios = new Set();
let isShortlistFilterActive = false;
const API_BASE_URL = 'http://localhost:5000/api';

// Initialize the application
async function init() {
    setupEventListeners();
    await loadShortlistedFromAPI();
}

// Set up all event listeners
function setupEventListeners() {
    // Shortlist button event listeners
    const shortlistButtons = document.querySelectorAll('.shortlist-btn');
    shortlistButtons.forEach(button => {
        button.addEventListener('click', handleShortlistToggle);
    });

    // Shortlist filter event listener
    const shortlistFilter = document.getElementById('shortlist-filter');
    shortlistFilter.addEventListener('click', handleShortlistFilter);
}

// Load shortlisted items from API
async function loadShortlistedFromAPI() {
    try {
        const response = await fetch(`${API_BASE_URL}/shortlist`);
        const data = await response.json();

        if (data.success) {
            shortlistedStudios = new Set(data.data.map(listing => listing.id));
            updateShortlistButtons();
        } else {
            console.error('Failed to load shortlisted items:', data.error);
        }
    } catch (error) {
        console.error('Error loading shortlisted items:', error);
    }
}

// Update shortlist buttons based on current state
function updateShortlistButtons() {
    const shortlistButtons = document.querySelectorAll('.shortlist-btn');
    shortlistButtons.forEach(button => {
        const studioId = button.getAttribute('data-studio');
        const icon = button.querySelector('.icon');

        if (shortlistedStudios.has(studioId)) {
            button.classList.add('shortlisted');
            icon.textContent = '❤️';
        } else {
            button.classList.remove('shortlisted');
            icon.textContent = '🤍';
        }
    });
}

// Handle shortlist button toggle
async function handleShortlistToggle(event) {
    event.preventDefault();
    const button = event.currentTarget;
    const studioId = button.getAttribute('data-studio');
    const icon = button.querySelector('.icon');

    try {
        if (shortlistedStudios.has(studioId)) {
            // Remove from shortlist
            const response = await fetch(`${API_BASE_URL}/shortlist/${studioId}`, {
                method: 'DELETE'
            });
            const data = await response.json();

            if (data.success) {
                shortlistedStudios.delete(studioId);
                button.classList.remove('shortlisted');
                icon.textContent = '🤍';
            }
        } else {
            // Add to shortlist
            const response = await fetch(`${API_BASE_URL}/shortlist/${studioId}`, {
                method: 'POST'
            });
            const data = await response.json();

            if (data.success) {
                shortlistedStudios.add(studioId);
                button.classList.add('shortlisted');
                icon.textContent = '❤️';
            }
        }

        // Update display if shortlist filter is active
        if (isShortlistFilterActive) {
            updateStudioDisplay();
        }
    } catch (error) {
        console.error('Error toggling shortlist:', error);
    }
}

// Handle shortlist filter toggle
function handleShortlistFilter(event) {
    event.preventDefault();
    const filterButton = event.currentTarget;

    isShortlistFilterActive = !isShortlistFilterActive;

    if (isShortlistFilterActive) {
        filterButton.classList.add('shortlist-active');
        filterButton.style.color = '#FF6B35';
    } else {
        filterButton.classList.remove('shortlist-active');
        filterButton.style.color = '#666';
    }

    updateStudioDisplay();
}

// Update which studios are displayed
function updateStudioDisplay() {
    const studioCards = document.querySelectorAll('.studio-card');

    studioCards.forEach(card => {
        const studioId = card.getAttribute('data-studio');

        if (isShortlistFilterActive) {
            // Show only shortlisted studios
            if (shortlistedStudios.has(studioId)) {
                card.classList.remove('hidden');
            } else {
                card.classList.add('hidden');
            }
        } else {
            // Show all studios
            card.classList.remove('hidden');
        }
    });
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', init);