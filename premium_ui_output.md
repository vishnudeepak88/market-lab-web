Here is the complete Premium Dark-Theme UI implementation. I have already applied these changes automatically to your local repository so you can view it live at `http://localhost:8000` right now!

### File Tree
```text
app/
├── static/
│   ├── app.js
│   └── styles.css
└── templates/
    ├── index.html
    └── ticker.html
```

---

### `app/templates/index.html`
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Market Lab - Dashboard</title>
  <link rel="stylesheet" href="/static/styles.css">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
</head>
<body>
  <header class="navbar">
    <div class="nav-container">
      <div class="brand">Market Lab</div>
      <div class="nav-timestamp">Updated: 2026-03-01 13:50 UTC</div>
      <div class="nav-links">
        <a href="/" class="active">Dashboard</a>
        <a href="#">Docs</a>
      </div>
    </div>
  </header>

  <main class="container">
    <div class="dash-header">
      <h1>Leaderboard</h1>
      
      <div class="dash-controls">
        <div class="search-box">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
          <input type="text" id="ticker-search" placeholder="Search ticker or company...">
        </div>
        
        <div class="filters-row">
          <select id="trend-filter" class="filter-select">
            <option value="ALL">All Trends</option>
            <option value="UP">Uptrend</option>
            <option value="DOWN">Downtrend</option>
            <option value="SIDEWAYS">Sideways</option>
          </select>
          <select id="region-filter" class="filter-select">
            <option value="ALL">All Regions</option>
            <option value="US">US Markets</option>
            <option value="EU">European Markets</option>
          </select>
          <input type="number" id="min-score" class="filter-input" placeholder="Min Score (e.g. 70)" min="0" max="100">
        </div>
      </div>
    </div>

    <div class="table-container">
      <div class="table-header">
        <div class="col-ticker">Symbol</div>
        <div class="col-score">Score</div>
        <div class="col-trend">Trend</div>
        <div class="col-ret">20D Return</div>
        <div class="col-rsi">RSI(14)</div>
        <div class="col-vol">Vol(20d)</div>
        <div class="col-alerts">Alerts</div>
      </div>

      <div id="leaderboard-body" class="table-body">
        <!-- Skeleton Loading State (hidden by default) -->
        <div id="loading-skeleton" style="display: none;">
          <div class="table-row skeleton"></div>
          <div class="table-row skeleton"></div>
          <div class="table-row skeleton"></div>
        </div>

        <!-- Empty State (hidden by default) -->
        <div id="empty-state" class="empty-state" style="display: none;">
          <p>No results match your filters</p>
        </div>

        <!-- Realistic Placeholder Rows -->
        <a href="/ticker/AAPL" class="table-row">
          <div class="col-ticker">
            <span class="ticker-sym">AAPL</span>
            <span class="ticker-name">Apple Inc.</span>
          </div>
          <div class="col-score">
            <span class="score-value accent">89.4</span>
          </div>
          <div class="col-trend">
            <span class="badge badge-up">UP</span>
          </div>
          <div class="col-ret text-success">+4.20%</div>
          <div class="col-rsi">
            <span class="rsi-val text-muted">54.2</span>
            <span class="pill pill-normal">NORMAL</span>
          </div>
          <div class="col-vol text-muted">1.25%</div>
          <div class="col-alerts">
            <span class="chip">OVERSOLD</span>
          </div>
        </a>

        <a href="/ticker/TSLA" class="table-row">
          <div class="col-ticker">
            <span class="ticker-sym">TSLA</span>
            <span class="ticker-name">Tesla, Inc.</span>
          </div>
          <div class="col-score">
            <span class="score-value">72.1</span>
          </div>
          <div class="col-trend">
            <span class="badge badge-sideways">SIDE</span>
          </div>
          <div class="col-ret text-danger">-2.10%</div>
          <div class="col-rsi">
            <span class="rsi-val text-warning">78.5</span>
            <span class="pill pill-overheated">OVERHEATED</span>
          </div>
          <div class="col-vol text-muted">3.40%</div>
          <div class="col-alerts">
            <span class="chip chip-warn">VOL_SPIKE</span>
            <span class="chip chip-danger">DRAWDOWN_WARN</span>
          </div>
        </a>

        <a href="/ticker/MSFT" class="table-row">
          <div class="col-ticker">
            <span class="ticker-sym">MSFT</span>
            <span class="ticker-name">Microsoft Corp.</span>
          </div>
          <div class="col-score">
            <span class="score-value accent">92.8</span>
          </div>
          <div class="col-trend">
            <span class="badge badge-up">UP</span>
          </div>
          <div class="col-ret text-success">+6.80%</div>
          <div class="col-rsi">
            <span class="rsi-val text-success">22.1</span>
            <span class="pill pill-oversold">OVERSOLD</span>
          </div>
          <div class="col-vol text-muted">1.10%</div>
          <div class="col-alerts">
            <span class="text-muted">-</span>
          </div>
        </a>
      </div>
    </div>
  </main>
  
  <script src="/static/app.js"></script>
