// FAQ Toggle Function
function toggleFaq(element) {
    const faqItem = element.closest('.faq-item');
    const isActive = faqItem.classList.contains('faq-active');
    
    // Close all other FAQs (accordion behavior)
    document.querySelectorAll('.faq-item').forEach(item => {
        item.classList.remove('faq-active');
    });
    
    // Toggle current - if it wasn't active, open it
    if (!isActive) {
        faqItem.classList.add('faq-active');
    }
}

// Ensure all FAQs are closed on page load
document.addEventListener('DOMContentLoaded', function() {
    // Close all FAQ items initially
    document.querySelectorAll('.faq-item').forEach(item => {
        item.classList.remove('faq-active');
    });
    
    // Counter Animation with Intersection Observer
    const counters = document.querySelectorAll('.counter');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const counter = entry.target;
                const target = parseInt(counter.getAttribute('data-target'));
                animateCounter(counter, target);
                observer.unobserve(counter);
            }
        });
    }, { threshold: 0.3 });
    
    counters.forEach(counter => observer.observe(counter));
});

// Counter Animation Function
function animateCounter(element, target) {
    let current = 0;
    const increment = Math.ceil(target / 40); // Adjust speed
    const duration = 1500; // ms
    const stepTime = Math.floor(duration / 40);
    
    const timer = setInterval(() => {
        current += increment;
        if (current >= target) {
            element.textContent = target;
            clearInterval(timer);
        } else {
            element.textContent = current;
        }
    }, stepTime);
}

// Optional: Reset counters if they need to re-animate (useful for tabs/modals)
function resetCounters() {
    document.querySelectorAll('.counter').forEach(counter => {
        counter.textContent = '0';
    });
}