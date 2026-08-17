(function() {
  "use strict";

  /**
   * ============================================================
   * SCROLLED HEADER
   * ============================================================
   */
  function toggleScrolled() {
    const selectBody = document.querySelector('body');
    const selectHeader = document.querySelector('#header');
    if (!selectHeader.classList.contains('scroll-up-sticky') && !selectHeader.classList.contains('sticky-top') && !selectHeader.classList.contains('fixed-top')) return;
    window.scrollY > 100 ? selectBody.classList.add('scrolled') : selectBody.classList.remove('scrolled');
  }

  document.addEventListener('scroll', toggleScrolled);
  window.addEventListener('load', toggleScrolled);

  /**
   * ============================================================
   * MOBILE NAVIGATION
   * ============================================================
   */
  const mobileNavToggleBtn = document.querySelector('.mobile-nav-toggle');

  function mobileNavToogle() {
    document.querySelector('body').classList.toggle('mobile-nav-active');
    mobileNavToggleBtn.classList.toggle('bi-list');
    mobileNavToggleBtn.classList.toggle('bi-x');
  }
  
  if (mobileNavToggleBtn) {
    mobileNavToggleBtn.addEventListener('click', mobileNavToogle);
  }

  document.querySelectorAll('#navmenu a').forEach(navmenu => {
    navmenu.addEventListener('click', () => {
      if (document.querySelector('.mobile-nav-active')) {
        mobileNavToogle();
      }
    });
  });

  document.querySelectorAll('.navmenu .toggle-dropdown').forEach(navmenu => {
    navmenu.addEventListener('click', function(e) {
      e.preventDefault();
      this.parentNode.classList.toggle('active');
      this.parentNode.nextElementSibling.classList.toggle('dropdown-active');
      e.stopImmediatePropagation();
    });
  });

  /**
   * ============================================================
   * SCROLL TOP BUTTON
   * ============================================================
   */
  let scrollTop = document.querySelector('.scroll-top');

  function toggleScrollTop() {
    if (scrollTop) {
      window.scrollY > 100 ? scrollTop.classList.add('active') : scrollTop.classList.remove('active');
    }
  }
  
  if (scrollTop) {
    scrollTop.addEventListener('click', (e) => {
      e.preventDefault();
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      });
    });
  }

  window.addEventListener('load', toggleScrollTop);
  document.addEventListener('scroll', toggleScrollTop);

  /**
   * ============================================================
   * AOS ANIMATION
   * ============================================================
   */
  function aosInit() {
    if (typeof AOS !== 'undefined') {
      AOS.init({
        duration: 700,
        easing: 'ease-in-out',
        once: true,
        mirror: false
      });
    }
  }
  window.addEventListener('load', aosInit);

  /**
   * ============================================================
   * SKILLS ANIMATION
   * ============================================================
   */
  let skillsAnimation = document.querySelectorAll('.skills-animation');
  skillsAnimation.forEach((item) => {
    if (typeof Waypoint !== 'undefined') {
      new Waypoint({
        element: item,
        offset: '80%',
        handler: function(direction) {
          let progress = item.querySelectorAll('.progress .progress-bar');
          progress.forEach(el => {
            el.style.width = el.getAttribute('aria-valuenow') + '%';
          });
        }
      });
    }
  });

  /**
   * ============================================================
   * GLIGHTBOX
   * ============================================================
   */
  if (typeof GLightbox !== 'undefined') {
    const glightbox = GLightbox({
      selector: '.glightbox'
    });
  }

  /**
   * ============================================================
   * ISOTOPE LAYOUT
   * ============================================================
   */
  document.querySelectorAll('.isotope-layout').forEach(function(isotopeItem) {
    let layout = isotopeItem.getAttribute('data-layout') ?? 'masonry';
    let filter = isotopeItem.getAttribute('data-default-filter') ?? '*';
    let sort = isotopeItem.getAttribute('data-sort') ?? 'original-order';

    let initIsotope;
    if (typeof imagesLoaded !== 'undefined' && typeof Isotope !== 'undefined') {
      imagesLoaded(isotopeItem.querySelector('.isotope-container'), function() {
        initIsotope = new Isotope(isotopeItem.querySelector('.isotope-container'), {
          itemSelector: '.isotope-item',
          layoutMode: layout,
          filter: filter,
          sortBy: sort
        });
      });

      isotopeItem.querySelectorAll('.isotope-filters li').forEach(function(filters) {
        filters.addEventListener('click', function() {
          isotopeItem.querySelector('.isotope-filters .filter-active').classList.remove('filter-active');
          this.classList.add('filter-active');
          initIsotope.arrange({
            filter: this.getAttribute('data-filter')
          });
          if (typeof aosInit === 'function') {
            aosInit();
          }
        }, false);
      });
    }
  });

  /**
   * ============================================================
   * SWIPER SLIDERS
   * ============================================================
   */
  function initSwiper() {
    document.querySelectorAll(".init-swiper").forEach(function(swiperElement) {
      let config = JSON.parse(
        swiperElement.querySelector(".swiper-config").innerHTML.trim()
      );

      if (swiperElement.classList.contains("swiper-tab")) {
        initSwiperWithCustomPagination(swiperElement, config);
      } else {
        if (typeof Swiper !== 'undefined') {
          new Swiper(swiperElement, config);
        }
      }
    });
  }

  window.addEventListener("load", initSwiper);

  /**
   * ============================================================
   * FAQ TOGGLE
   * ============================================================
   */
  document.querySelectorAll('.faq-item h3, .faq-item .faq-toggle').forEach((faqItem) => {
    faqItem.addEventListener('click', () => {
      faqItem.parentNode.classList.toggle('faq-active');
    });
  });

  /**
   * ============================================================
   * HASH SCROLL CORRECTION
   * ============================================================
   */
  window.addEventListener('load', function(e) {
    if (window.location.hash) {
      if (document.querySelector(window.location.hash)) {
        setTimeout(() => {
          let section = document.querySelector(window.location.hash);
          let scrollMarginTop = getComputedStyle(section).scrollMarginTop;
          window.scrollTo({
            top: section.offsetTop - parseInt(scrollMarginTop),
            behavior: 'smooth'
          });
        }, 100);
      }
    }
  });

  /**
   * ============================================================
   * NAVMENU SCROLLSPY
   * ============================================================
   */
  let navmenulinks = document.querySelectorAll('.navmenu a');

  function navmenuScrollspy() {
    navmenulinks.forEach(navmenulink => {
      if (!navmenulink.hash) return;
      let section = document.querySelector(navmenulink.hash);
      if (!section) return;
      let position = window.scrollY + 200;
      if (position >= section.offsetTop && position <= (section.offsetTop + section.offsetHeight)) {
        document.querySelectorAll('.navmenu a.active').forEach(link => link.classList.remove('active'));
        navmenulink.classList.add('active');
      } else {
        navmenulink.classList.remove('active');
      }
    })
  }
  window.addEventListener('load', navmenuScrollspy);
  document.addEventListener('scroll', navmenuScrollspy);

  /**
   * ============================================================
   * CAROUSEL CLASS
   * ============================================================
   */
  class Carousel {
    constructor(containerSelector, interval = 5000) {
      this.slides = document.querySelectorAll(`${containerSelector} .carousel-slide`);
      this.interval = interval;
      this.currentIndex = 0;
      this.timer = null;
      this.init();
    }

    init() {
      this.slides.forEach((slide, index) => {
        if (index === 0) {
          slide.classList.add('active');
        } else if (index === 1) {
          slide.classList.add('next');
        } else {
          slide.classList.remove('active', 'exiting', 'next');
        }
      });
      this.startAutoPlay();
    }

    transitionToNext() {
      const nextIndex = (this.currentIndex + 1) % this.slides.length;
      this.transitionToIndex(nextIndex);
    }

    transitionToIndex(newIndex) {
      this.slides.forEach(slide => {
        slide.classList.remove('active', 'exiting', 'next');
      });
      this.slides[this.currentIndex].classList.add('exiting');
      this.slides[newIndex].classList.add('active');
      const nextNextIndex = (newIndex + 1) % this.slides.length;
      this.slides[nextNextIndex].classList.add('next');
      this.currentIndex = newIndex;
    }

    startAutoPlay() {
      this.timer = setInterval(() => {
        this.transitionToNext();
      }, this.interval);
    }

    stopAutoPlay() {
      clearInterval(this.timer);
    }
  }

  /**
   * ============================================================
   * INITIALIZE CAROUSEL
   * ============================================================
   */
  document.addEventListener('DOMContentLoaded', () => {
    const container = document.querySelector('.carousel-container');
    if (container) {
      const myCarousel = new Carousel('.carousel-container', 5000);
      container.addEventListener('mouseenter', () => myCarousel.stopAutoPlay());
      container.addEventListener('mouseleave', () => myCarousel.startAutoPlay());
    }
  });

  /**
   * ============================================================
   * EMAILJS INITIALIZATION
   * ============================================================
   */
  if (typeof emailjs !== 'undefined') {
    (function() {
      emailjs.init("GLvB9e1q7YgCuXOqJ");
    })();
  }

  /**
   * ============================================================
   * CONTACT FORM HANDLING
   * ============================================================
   */
  document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("contactForm");

    if (form) {
      form.addEventListener("submit", function(e) {
        e.preventDefault();

        const name = document.getElementById("name").value;
        const phone = document.getElementById("phone").value;
        const email = document.getElementById("email").value;
        const subject = document.getElementById("subject").value;
        const message = document.getElementById("message").value;

        const whatsappMessage = `New contact from:\nName: ${name}\nPhone: ${phone}\nEmail: ${email}\nSubject: ${subject}\nMessage: ${message}`;
        const phoneNumber = "254742524370";
        const whatsappUrl = `https://wa.me/${phoneNumber}?text=${encodeURIComponent(whatsappMessage)}`;

        function showMessage(msg, isSuccess) {
          const responseDiv = document.getElementById("response");
          if (responseDiv) {
            responseDiv.style.display = "block";
            responseDiv.style.position = "relative";
            responseDiv.style.padding = "10px";
            responseDiv.style.marginTop = "10px";
            responseDiv.style.borderRadius = "5px";
            responseDiv.style.fontWeight = "bold";
            responseDiv.style.fontSize = "14px";
            responseDiv.style.transition = "opacity 0.5s ease";

            if (isSuccess) {
              responseDiv.style.backgroundColor = "#d4edda";
              responseDiv.style.color = "#155724";
              responseDiv.style.border = "1px solid #c3e6cb";
            } else {
              responseDiv.style.backgroundColor = "#f8d7da";
              responseDiv.style.color = "#721c24";
              responseDiv.style.border = "1px solid #f5c6cb";
            }

            responseDiv.innerHTML = `
              ${msg}
              <button onclick="this.parentElement.style.display='none'" 
                      style="position: absolute; top: 5px; right: 10px; background: transparent; border: none; font-size: 20px; cursor: pointer;">
                &times;
              </button>
            `;
          }
        }

        // Submit the form via AJAX or open WhatsApp
        // For now, we'll show a success message
        showMessage("Thank you! Your message has been sent. We'll get back to you soon.", true);
        form.reset();
      });
    }
  });

  /**
   * ============================================================
   * CONTACT POPUP FUNCTIONALITY
   * ============================================================
   */

  // Show tooltip for floating contact button
  document.addEventListener('DOMContentLoaded', function() {
    setTimeout(function() {
      const label = document.getElementById('floatingLabel');
      if (label) {
        label.classList.add('show');
        setTimeout(function() {
          label.classList.remove('show');
        }, 5000);
      }
    }, 2000);

    // Check if popup has been shown before using sessionStorage
    const contactPopupElement = document.getElementById("contactPopup");
    
    if (contactPopupElement) {
      const contactPopup = new bootstrap.Modal(contactPopupElement);

      if (!sessionStorage.getItem('contactPopupShown')) {
        setTimeout(function() {
          contactPopup.show();
          sessionStorage.setItem('contactPopupShown', 'true');
        }, 3000);
      }
    }
  });

  /**
   * Open contact popup manually
   */
  function openContactPopup(showForm = false) {
    const contactPopupElement = document.getElementById("contactPopup");
    if (contactPopupElement) {
      const contactPopup = bootstrap.Modal.getOrCreateInstance(contactPopupElement);

      if (showForm) {
        showContactForm();
      } else {
        showContactIntro();
      }

      contactPopup.show();
    }
  }

  /**
   * Show the contact introduction
   */
  function showContactIntro() {
    const intro = document.getElementById("contactIntro");
    const form = document.getElementById("contactFormContainer");
    const icon = document.getElementById("contactPopupIcon");
    const title = document.getElementById("contactPopupTitle");
    const subtitle = document.getElementById("contactPopupSubtitle");

    if (intro) intro.style.display = "block";
    if (form) form.style.display = "none";
    if (icon) icon.innerHTML = "💬";
    if (title) title.innerText = "Let's Talk";
    if (subtitle) subtitle.innerText = "Have a question or need a digital solution?";

    // Re-trigger animation
    if (intro) {
      intro.style.animation = 'none';
      requestAnimationFrame(() => {
        intro.style.animation = 'fadeInUp 0.6s ease-out';
      });
    }
  }

  /**
   * Show the actual contact form
   */
  function showContactForm() {
    const intro = document.getElementById("contactIntro");
    const form = document.getElementById("contactFormContainer");
    const icon = document.getElementById("contactPopupIcon");
    const title = document.getElementById("contactPopupTitle");
    const subtitle = document.getElementById("contactPopupSubtitle");

    if (intro) intro.style.display = "none";
    if (form) form.style.display = "block";
    if (icon) icon.innerHTML = "✉️";
    if (title) title.innerText = "Contact Us";
    if (subtitle) subtitle.innerText = "Send us your message and we'll get back to you.";

    // Re-trigger animation
    if (form) {
      form.style.animation = 'none';
      requestAnimationFrame(() => {
        form.style.animation = 'fadeInUp 0.6s ease-out';
      });
    }
  }

  /**
   * ============================================================
   * EXPOSE FUNCTIONS TO GLOBAL SCOPE
   * ============================================================
   */
  window.openContactPopup = openContactPopup;
  window.showContactIntro = showContactIntro;
  window.showContactForm = showContactForm;
  window.mobileNavToogle = mobileNavToogle;

})();