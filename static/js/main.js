// Main JavaScript file for the home page

document.addEventListener('DOMContentLoaded', function() {
    console.log('arXiv Paper Analysis application loaded successfully');
    
    // Add any home page specific functionality here
    
    // Example: Animated counter for stats (if we add them later)
    function animateCounter(element, target, duration) {
        const start = 0;
        const increment = target / (duration / 16);
        let current = start;
        
        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                clearInterval(timer);
                element.textContent = target;
            } else {
                element.textContent = Math.floor(current);
            }
        }, 16);
    }
    
    // If there are any counter elements on the page, animate them
    const counters = document.querySelectorAll('.counter');
    if (counters.length > 0) {
        counters.forEach(counter => {
            const target = parseInt(counter.getAttribute('data-target'), 10);
            animateCounter(counter, target, 1000);
        });
    }
});
