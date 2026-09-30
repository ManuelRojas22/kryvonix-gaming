/**
 * VEXOR GAMING - GSAP Animations
 * Handles all scroll-triggered and interaction animations
 * Respects prefers-reduced-motion
 */

(function() {
  'use strict';

  // Check for reduced motion preference
  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const isMobile = window.innerWidth < 768;

  // Register GSAP plugins
  if (typeof gsap !== 'undefined' && typeof ScrollTrigger !== 'undefined') {
    gsap.registerPlugin(ScrollTrigger);
  }

  /**
   * Initialize all animations
   */
  function initAnimations() {
    if (prefersReducedMotion) {
      // Still set initial states but skip animations
      setInitialStates();
      return;
    }

    // Hero animations
    animateHero();

    // Product cards on scroll
    animateProductCards();

    // Section headers
    animateSectionHeaders();

    // Counter animations
    animateCounters();

    // Floating elements
    animateFloatingElements();

    // Button hover effects
    initButtonHoverEffects();

    // Card hover effects
    initCardHoverEffects();

    // Parallax effects
    initParallaxEffects();

    // Reveal on scroll for generic elements
    initScrollReveal();
  }

  /**
   * Set initial states for reduced motion
   */
  function setInitialStates() {
    gsap.set('[data-gsap-hero]', { opacity: 1, y: 0 });
    gsap.set('.product-card', { opacity: 1, y: 0 });
    gsap.set('[data-gsap-counter]', { opacity: 1 });
    gsap.set('[data-gsap-reveal]', { opacity: 1, y: 0 });
  }

  /**
   * Hero section animations
   */
  function animateHero() {
    const heroTitle = document.querySelector('[data-gsap-hero="title"]');
    const heroSubtitle = document.querySelector('[data-gsap-hero="subtitle"]');
    const heroButtons = document.querySelector('[data-gsap-hero="buttons"]');
    const heroStats = document.querySelector('[data-gsap-hero="stats"]');
    const heroVisual = document.querySelector('[data-gsap-hero="visual"]');

    if (!heroTitle && !heroSubtitle && !heroButtons) return;

    const tl = gsap.timeline({
      defaults: { ease: 'power3.out', duration: 0.8 },
      scrollTrigger: {
        trigger: 'section:first-of-type',
        start: 'top top',
        end: 'bottom top',
        toggleActions: 'play none none reverse',
      }
    });

    if (heroTitle) {
      tl.from(heroTitle, {
        opacity: 0,
        y: 40,
        duration: 1,
      }, 0);
    }

    if (heroSubtitle) {
      tl.from(heroSubtitle, {
        opacity: 0,
        y: 30,
        duration: 0.8,
      }, 0.15);
    }

    if (heroButtons) {
      tl.from(heroButtons.children, {
        opacity: 0,
        y: 30,
        stagger: 0.1,
        duration: 0.6,
      }, 0.3);
    }

    if (heroStats) {
      tl.from(heroStats.children, {
        opacity: 0,
        y: 30,
        stagger: 0.08,
        duration: 0.6,
      }, 0.5);
    }

    if (heroVisual) {
      tl.from(heroVisual, {
        opacity: 0,
        x: 60,
        scale: 0.95,
        duration: 1,
        ease: 'power2.out',
      }, 0.2);
    }
  }

  /**
   * Product cards stagger animation on scroll
   */
  function animateProductCards() {
    const cards = gsap.utils.toArray('.product-card:not([data-gsap-animated])');

    if (cards.length === 0) return;

    cards.forEach((card, index) => {
      card.dataset.gsapAnimated = 'true';

      gsap.from(card, {
        opacity: 0,
        y: 50,
        duration: 0.6,
        ease: 'power2.out',
        scrollTrigger: {
          trigger: card,
          start: 'top 85%',
          end: 'bottom 20%',
          toggleActions: 'play none none reverse',
          once: true, // Only animate once
        },
        delay: index * 0.05, // Stagger effect
      });
    });
  }

  /**
   * Section headers animation
   */
  function animateSectionHeaders() {
    const headers = gsap.utils.toArray('section header, .section-header');

    headers.forEach(header => {
      const title = header.querySelector('h2, h3');
      const subtitle = header.querySelector('p');
      const action = header.querySelector('a:last-child');

      const tl = gsap.timeline({
        scrollTrigger: {
          trigger: header,
          start: 'top 80%',
          toggleActions: 'play none none reverse',
        }
      });

      if (title) {
        tl.from(title, {
          opacity: 0,
          y: 30,
          duration: 0.6,
          ease: 'power2.out',
        });
      }

      if (subtitle) {
        tl.from(subtitle, {
          opacity: 0,
          y: 20,
          duration: 0.5,
        }, '-=0.3');
      }

      if (action) {
        tl.from(action, {
          opacity: 0,
          x: -20,
          duration: 0.4,
        }, '-=0.2');
      }
    });
  }

  /**
   * Counter number animations
   */
  function animateCounters() {
    const counters = gsap.utils.toArray('[data-gsap-counter]');

    counters.forEach(counter => {
      const target = parseFloat(counter.dataset.gsapCounter) || 0;
      const suffix = counter.dataset.gsapSuffix || '';
      const duration = parseFloat(counter.dataset.gsapDuration) || 2;
      const decimals = parseInt(counter.dataset.gsapDecimals) || 0;

      ScrollTrigger.create({
        trigger: counter,
        start: 'top 85%',
        onEnter: () => animateCounter(counter, target, suffix, duration, decimals),
        once: true,
      });
    });
  }

  function animateCounter(element, target, suffix, duration, decimals) {
    const obj = { value: 0 };
    gsap.to(obj, {
      value: target,
      duration: duration,
      ease: 'power2.out',
      onUpdate: () => {
        element.textContent = obj.value.toFixed(decimals) + suffix;
      },
      onComplete: () => {
        element.textContent = target.toFixed(decimals) + suffix;
      }
    });
  }

  /**
   * Floating elements animation
   */
  function animateFloatingElements() {
    const floaters = gsap.utils.toArray('[data-gsap-float]');

    floaters.forEach((el, index) => {
      const intensity = parseFloat(el.dataset.gsapFloat) || 20;
      const duration = parseFloat(el.dataset.gsapDuration) || 3 + index * 0.5;

      gsap.to(el, {
        y: -intensity,
        duration: duration,
        ease: 'sine.inOut',
        yoyo: true,
        repeat: -1,
        delay: index * 0.3,
      });
    });
  }

  /**
   * Button hover micro-interactions
   */
  function initButtonHoverEffects() {
    const buttons = document.querySelectorAll('button:not([data-gsap-no-hover]), a.btn-primary, a.btn-secondary, .product-card button');

    buttons.forEach(btn => {
      if (btn.dataset.gsapHoverInitialized) return;
      btn.dataset.gsapHoverInitialized = 'true';

      let tl;

      btn.addEventListener('mouseenter', () => {
        if (prefersReducedMotion) return;

        tl = gsap.timeline({ defaults: { duration: 0.2, ease: 'power2.out' } });
        tl.to(btn, { scale: 1.02 });
        tl.to(btn, { boxShadow: '0 10px 25px -5px rgba(14, 165, 233, 0.4)', duration: 0.3 }, 0);
      });

      btn.addEventListener('mouseleave', () => {
        if (prefersReducedMotion) return;

        gsap.to(btn, {
          scale: 1,
          boxShadow: btn.classList.contains('btn-primary') ? '0 10px 25px -5px rgba(14, 165, 233, 0.3)' : 'none',
          duration: 0.3,
          ease: 'power2.out',
        });
      });

      btn.addEventListener('mousedown', () => {
        if (prefersReducedMotion) return;
        gsap.to(btn, { scale: 0.98, duration: 0.1 });
      });

      btn.addEventListener('mouseup', () => {
        if (prefersReducedMotion) return;
        gsap.to(btn, { scale: 1.02, duration: 0.1 });
      });
    });
  }

  /**
   * Product card hover effects
   */
  function initCardHoverEffects() {
    const cards = document.querySelectorAll('.product-card');

    cards.forEach(card => {
      if (card.dataset.gsapHoverInitialized) return;
      card.dataset.gsapHoverInitialized = 'true';

      const image = card.querySelector('img');
      const badges = card.querySelector('.absolute.top-3');
      const quickAdd = card.querySelector('.absolute.bottom-3');

      card.addEventListener('mouseenter', () => {
        if (prefersReducedMotion) return;

        gsap.to(card, { y: -8, boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.25)', duration: 0.3, ease: 'power2.out' });

        if (image) {
          gsap.to(image, { scale: 1.05, duration: 0.5, ease: 'power2.out' });
        }

        if (badges) {
          gsap.fromTo(badges.children,
            { opacity: 0, x: -10 },
            { opacity: 1, x: 0, stagger: 0.05, duration: 0.2, ease: 'power2.out' }
          );
        }

        if (quickAdd) {
          gsap.to(quickAdd, { opacity: 1, y: 0, duration: 0.2, ease: 'power2.out' });
        }
      });

      card.addEventListener('mouseleave', () => {
        if (prefersReducedMotion) return;

        gsap.to(card, { y: 0, boxShadow: '0 1px 2px 0 rgba(0, 0, 0, 0.05)', duration: 0.3, ease: 'power2.out' });

        if (image) {
          gsap.to(image, { scale: 1, duration: 0.5, ease: 'power2.out' });
        }

        if (quickAdd) {
          gsap.to(quickAdd, { opacity: 0, y: 8, duration: 0.2, ease: 'power2.in' });
        }
      });
    });
  }

  /**
   * Parallax effects for hero and sections
   */
  function initParallaxEffects() {
    if (isMobile) return; // Skip on mobile for performance

    const parallaxElements = gsap.utils.toArray('[data-gsap-parallax]');

    parallaxElements.forEach(el => {
      const speed = parseFloat(el.dataset.gsapParallax) || 0.3;

      gsap.to(el, {
        yPercent: -50 * speed,
        ease: 'none',
        scrollTrigger: {
          trigger: el,
          start: 'top bottom',
          end: 'bottom top',
          scrub: true,
        }
      });
    });
  }

  /**
   * Generic scroll reveal
   */
  function initScrollReveal() {
    const revealElements = gsap.utils.toArray('[data-gsap-reveal]:not([data-gsap-revealed])');

    revealElements.forEach(el => {
      el.dataset.gsapRevealed = 'true';

      const direction = el.dataset.gsapReveal || 'up';
      const delay = parseFloat(el.dataset.gsapDelay) || 0;
      const duration = parseFloat(el.dataset.gsapDuration) || 0.6;

      let fromVars = { opacity: 0, duration, ease: 'power2.out' };

      switch (direction) {
        case 'up':
          fromVars.y = 40;
          break;
        case 'down':
          fromVars.y = -40;
          break;
        case 'left':
          fromVars.x = -40;
          break;
        case 'right':
          fromVars.x = 40;
          break;
        case 'scale':
          fromVars.scale = 0.9;
          break;
      }

      gsap.from(el, {
        ...fromVars,
        scrollTrigger: {
          trigger: el,
          start: 'top 85%',
          toggleActions: 'play none none reverse',
        },
        delay,
      });
    });
  }

  /**
   * Stagger children animation helper
   */
  function staggerChildren(container, selector, options = {}) {
    const children = container.querySelectorAll(selector);
    if (children.length === 0) return;

    const defaults = {
      opacity: 0,
      y: 20,
      duration: 0.5,
      stagger: 0.1,
      ease: 'power2.out',
    };

    gsap.from(children, {
      ...defaults,
      ...options,
      scrollTrigger: {
        trigger: container,
        start: 'top 80%',
        toggleActions: 'play none none reverse',
        ...options.scrollTrigger,
      },
    });
  }

  /**
   * Refresh ScrollTrigger on layout changes
   */
  function refreshScrollTriggers() {
    if (typeof ScrollTrigger !== 'undefined') {
      ScrollTrigger.refresh();
    }
  }

  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initAnimations);
  } else {
    initAnimations();
  }

  // Re-initialize on dynamic content load
  document.addEventListener('vexor:content-loaded', () => {
    setTimeout(initAnimations, 100);
  });

  // Refresh on window resize (debounced)
  let resizeTimeout;
  window.addEventListener('resize', () => {
    clearTimeout(resizeTimeout);
    resizeTimeout = setTimeout(refreshScrollTriggers, 250);
  });

  // Expose globally
  window.VexorAnimations = {
    init: initAnimations,
    refresh: refreshScrollTriggers,
    staggerChildren,
    animateCounter,
  };
})();