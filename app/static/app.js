document.addEventListener('DOMContentLoaded', () => {
    // Basic search filtering for table view elements
    const searchInput = document.getElementById('ticker-search');
    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            const term = e.target.value.toLowerCase();
            const rows = document.querySelectorAll('.table-row');
            let hasResults = false;

            rows.forEach(row => {
                if (row.classList.contains('skeleton')) return; // Ignore skeletons

                const ticker = row.querySelector('.ticker-sym')?.textContent.toLowerCase() || '';
                const name = row.querySelector('.ticker-name')?.textContent.toLowerCase() || '';

                if (ticker.includes(term) || name.includes(term)) {
                    row.style.display = 'grid';
                    hasResults = true;
                } else {
                    row.style.display = 'none';
                }
            });

            // Toggle empty state
            const emptyState = document.getElementById('empty-state');
            if (emptyState) {
                emptyState.style.display = hasResults ? 'none' : 'block';
            }
        });
    }

    // Basic dropdown filtering (Trend)
    const trendSelect = document.getElementById('trend-filter');
    if (trendSelect) {
        trendSelect.addEventListener('change', (e) => {
            const filterValue = e.target.value;
            const rows = document.querySelectorAll('.table-row');
            let hasResults = false;

            rows.forEach(row => {
                if (row.classList.contains('skeleton')) return;

                const trendBadge = row.querySelector('.badge')?.textContent || 'ALL';

                // Show if ALL is selected, or if badge text matches selected option
                if (filterValue === 'ALL' || trendBadge === filterValue) {
                    row.style.display = 'grid';
                    hasResults = true;
                } else {
                    row.style.display = 'none';
                }
            });

            const emptyState = document.getElementById('empty-state');
            if (emptyState) {
                emptyState.style.display = hasResults ? 'none' : 'block';
            }
        });
    }
});
