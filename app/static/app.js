document.addEventListener('DOMContentLoaded', () => {
    // Table row clicking
    const rows = document.querySelectorAll('.clickable-row');
    rows.forEach(row => {
        row.addEventListener('click', () => {
            const href = row.getAttribute('data-href');
            if (href) {
                window.location.href = href;
            }
        });
    });

    // Search functionality
    const searchInput = document.getElementById('ticker-search');
    const searchBtn = document.getElementById('search-btn');

    function executeSearch() {
        const val = searchInput.value.trim().toUpperCase();
        if (val) {
            window.location.href = `/ticker/${val}`;
        }
    }

    if (searchInput && searchBtn) {
        searchBtn.addEventListener('click', executeSearch);
        searchInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                executeSearch();
            }
        });
    }

    // Trend filter functionality
    const trendFilter = document.getElementById('trend-filter');
    if (trendFilter) {
        // Read URL params to set initial state
        const urlParams = new URLSearchParams(window.location.search);
        const currentTrend = urlParams.get('trend');
        if (currentTrend) {
            trendFilter.value = currentTrend;
        }

        trendFilter.addEventListener('change', () => {
            const selected = trendFilter.value;
            const newUrl = new URL(window.location.href);
            if (selected === 'ALL') {
                newUrl.searchParams.delete('trend');
            } else {
                newUrl.searchParams.set('trend', selected);
            }
            window.location.href = newUrl.toString();
        });
    }
});
