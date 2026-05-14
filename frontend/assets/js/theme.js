// Dark mode theme switcher - Load immediately
(function() {
    const html = document.documentElement;
    
    // Initialize theme from localStorage or system preference
    function initTheme() {
        const saved = localStorage.getItem('theme');
        const isDark = saved ? saved === 'dark' : window.matchMedia('(prefers-color-scheme: dark)').matches;
        setTheme(isDark ? 'dark' : 'light');
    }

    window.setTheme = function(theme) {
        const themeToggle = document.getElementById('theme-toggle');
        if (theme === 'dark') {
            html.setAttribute('data-theme', 'dark');
            if (themeToggle) themeToggle.textContent = '☀️';
            localStorage.setItem('theme', 'dark');
        } else {
            html.removeAttribute('data-theme');
            if (themeToggle) themeToggle.textContent = '🌙';
            localStorage.setItem('theme', 'light');
        }
    }

    window.toggleTheme = function() {
        const current = html.getAttribute('data-theme');
        setTheme(current === 'dark' ? 'light' : 'dark');
    }

    // Wait for DOM to be ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initTheme);
    } else {
        initTheme();
    }

    // Set up event listener
    document.addEventListener('DOMContentLoaded', function() {
        const themeToggle = document.getElementById('theme-toggle');
        if (themeToggle) {
            themeToggle.addEventListener('click', window.toggleTheme);
        }
    });
})();
