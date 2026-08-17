
document.addEventListener('DOMContentLoaded', function() {
    
    // ============================================================
    // VALUE CARDS - Animate progress bars on scroll
    // ============================================================
    const aboutValueCards = document.querySelectorAll('.about-value-card');
    
    const aboutObserverOptions = {
        threshold: 0.3,
        rootMargin: '0px'
    };
    
    const aboutValueObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const card = entry.target;
                const progressBar = card.querySelector('.about-value-progress-bar');
                if (progressBar) {
                    progressBar.style.width = '100%';
                }
                aboutValueObserver.unobserve(card);
            }
        });
    }, aboutObserverOptions);
    
    aboutValueCards.forEach(card => {
        aboutValueObserver.observe(card);
    });
    
    // ============================================================
    // FLOATING CARDS - Parallax effect on mouse move
    // ============================================================
    const aboutImageContainer = document.querySelector('.about-image-container');
    
    if (aboutImageContainer) {
        aboutImageContainer.addEventListener('mousemove', function(e) {
            const rect = this.getBoundingClientRect();
            const x = (e.clientX - rect.left) / rect.width;
            const y = (e.clientY - rect.top) / rect.height;
            
            const cards = this.querySelectorAll('.about-float-card');
            cards.forEach(function(card, index) {
                const speed = 20 + (index * 5);
                const moveX = (x - 0.5) * speed;
                const moveY = (y - 0.5) * speed;
                card.style.transform = 'translate(' + moveX + 'px, ' + moveY + 'px)';
            });
        });
        
        aboutImageContainer.addEventListener('mouseleave', function() {
            const cards = this.querySelectorAll('.about-float-card');
            cards.forEach(function(card) {
                card.style.transform = 'translate(0, 0)';
                card.style.transition = 'all 0.5s ease';
            });
        });
    }
    
    // ============================================================
    // SCROLL REVEAL - Fade in elements
    // ============================================================
    const aboutRevealElements = document.querySelectorAll('.about-value-card, .about-stat-item, .about-timeline-item');
    
    const aboutRevealObserver = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, { threshold: 0.2 });
    
    aboutRevealElements.forEach(function(el) {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'all 0.8s ease';
        aboutRevealObserver.observe(el);
    });
    
    // ============================================================
    // TIMELINE DOT - Animate on scroll
    // ============================================================
    const aboutTimelineDots = document.querySelectorAll('.about-timeline-dot');
    
    const aboutDotObserver = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting) {
                entry.target.style.transform = 'scale(1.2)';
                entry.target.style.boxShadow = '0 0 0 8px rgba(30, 58, 138, 0.2)';
                setTimeout(function() {
                    entry.target.style.transform = 'scale(1)';
                    entry.target.style.boxShadow = '0 0 0 4px rgba(30, 58, 138, 0.15)';
                }, 400);
                aboutDotObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });
    
    aboutTimelineDots.forEach(function(dot) {
        aboutDotObserver.observe(dot);
    });
    
});