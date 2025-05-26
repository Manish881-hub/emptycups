// State management for shortlisted items
let shortlistedStudios = new Set();
let isShortlistFilterActive = false;

// Initialize the application
function init() {
    setupEventListeners();
    loadShortlistedFromStorage();
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

// Load shortlisted items from localStorage
function loadShortlistedFromStorage() {
    const savedShortlist = localStorage.getItem('shortlistedStudios');
    if (savedShortlist) {
        shortlistedStudios = new Set(JSON.parse(savedShortlist));
        updateShortlistButtons();
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
function handleShortlistToggle(event) {
    event.preventDefault();
    const button = event.currentTarget;
    const studioId = button.getAttribute('data-studio');
    const icon = button.querySelector('.icon');

    if (shortlistedStudios.has(studioId)) {
        // Remove from shortlist
        shortlistedStudios.delete(studioId);
        button.classList.remove('shortlisted');
        icon.textContent = '🤍';
    } else {
        // Add to shortlist
        shortlistedStudios.add(studioId);
        button.classList.add('shortlisted');
        icon.textContent = '❤️';
    }

    // Save to localStorage
    localStorage.setItem('shortlistedStudios', JSON.stringify(Array.from(shortlistedStudios)));

    // Update display if shortlist filter is active
    if (isShortlistFilterActive) {
        updateStudioDisplay();
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