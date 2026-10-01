/**
 * VEXOR GAMING - Theme Management
 * Handles dark/light mode with localStorage persistence and flash prevention
 */

(function() {
  'use strict';

  const THEME_KEY = 'vexor-theme';
  const DARK_CLASS = 'dark';
  const STORAGE_EVENT = 'storage';

  /**
   * Get the initial theme preference
   * Priority: localStorage > system preference > light
   */
  function getInitialTheme() {
    // Check localStorage first
    const stored = localStorage.getItem(THEME_KEY);
    if (stored !== null) {
      return stored === 'dark';
    }

    // Check system preference
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
      return true;
    }

    return false;
  }

  /**
   * Apply theme to document element
   * This runs immediately to prevent flash
   */
  function applyTheme(isDark) {
    const html = document.documentElement;
    if (isDark) {
      html.classList.add(DARK_CLASS);
    } else {
      html.classList.remove(DARK_CLASS);
    }
    html.setAttribute('data-theme', isDark ? 'dark' : 'light');
  }

  /**
   * Save theme to localStorage
   */
  function saveTheme(isDark) {
    try {
      localStorage.setItem(THEME_KEY, isDark ? 'dark' : 'light');
    } catch (e) {
      // localStorage might be disabled or full
      console.warn('Could not save theme preference:', e);
    }
  }

  /**
   * Toggle theme
   */
  function toggleTheme() {
    const isDark = !document.documentElement.classList.contains(DARK_CLASS);
    applyTheme(isDark);
    saveTheme(isDark);
    dispatchThemeChangeEvent(isDark);
  }

  /**
   * Set specific theme
   */
  function setTheme(isDark) {
    applyTheme(isDark);
    saveTheme(isDark);
    dispatchThemeChangeEvent(isDark);
  }

  /**
   * Dispatch custom event for other components
   */
  function dispatchThemeChangeEvent(isDark) {
    window.dispatchEvent(new CustomEvent('themechange', {
      detail: { isDark, theme: isDark ? 'dark' : 'light' }
    }));
  }

  /**
   * Initialize theme on page load
   * This runs as early as possible
   */
  function initTheme() {
    const isDark = getInitialTheme();
    applyTheme(isDark);

    // Listen for system preference changes
    if (window.matchMedia) {
      const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
      mediaQuery.addEventListener('change', (e) => {
        // Only auto-switch if user hasn't set a preference
        const stored = localStorage.getItem(THEME_KEY);
        if (stored === null) {
          applyTheme(e.matches);
          dispatchThemeChangeEvent(e.matches);
        }
      });
    }

    // Listen for storage changes (other tabs)
    window.addEventListener(STORAGE_EVENT, (e) => {
      if (e.key === THEME_KEY && e.newValue !== null) {
        const isDark = e.newValue === 'dark';
        applyTheme(isDark);
        dispatchThemeChangeEvent(isDark);
      }
    });
  }

  // Run immediately to prevent flash
  initTheme();

  // Expose globally for Alpine.js
  window.VexorTheme = {
    toggle: toggleTheme,
    set: setTheme,
    get: () => document.documentElement.classList.contains(DARK_CLASS),
    init: initTheme,
  };

  // Alpine.js component
  document.addEventListener('alpine:init', () => {
    Alpine.data('theme', () => ({
      isDark: document.documentElement.classList.contains(DARK_CLASS),

      initTheme() {
        this.isDark = window.VexorTheme.get();
        // Listen for theme changes from other sources
        window.addEventListener('themechange', (e) => {
          this.isDark = e.detail.isDark;
        });
      },

      toggleTheme() {
        window.VexorTheme.toggle();
      },
    }));
  });
})();