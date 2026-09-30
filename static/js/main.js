/**
 * VEXOR GAMING - Main JavaScript
 * Lightweight interactivity: mobile menu, modals, cart drawer, search, etc.
 */

(function() {
  'use strict';

  /**
   * Mobile Menu Toggle
   */
  function initMobileMenu() {
    const menuBtn = document.querySelector('[data-mobile-menu-btn]');
    const menuPanel = document.querySelector('[data-mobile-menu-panel]');
    const menuOverlay = document.querySelector('[data-mobile-menu-overlay]');
    const closeBtn = document.querySelector('[data-mobile-menu-close]');

    if (!menuBtn || !menuPanel) return;

    function openMenu() {
      menuPanel.classList.remove('translate-x-full');
      menuOverlay?.classList.remove('hidden');
      document.body.style.overflow = 'hidden';
      menuBtn.setAttribute('aria-expanded', 'true');
      trapFocus(menuPanel);
    }

    function closeMenu() {
      menuPanel.classList.add('translate-x-full');
      menuOverlay?.classList.add('hidden');
      document.body.style.overflow = '';
      menuBtn.setAttribute('aria-expanded', 'false');
      menuBtn.focus();
    }

    menuBtn.addEventListener('click', openMenu);
    closeBtn?.addEventListener('click', closeMenu);
    menuOverlay?.addEventListener('click', closeMenu);

    // Close on escape
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && !menuPanel.classList.contains('translate-x-full')) {
        closeMenu();
      }
    });

    // Close on link click
    menuPanel.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', closeMenu);
    });
  }

  /**
   * Focus trap for modals/drawers
   */
  function trapFocus(element) {
    const focusableElements = element.querySelectorAll(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );
    const firstElement = focusableElements[0];
    const lastElement = focusableElements[focusableElements.length - 1];

    firstElement?.focus();

    element.addEventListener('keydown', function handleTab(e) {
      if (e.key !== 'Tab') return;

      if (e.shiftKey) {
        if (document.activeElement === firstElement) {
          e.preventDefault();
          lastElement?.focus();
        }
      } else {
        if (document.activeElement === lastElement) {
          e.preventDefault();
          firstElement?.focus();
        }
      }
    });
  }

  /**
   * Cart Drawer (for future cart app)
   */
  function initCartDrawer() {
    const cartBtn = document.querySelector('[data-cart-btn]');
    const cartDrawer = document.querySelector('[data-cart-drawer]');
    const cartOverlay = document.querySelector('[data-cart-overlay]');
    const cartClose = document.querySelector('[data-cart-close]');

    if (!cartBtn || !cartDrawer) return;

    function openCart() {
      cartDrawer.classList.remove('translate-x-full');
      cartOverlay?.classList.remove('hidden');
      document.body.style.overflow = 'hidden';
      cartBtn.setAttribute('aria-expanded', 'true');
      trapFocus(cartDrawer);
    }

    function closeCart() {
      cartDrawer.classList.add('translate-x-full');
      cartOverlay?.classList.add('hidden');
      document.body.style.overflow = '';
      cartBtn.setAttribute('aria-expanded', 'false');
      cartBtn.focus();
    }

    cartBtn.addEventListener('click', openCart);
    cartClose?.addEventListener('click', closeCart);
    cartOverlay?.addEventListener('click', closeCart);

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && !cartDrawer.classList.contains('translate-x-full')) {
        closeCart();
      }
    });
  }

  /**
   * Search Autocomplete (placeholder for future)
   */
  function initSearchAutocomplete() {
    const searchInputs = document.querySelectorAll('input[type="search"]');

    searchInputs.forEach(input => {
      let debounceTimer;
      const resultsContainer = document.createElement('div');
      resultsContainer.className = 'absolute top-full left-0 right-0 mt-1 bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg shadow-lg hidden z-50 max-h-96 overflow-y-auto';
      resultsContainer.setAttribute('role', 'listbox');
      input.parentNode.style.position = 'relative';
      input.parentNode.appendChild(resultsContainer);

      input.addEventListener('input', () => {
        clearTimeout(debounceTimer);
        const query = input.value.trim();

        if (query.length < 2) {
          resultsContainer.classList.add('hidden');
          return;
        }

        debounceTimer = setTimeout(() => {
          // Future: fetch suggestions from API
          // fetch(`/api/search/suggest/?q=${encodeURIComponent(query)}`)
          //   .then(res => res.json())
          //   .then(data => renderSuggestions(data, resultsContainer));
        }, 300);
      });

      input.addEventListener('focus', () => {
        if (input.value.trim().length >= 2) {
          resultsContainer.classList.remove('hidden');
        }
      });

      document.addEventListener('click', (e) => {
        if (!input.parentNode.contains(e.target)) {
          resultsContainer.classList.add('hidden');
        }
      });
    });
  }

  /**
   * Quantity Input Component
   */
  function initQuantityInputs() {
    document.querySelectorAll('[data-quantity-input]').forEach(wrapper => {
      const input = wrapper.querySelector('input[type="number"]');
      const decrementBtn = wrapper.querySelector('[data-quantity-decrement]');
      const incrementBtn = wrapper.querySelector('[data-quantity-increment]');
      const min = parseInt(input.min) || 1;
      const max = parseInt(input.max) || 99;

      function updateValue(delta) {
        let value = parseInt(input.value) || min;
        value = Math.max(min, Math.min(max, value + delta));
        input.value = value;
        input.dispatchEvent(new Event('change', { bubbles: true }));
      }

      decrementBtn?.addEventListener('click', () => updateValue(-1));
      incrementBtn?.addEventListener('click', () => updateValue(1));

      input.addEventListener('change', () => {
        let value = parseInt(input.value) || min;
        value = Math.max(min, Math.min(max, value));
        input.value = value;
      });

      input.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowUp') {
          e.preventDefault();
          updateValue(1);
        } else if (e.key === 'ArrowDown') {
          e.preventDefault();
          updateValue(-1);
        }
      });
    });
  }

  /**
   * Toast Notifications
   */
  function showToast(message, type = 'info', duration = 4000) {
    const container = getOrCreateToastContainer();
    const toast = document.createElement('div');
    toast.className = `toast toast-${type} flex items-center gap-3 px-4 py-3 rounded-lg shadow-lg transform translate-x-full transition-transform duration-300`;
    toast.setAttribute('role', 'alert');
    toast.setAttribute('aria-live', 'polite');

    const icons = {
      success: '<svg class="w-5 h-5 text-green-500" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"/></svg>',
      error: '<svg class="w-5 h-5 text-red-500" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"/></svg>',
      warning: '<svg class="w-5 h-5 text-yellow-500" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z"/></svg>',
      info: '<svg class="w-5 h-5 text-blue-500" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z"/></svg>',
    };

    const colors = {
      success: 'bg-green-50 dark:bg-green-900/30 border-green-200 dark:border-green-800 text-green-800 dark:text-green-200',
      error: 'bg-red-50 dark:bg-red-900/30 border-red-200 dark:border-red-800 text-red-800 dark:text-red-200',
      warning: 'bg-yellow-50 dark:bg-yellow-900/30 border-yellow-200 dark:border-yellow-800 text-yellow-800 dark:text-yellow-200',
      info: 'bg-blue-50 dark:bg-blue-900/30 border-blue-200 dark:border-blue-800 text-blue-800 dark:text-blue-200',
    };

    toast.className += ` ${colors[type]} border`;
    toast.innerHTML = `${icons[type]}<span class="flex-1">${message}</span><button class="ml-4 text-current opacity-50 hover:opacity-100" aria-label="Cerrar"><svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg></button>`;

    toast.querySelector('button').addEventListener('click', () => removeToast(toast));
    container.appendChild(toast);

    // Animate in
    requestAnimationFrame(() => {
      toast.classList.remove('translate-x-full');
    });

    // Auto remove
    setTimeout(() => removeToast(toast), duration);

    return toast;
  }

  function getOrCreateToastContainer() {
    let container = document.querySelector('[data-toast-container]');
    if (!container) {
      container = document.createElement('div');
      container.setAttribute('data-toast-container', '');
      container.className = 'fixed top-4 right-4 z-50 flex flex-col gap-2 pointer-events-none';
      document.body.appendChild(container);
    }
    return container;
  }

  function removeToast(toast) {
    toast.classList.add('translate-x-full', 'opacity-0');
    setTimeout(() => toast.remove(), 300);
  }

  /**
   * Add to Cart (placeholder for future cart app)
   */
  function initAddToCart() {
    document.querySelectorAll('[data-add-to-cart]').forEach(btn => {
      btn.addEventListener('click', async (e) => {
        e.preventDefault();

        const productId = btn.dataset.addToCart;
        const originalText = btn.innerHTML;

        btn.disabled = true;
        btn.innerHTML = '<svg class="animate-spin -ml-1 mr-2 h-5 w-5" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg> Añadiendo...';

        try {
          // Future: await fetch('/cart/add/', { method: 'POST', body: JSON.stringify({ product_id: productId }) });
          await new Promise(resolve => setTimeout(resolve, 1000)); // Simulate
          showToast('Producto añadido al carrito', 'success');
        } catch (err) {
          showToast('Error al añadir al carrito', 'error');
        } finally {
          btn.disabled = false;
          btn.innerHTML = originalText;
        }
      });
    });
  }

  /**
   * Lazy load images with IntersectionObserver
   */
  function initLazyImages() {
    if ('loading' in HTMLImageElement.prototype) {
      // Native lazy loading supported
      document.querySelectorAll('img[loading="lazy"]').forEach(img => {
        img.loading = 'lazy';
      });
      return;
    }

    // Fallback for older browsers
    const imageObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const img = entry.target;
          if (img.dataset.src) {
            img.src = img.dataset.src;
            img.removeAttribute('data-src');
          }
          imageObserver.unobserve(img);
        }
      });
    }, { rootMargin: '50px' });

    document.querySelectorAll('img[data-src]').forEach(img => {
      imageObserver.observe(img);
    });
  }

  /**
   * Smooth scroll for anchor links
   */
  function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
      anchor.addEventListener('click', (e) => {
        const targetId = anchor.getAttribute('href');
        if (targetId === '#') return;

        const target = document.querySelector(targetId);
        if (target) {
          e.preventDefault();
          target.scrollIntoView({ behavior: 'smooth', block: 'start' });
          target.focus({ preventScroll: true });
        }
      });
    });
  }

  /**
   * Copy to clipboard helper
   */
  function copyToClipboard(text, successMessage = 'Copiado al portapapeles') {
    return navigator.clipboard.writeText(text).then(() => {
      showToast(successMessage, 'success');
      return true;
    }).catch(() => {
      showToast('Error al copiar', 'error');
      return false;
    });
  }

  /**
   * Initialize all components
   */
  function init() {
    initMobileMenu();
    initCartDrawer();
    initSearchAutocomplete();
    initQuantityInputs();
    initAddToCart();
    initLazyImages();
    initSmoothScroll();

    // Expose toast globally
    window.VexorToast = { show: showToast };
  }

  // Run on DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  // Re-initialize on dynamic content
  document.addEventListener('vexor:content-loaded', init);
})();