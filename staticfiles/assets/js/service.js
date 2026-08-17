
document.addEventListener('DOMContentLoaded', function() {
    
    // ============================================================
    // SERVICE CARDS - Intersection Observer Animation
    // ============================================================
    const serviceCards = document.querySelectorAll('.service-card');
    
    const cardObserver = new IntersectionObserver((entries) => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                setTimeout(() => {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }, index * 100);
                cardObserver.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.2,
        rootMargin: '0px'
    });
    
    serviceCards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        card.style.transition = 'all 0.6s cubic-bezier(0.34, 1.56, 0.64, 1)';
        cardObserver.observe(card);
    });
    
    // ============================================================
    // VISUAL CARDS - Parallax mouse effect
    // ============================================================
    const visualGrid = document.querySelector('.visual-grid');
    
    if (visualGrid) {
        visualGrid.addEventListener('mousemove', function(e) {
            const rect = this.getBoundingClientRect();
            const x = (e.clientX - rect.left) / rect.width - 0.5;
            const y = (e.clientY - rect.top) / rect.height - 0.5;
            
            const cards = this.querySelectorAll('.visual-card');
            cards.forEach((card, index) => {
                const speed = 10 + (index * 3);
                const moveX = x * speed;
                const moveY = y * speed;
                card.style.transform = `translate(${moveX}px, ${moveY}px)`;
            });
        });
        
        visualGrid.addEventListener('mouseleave', function() {
            const cards = this.querySelectorAll('.visual-card');
            cards.forEach(card => {
                card.style.transform = 'translate(0, 0)';
                card.style.transition = 'all 0.5s ease';
            });
        });
    }
    
    // ============================================================
    // STAT COUNTER ANIMATION
    // ============================================================
    const statNumbers = document.querySelectorAll('.stat-number');
    
    const statObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const el = entry.target;
                const text = el.textContent;
                const number = parseInt(text.replace(/[^0-9]/g, ''));
                const suffix = text.replace(/[0-9]/g, '');
                
                if (isNaN(number)) return;
                
                let current = 0;
                const duration = 2000;
                const stepTime = 16;
                const steps = duration / stepTime;
                const increment = number / steps;
                
                const updateCounter = () => {
                    current += increment;
                    if (current >= number) {
                        el.textContent = number + suffix;
                        return;
                    }
                    el.textContent = Math.floor(current) + suffix;
                    requestAnimationFrame(updateCounter);
                };
                
                updateCounter();
                statObserver.unobserve(el);
            }
        });
    }, { threshold: 0.5 });
    
    statNumbers.forEach(stat => statObserver.observe(stat));
    
});