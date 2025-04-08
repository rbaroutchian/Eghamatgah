// Mobile Menu Toggle
document.addEventListener('DOMContentLoaded', function() {
    const navbar = document.querySelector('.navbar');
    const menuToggle = document.createElement('button');
    menuToggle.className = 'menu-toggle';
    menuToggle.innerHTML = '<i class="fas fa-bars"></i>';

    // Add menu toggle button for mobile
    navbar.insertBefore(menuToggle, navbar.firstChild);

    menuToggle.addEventListener('click', function() {
        const navLinks = document.querySelector('.nav-links');
        navLinks.classList.toggle('active');
    });
});

// Search Form Validation
const searchForm = document.querySelector('.search-box');
if (searchForm) {
    searchForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const destination = this.querySelector('input[type="text"]').value;
        const checkIn = this.querySelector('input[type="date"]').value;
        const checkOut = this.querySelectorAll('input[type="date"]')[1].value;

        if (!destination || !checkIn || !checkOut) {
            alert('لطفا تمام فیلدها را پر کنید');
            return;
        }

        // Redirect to search results page
        window.location.href = `pages/properties.html?destination=${destination}&checkIn=${checkIn}&checkOut=${checkOut}`;
    });
}

// Property Card Hover Effect
const propertyCards = document.querySelectorAll('.property-card');
propertyCards.forEach(card => {
    card.addEventListener('mouseenter', function() {
        this.style.transform = 'translateY(-5px)';
    });

    card.addEventListener('mouseleave', function() {
        this.style.transform = 'translateY(0)';
    });
});

// Smooth Scroll for Navigation Links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth'
            });
        }
    });
});

// Date Picker Initialization
const dateInputs = document.querySelectorAll('input[type="date"]');
dateInputs.forEach(input => {
    const today = new Date().toISOString().split('T')[0];
    input.min = today;

    // Set minimum check-out date based on check-in date
    if (input.placeholder === 'تاریخ خروج') {
        const checkInInput = input.previousElementSibling;
        checkInInput.addEventListener('change', function() {
            input.min = this.value;
        });
    }
});

// Add to Favorites
const favoriteButtons = document.querySelectorAll('.favorite-btn');
favoriteButtons.forEach(button => {
    button.addEventListener('click', function() {
        this.classList.toggle('active');
        const propertyId = this.dataset.propertyId;
        // Add to favorites logic here
    });
});

// Image Gallery for Property Details
const propertyImages = document.querySelectorAll('.property-gallery img');
if (propertyImages.length > 0) {
    propertyImages.forEach(img => {
        img.addEventListener('click', function() {
            // Open image in lightbox
            const lightbox = document.createElement('div');
            lightbox.className = 'lightbox';
            lightbox.innerHTML = `
                <img src="${this.src}" alt="${this.alt}">
                <button class="close-lightbox"><i class="fas fa-times"></i></button>
            `;
            document.body.appendChild(lightbox);

            // Close lightbox
            lightbox.querySelector('.close-lightbox').addEventListener('click', function() {
                lightbox.remove();
            });
        });
    });
}