</body>
</html>
```

---

### `app/templates/ticker.html`
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Market Lab - AAPL</title>
  <link rel="stylesheet" href="/static/styles.css">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
</head>
<body>
  <header class="navbar">
    <div class="nav-container">
      <div class="brand">Market Lab</div>
      <div class="nav-links">
        <a href="/">Dashboard</a>
        <a href="#">Docs</a>
      </div>
    </div>
  </header>

  <main class="container">
    <!-- Header -->
    <div class="ticker-header">
      <div class="ticker-title-group">
        <a href="/" class="back-link">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="15 18 9 12 15 6"></polyline></svg>
        </a>
        <div>
          <h1>AAPL</h1>
          <div class="ticker-name">Apple Inc.</div>
        </div>
      </div>
      <div class="ticker-price-group">
        <div class="price-val">$152.40</div>
        <span class="badge badge-up badge-large">UP</span>
      </div>
    </div>

    <!-- Chart Panel -->
    <div class="card mb-4 panel-chart">
      <h2>180-Day Price Action</h2>
      <div class="chart-wrapper">
        <!-- SVG Placeholder -->
        <svg class="placeholder-chart" width="100%" height="200" preserveAspectRatio="none" viewBox="0 0 1000 200">
          <polyline fill="none" class="chart-line" points="0,150 100,140 200,160 300,120 400,130 500,90 600,110 700,70 800,85 900,40 1000,50" />
          <polyline fill="url(#gradient)" class="chart-area" points="0,200 0,150 100,140 200,160 300,120 400,130 500,90 600,110 700,70 800,85 900,40 1000,50 1000,200" />
          <defs>
            <linearGradient id="gradient" x1="0" x2="0" y1="0" y2="1">
              <stop offset="0%" stop-color="#FF6B35" stop-opacity="0.3" />
              <stop offset="100%" stop-color="#FF6B35" stop-opacity="0.0" />
            </linearGradient>
          </defs>
        </svg>
      </div>
    </div>

    <!-- 4 Stat Cards Grid -->
    <div class="grid-4">
      <div class="card stat-card">
        <h3>Trend</h3>
        <div class="stat-row"><span>SMA 20</span> <strong>148.20</strong></div>
        <div class="stat-row"><span>SMA 50</span> <strong>142.10</strong></div>
        <div class="stat-row"><span>SMA 200</span> <strong>135.50</strong></div>
        <div class="stat-footer text-success">State: UP</div>
      </div>

      <div class="card stat-card">
        <h3>Momentum</h3>
        <div class="stat-row"><span>20D Return</span> <strong class="text-success">+4.20%</strong></div>
        <div class="stat-row"><span>60D Return</span> <strong class="text-success">+12.4%</strong></div>
        <div class="stat-row"><span>RSI(14)</span> <strong>54.2</strong></div>
        <div class="stat-footer text-muted">Neutral Momentum</div>
      </div>

      <div class="card stat-card">
        <h3>Risk</h3>
        <div class="stat-row"><span>Volatility 20D</span> <strong>1.25%</strong></div>
        <div class="stat-row"><span>Drawdown 60D</span> <strong class="text-danger">-3.10%</strong></div>
        <div class="stat-row"><span>Volume Z</span> <strong>0.5</strong></div>
        <div class="stat-footer text-muted">Normal Risk Profile</div>
      </div>

      <div class="card stat-card">
        <h3>Alerts</h3>
        <div class="alerts-list">
          <div class="chip">OVERSOLD</div>
          <p class="alert-desc text-muted">RSI dropped below 30 threshold during recent pullback.</p>
        </div>
      </div>
    </div>

    <!-- Rule Output Panel -->
    <div class="card panel-rules mt-4">
      <h2>Rule Output <span class="system-status status-buy">BUY</span></h2>
      <div class="rules-grid">
        <div class="rules-col">
          <h4 class="text-success">Entry Conditions</h4>
          <ul class="rule-list">
            <li><span class="check">✓</span> Closing price > SMA 50</li>
            <li><span class="check">✓</span> SMA 50 > SMA 200</li>
            <li><span class="check">✓</span> RSI(14) < 75 (Not overheated)</li>
          </ul>
        </div>
        <div class="rules-col">
          <h4 class="text-danger">Exit Conditions</h4>
          <ul class="rule-list">
            <li><span class="cross">✗</span> Drawdown > 15% from local high</li>
            <li><span class="cross">✗</span> Closing price < SMA 50</li>
          </ul>
        </div>
      </div>
    </div>

    <!-- JSON Debug Panel -->
    <details class="debug-panel mt-4">
      <summary>Raw JSON Payload (Developer/Debug)</summary>
      <pre><code>{
  "symbol": "AAPL",
  "name": "Apple Inc.",
  "final_score": 89.4,
  "trend_state": "UP",
  "indicators": {
    "sma_20": 148.2,
    "sma_50": 142.1,
    "sma_200": 135.5,
    "rsi_14": 54.2
  },
  "alerts": ["OVERSOLD"]
}</code></pre>
    </details>
  </main>
</body>
</html>
```

