/**
* Template Name: EasyFolio
* Template URL: https://bootstrapmade.com/easyfolio-bootstrap-portfolio-template/
* Updated: Feb 21 2025 with Bootstrap v5.3.3
* Author: BootstrapMade.com
* License: https://bootstrapmade.com/license/
*/

(function() {
  "use strict";

  /**
   * Apply .scrolled class to the body as the page is scrolled down
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
   * Mobile nav toggle
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

  /**
   * Hide mobile nav on same-page/hash links
   */
  document.querySelectorAll('#navmenu a').forEach(navmenu => {
    navmenu.addEventListener('click', () => {
      if (document.querySelector('.mobile-nav-active')) {
        mobileNavToogle();
      }
    });

  });

  /**
   * Toggle mobile nav dropdowns
   */
  document.querySelectorAll('.navmenu .toggle-dropdown').forEach(navmenu => {
    navmenu.addEventListener('click', function(e) {
      e.preventDefault();
      this.parentNode.classList.toggle('active');
      this.parentNode.nextElementSibling.classList.toggle('dropdown-active');
      e.stopImmediatePropagation();
    });
  });

  /**
   * Scroll top button
   */
  let scrollTop = document.querySelector('.scroll-top');

  function toggleScrollTop() {
    if (scrollTop) {
      window.scrollY > 100 ? scrollTop.classList.add('active') : scrollTop.classList.remove('active');
    }
  }
  scrollTop.addEventListener('click', (e) => {
    e.preventDefault();
    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    });
  });

  window.addEventListener('load', toggleScrollTop);
  document.addEventListener('scroll', toggleScrollTop);

  /**
   * Animation on scroll function and init
   */
  function aosInit() {
    AOS.init({
      duration: 600,
      easing: 'ease-in-out',
      once: true,
      mirror: false
    });
  }
  window.addEventListener('load', aosInit);

  /**
   * Animate the skills items on reveal
   */
  let skillsAnimation = document.querySelectorAll('.skills-animation');
  skillsAnimation.forEach((item) => {
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
  });

  /**
   * Initiate glightbox
   */
  const glightbox = GLightbox({
    selector: '.glightbox'
  });

  /**
   * Init isotope layout and filters
   */
  document.querySelectorAll('.isotope-layout').forEach(function(isotopeItem) {
    let layout = isotopeItem.getAttribute('data-layout') ?? 'masonry';
    let filter = isotopeItem.getAttribute('data-default-filter') ?? '*';
    let sort = isotopeItem.getAttribute('data-sort') ?? 'original-order';

    let initIsotope;
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

  });

  /**
   * Init swiper sliders
   */
  function initSwiper() {
    document.querySelectorAll(".init-swiper").forEach(function(swiperElement) {
      let config = JSON.parse(
        swiperElement.querySelector(".swiper-config").innerHTML.trim()
      );

      if (swiperElement.classList.contains("swiper-tab")) {
        initSwiperWithCustomPagination(swiperElement, config);
      } else {
        new Swiper(swiperElement, config);
      }
    });
  }

  window.addEventListener("load", initSwiper);

  /**
   * Frequently Asked Questions Toggle
   */
  document.querySelectorAll('.faq-item h3, .faq-item .faq-toggle').forEach((faqItem) => {
    faqItem.addEventListener('click', () => {
      faqItem.parentNode.classList.toggle('faq-active');
    });
  });

  /**
   * Correct scrolling position upon page load for URLs containing hash links.
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
   * Navmenu Scrollspy
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

})();

class Carousel {
  constructor(containerSelector, interval = 5000) {
    this.slides = document.querySelectorAll(`${containerSelector} .carousel-slide`);
    this.interval = interval;
    this.currentIndex = 0;
    this.timer = null;

    this.init();
  }

  init() {
    // Set initial states
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
    // Clear all classes first
    this.slides.forEach(slide => {
      slide.classList.remove('active', 'exiting', 'next');
    });

    // Set current slide to exiting
    this.slides[this.currentIndex].classList.add('exiting');

    // Set new slide to active
    this.slides[newIndex].classList.add('active');

    // Set next slide in queue
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

// Initialize carousel
document.addEventListener('DOMContentLoaded', () => {
  const myCarousel = new Carousel('.carousel-container', 5000);

  // Optional: Pause on hover
  const container = document.querySelector('.carousel-container');
  container.addEventListener('mouseenter', () => myCarousel.stopAutoPlay());
  container.addEventListener('mouseleave', () => myCarousel.startAutoPlay());
});

// Initialize EmailJS
(function(){
  emailjs.init("GLvB9e1q7YgCuXOqJ");
})();

document.addEventListener("DOMContentLoaded", function() {
  const form = document.getElementById("contactForm");

  if (form) {
    form.addEventListener("submit", function(e){
      e.preventDefault();

      const name = document.getElementById("name").value;
      const phone = document.getElementById("phone").value;
      const email = document.getElementById("email").value;
      const subject = document.getElementById("subject").value;
      const message = document.getElementById("message").value;

      const whatsappMessage = `New contact from:\nName: ${name}\nPhone: ${phone}\nEmail: ${email}\nSubject: ${subject}\nMessage: ${message}`;

      // Optional: Send to WhatsApp silently (via WhatsApp API you cannot really send silently unless using a server or Twilio/Business API)
      // This just builds the link but doesn’t open it
      const phoneNumber = "254742524370";
      const whatsappUrl = `https://wa.me/${phoneNumber}?text=${encodeURIComponent(whatsappMessage)}`;
      // Optionally, log or fetch to your own server to handle this

      // Send email to admin
      const toAdmin = emailjs.send("service_gjegbzl", "template_0de245k", {
        from_name: name,
        reply_to: email,
        phone: phone,
        subject: subject,
        message: message
      });

      // Send confirmation to client
      const toClient = emailjs.send("service_gjegbzl", "template_yj1kc78", {
        from_name: name,
        reply_to: email,
        message: message
      });

      Promise.all([toAdmin, toClient])
        .then(function(response) {
          showMessage("Message sent successfully! Confirm your email.", true);
          form.reset();
        })
        .catch(function(error) {
          showMessage("Failed to send message. Please try again.", false);
          console.error("EmailJS Error:", error);
        });
    });
  }

  // Function to show success or error message with close button
  function showMessage(msg, isSuccess) {
    const responseDiv = document.getElementById("response");
    responseDiv.style.display = "block";
    responseDiv.style.position = "relative";
    responseDiv.style.padding = "10px";
    responseDiv.style.marginTop = "10px";
    responseDiv.style.borderRadius = "5px";
    responseDiv.style.fontWeight = "bold";
    responseDiv.style.fontSize = "14px";
    responseDiv.style.transition = "opacity 0.5s ease";

    if (isSuccess) {
      responseDiv.style.backgroundColor = "#d4edda"; // green
      responseDiv.style.color = "#155724";
      responseDiv.style.border = "1px solid #c3e6cb";
    } else {
      responseDiv.style.backgroundColor = "#f8d7da"; // red
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
});