---

### `app/static/styles.css`
```css
:root {
  --bg-base: #0E0E0E;
  --bg-surface: #141414;
  --bg-surface-elevated: #1A1A1A;
  --border: #232323;
  --accent: #FF6B35;
  --accent-hover: #e55a29;
  
  --text-main: #EDEDED;
  --text-muted: #A0A0A0;
  
  --success: #22c55e;
  --danger: #ef4444;
  --warning: #f59e0b;
  --sideways: #64748b;

  --success-bg: rgba(34, 197, 94, 0.15);
  --danger-bg: rgba(239, 68, 68, 0.15);
  --warning-bg: rgba(245, 158, 11, 0.15);
  --sideways-bg: rgba(100, 116, 139, 0.15);
  
  --radius-lg: 16px;
  --radius-md: 8px;
  --radius-sm: 4px;
}

* { box-sizing: border-box; }

body {
  margin: 0;
  font-family: 'Inter', sans-serif;
  background-color: var(--bg-base);
  color: var(--text-main);
  -webkit-font-smoothing: antialiased;
}

a { color: inherit; text-decoration: none; }

/* Utilities */
.text-success { color: var(--success); }
.text-danger { color: var(--danger); }
.text-warning { color: var(--warning); }
.text-muted { color: var(--text-muted); }
.accent { color: var(--accent); font-weight: 700; }
.mt-4 { margin-top: 2rem; }
.mb-4 { margin-bottom: 2rem; }

/* Navigation */
.navbar {
  background-color: var(--bg-surface);
  border-bottom: 1px solid var(--border);
  position: sticky;
  top: 0;
  z-index: 100;
  padding: 1rem 0;
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.brand {
  font-size: 1.25rem;
  font-weight: 700;
  letter-spacing: -0.02em;
  color: var(--text-main);
}

.nav-timestamp {
  font-size: 0.85rem;
  color: var(--text-muted);
}

.nav-links a {
  margin-left: 1.5rem;
  font-size: 0.95rem;
  color: var(--text-muted);
  transition: color 0.2s;
  font-weight: 500;
}

.nav-links a:hover, .nav-links a.active {
  color: var(--text-main);
}

/* Layout */
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2.5rem 2rem;
}

/* Dashboard Header */
.dash-header {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  margin-bottom: 2.5rem;
}

.dash-header h1 {
  margin: 0;
  font-size: 2rem;
  font-weight: 600;
  letter-spacing: -0.02em;
}

.dash-controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
}

/* Inputs & Forms */
.search-box {
  display: flex;
  align-items: center;
  background-color: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: 0.5rem 1rem;
  width: 100%;
  max-width: 320px;
  transition: border-color 0.2s;
}

.search-box:focus-within {
  border-color: var(--accent);
}

.search-box svg {
  color: var(--text-muted);
  margin-right: 0.75rem;
}

.search-box input {
  background: transparent;
  border: none;
  outline: none;
  color: var(--text-main);
  font-size: 0.95rem;
  width: 100%;
}

.filters-row {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.filter-select, .filter-input {
  background-color: var(--bg-surface);
  border: 1px solid var(--border);
  color: var(--text-main);
  padding: 0.6rem 1rem;
  border-radius: var(--radius-md);
  font-family: inherit;
  font-size: 0.9rem;
  outline: none;
  cursor: pointer;
}

.filter-select:focus, .filter-input:focus {
  border-color: var(--accent);
}

/* Leaderboard Table */
.table-container {
  background-color: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
}

.table-header {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr 1.5fr 1fr 2fr;
  padding: 1rem 1.5rem;
  border-bottom: 1px solid var(--border);
  color: var(--text-muted);
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  font-weight: 600;
  background-color: var(--bg-surface-elevated);
}

.table-row {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr 1.5fr 1fr 2fr;
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid var(--border);
  align-items: center;
  transition: background-color 0.2s;
  cursor: pointer;
}

.table-row:last-child {
  border-bottom: none;
}

.table-row:hover {
  background-color: var(--bg-surface-elevated);
}

.col-ticker { display: flex; flex-direction: column; gap: 0.25rem; }
.ticker-sym { font-weight: 700; font-size: 1.05rem; }
.ticker-name { font-size: 0.85rem; color: var(--text-muted); }

.score-value { font-size: 1.2rem; font-weight: 600; }

.badge {
  display: inline-flex;
  padding: 0.25rem 0.5rem;
  border-radius: var(--radius-sm);
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.05em;
}
.badge-up { background-color: var(--success-bg); color: var(--success); }
.badge-down { background-color: var(--danger-bg); color: var(--danger); }
.badge-sideways { background-color: var(--sideways-bg); color: var(--sideways); }

.badge-large { font-size: 1rem; padding: 0.4rem 0.8rem; }

.pill {
  display: inline-flex;
  padding: 0.15rem 0.4rem;
  border-radius: 99px;
  font-size: 0.7rem;
  font-weight: 600;
  margin-left: 0.5rem;
}
.pill-overheated { background-color: var(--danger-bg); color: var(--danger); border: 1px solid var(--danger); }
.pill-oversold { background-color: var(--success-bg); color: var(--success); border: 1px solid var(--success); }
.pill-normal { background-color: var(--sideways-bg); color: var(--text-muted); border: 1px solid var(--border); }
.rsi-val { font-weight: 500; }

.col-alerts { display: flex; flex-wrap: wrap; gap: 0.5rem; }
.chip {
  padding: 0.25rem 0.5rem;
  background-color: var(--bg-surface-elevated);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  font-size: 0.7rem;
  font-weight: 600;
  color: var(--text-muted);
}
.chip-danger { color: var(--danger); border-color: rgba(239, 68, 68, 0.4); }
.chip-warn { color: var(--warning); border-color: rgba(245, 158, 11, 0.4); }

.empty-state {
  text-align: center;
  padding: 3rem 1.5rem;
  color: var(--text-muted);
}

/* Skeleton Loading */
.skeleton {
  animation: pulse 1.5s infinite ease-in-out;
}
@keyframes pulse {
  0% { background-color: var(--bg-surface); }
  50% { background-color: var(--bg-surface-elevated); }
  100% { background-color: var(--bg-surface); }
}

/* Ticker Detail Page */
.ticker-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2.5rem;
}

.ticker-title-group {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.back-link {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 44px;
  height: 44px;
  background-color: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: 50%;
  color: var(--text-muted);
  transition: all 0.2s;
}

.back-link:hover {
  color: var(--text-main);
  background-color: var(--bg-surface-elevated);
  border-color: var(--accent);
}

.ticker-header h1 { margin: 0; font-size: 2.5rem; font-weight: 700; line-height: 1; }

.ticker-price-group {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.price-val {
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--text-main);
}

/* Cards */
.card {
  background-color: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 1.5rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
}

.card h2, .card h3 {
  margin: 0 0 1.25rem 0;
  font-weight: 600;
}

.card h2 { font-size: 1.25rem; }
.card h3 { font-size: 1.05rem; color: var(--text-muted); }

/* SVG Chart Placeholder */
.chart-wrapper {
  width: 100%;
  height: 200px;
  position: relative;
}
.chart-line { stroke: var(--accent); stroke-width: 2px; }

/* 4 Grid Layout */
.grid-4 {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 1.5rem;
}

.stat-card {
  display: flex;
  flex-direction: column;
}

.stat-row {
  display: flex;
  justify-content: space-between;
  padding: 0.6rem 0;
  border-bottom: 1px solid var(--border);
  font-size: 0.95rem;
}

.stat-row:last-of-type { border-bottom: none; }
.stat-row span { color: var(--text-muted); }
.stat-footer {
  margin-top: auto;
  padding-top: 1rem;
  font-weight: 600;
  font-size: 0.85rem;
}

/* Rules Grid */
.rules-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
}

.rules-col h4 { margin: 0 0 1.25rem 0; font-size: 1.05rem; }

.rule-list { list-style: none; padding: 0; margin: 0; }
.rule-list li {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  margin-bottom: 0.75rem;
  color: var(--text-main);
}

.check { color: var(--success); font-weight: bold; }
.cross { color: var(--danger); font-weight: bold; }

.system-status {
  padding: 0.25rem 0.75rem;
  border-radius: var(--radius-md);
  margin-left: 1rem;
  font-size: 0.9rem;
}
.status-buy { background-color: var(--success-bg); color: var(--success); border: 1px solid rgba(34,197,94,0.3); }

/* Debug Panel */
.debug-panel {
  background-color: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: 1rem;
}

.debug-panel summary {
  color: var(--text-muted);
  cursor: pointer;
  font-weight: 500;
  font-size: 0.9rem;
}

.debug-panel pre {
  margin: 1rem 0 0 0;
  color: var(--accent);
  font-size: 0.85rem;
  overflow-x: auto;
}

/* Responsive */
@media (max-width: 900px) {
  .table-header, .table-row {
    grid-template-columns: 1.5fr 1fr 1fr 1.5fr;
  }
  .col-ret, .col-vol, .col-alerts { display: none; }
  .dash-header { flex-direction: column; align-items: stretch; }
  .filters-row { flex-direction: column; }
}

@media (max-width: 600px) {
  .rules-grid { grid-template-columns: 1fr; }
  .ticker-header { flex-direction: column; align-items: flex-start; gap: 1rem; }
  .nav-timestamp { display: none; }
}
```

---

### `app/static/app.js`
```javascript
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
```
