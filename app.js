// ==========================================================================
// Cloudflare Edge Fabric — Apple Style React Application (app.js)
// ==========================================================================

const { useState, useEffect, useRef, useCallback } = React;

function App() {
  // Theme State
  const [theme, setTheme] = useState('dark');
  const [activeTab, setActiveTab] = useState('overview');

  // Interactive Controls State
  const [underAttackMode, setUnderAttackMode] = useState(false);
  const [autoMinify, setAutoMinify] = useState(true);
  const [cacheTTL, setCacheTTL] = useState(4); // Hours
  const [workersCount, setWorkersCount] = useState(42);

  // Live Metric Counter State
  const [metrics, setMetrics] = useState({
    requestsPerSec: 14820,
    avgLatency: 11.4,
    cacheHitRatio: 98.4,
    threatsBlocked: 4120
  });

  // Realtime Log Feed State
  const [logs, setLogs] = useState([
    { id: 1, time: '21:58:01', status: 200, method: 'GET', path: '/api/v1/worker-fetch', latency: '9ms', pop: 'ICN (Incheon)' },
    { id: 2, time: '21:58:02', status: 304, method: 'GET', path: '/static/app.js', latency: '4ms', pop: 'NRT (Tokyo)' },
    { id: 3, time: '21:58:03', status: 200, method: 'POST', path: '/functions/auth', latency: '14ms', pop: 'SJC (San Jose)' },
    { id: 4, time: '21:58:04', status: 200, method: 'GET', path: '/assets/style.css', latency: '3ms', pop: 'ICN (Incheon)' }
  ]);

  // Toast Notification State
  const [toast, setToast] = useState(null);

  // Trigger Toast helper
  const showToast = (message, icon = 'check-circle') => {
    setToast({ message, icon });
    setTimeout(() => {
      setToast(null);
    }, 3500);
  };

  // Toggle Theme
  const toggleTheme = () => {
    const newTheme = theme === 'dark' ? 'light' : 'dark';
    setTheme(newTheme);
    document.body.className = `${newTheme}-theme`;
    showToast(`Switched to ${newTheme.toUpperCase()} mode`, newTheme === 'dark' ? 'moon' : 'sun');
  };

  // Simulate Live Metric Pulsing & Logs Stream
  useEffect(() => {
    const interval = setInterval(() => {
      // Fluctuate metrics slightly for live feel
      setMetrics(prev => ({
        requestsPerSec: Math.floor(prev.requestsPerSec + (Math.random() * 300 - 150)),
        avgLatency: +(prev.avgLatency + (Math.random() * 0.4 - 0.2)).toFixed(1),
        cacheHitRatio: +(Math.min(99.9, Math.max(95.0, prev.cacheHitRatio + (Math.random() * 0.2 - 0.1)))).toFixed(1),
        threatsBlocked: prev.threatsBlocked + (Math.random() > 0.6 ? 1 : 0)
      }));

      // Add a random log entry periodically
      const pops = ['ICN (Incheon)', 'NRT (Tokyo)', 'SJC (San Jose)', 'FRA (Frankfurt)', 'LHR (London)'];
      const paths = ['/api/v2/kv-query', '/assets/logo.png', '/functions/deploy', '/edge/stream', '/pages/index.html'];
      const statuses = [200, 200, 200, 304, 200];

      const now = new Date();
      const timeStr = now.toTimeString().split(' ')[0];
      const newLog = {
        id: Date.now(),
        time: timeStr,
        status: statuses[Math.floor(Math.random() * statuses.length)],
        method: 'GET',
        path: paths[Math.floor(Math.random() * paths.length)],
        latency: `${Math.floor(Math.random() * 12 + 3)}ms`,
        pop: pops[Math.floor(Math.random() * pops.length)]
      };

      setLogs(prevLogs => [newLog, ...prevLogs.slice(0, 7)]);
    }, 2500);

    return () => clearInterval(interval);
  }, []);

  // Initialize Lucide Icons on mount & updates
  useEffect(() => {
    if (window.lucide) {
      window.lucide.createIcons();
    }
  });

  return (
    <div className="app-container">
      {/* Toast Popup Notification */}
      {toast && (
        <div className="toast-container">
          <div className="toast">
            <i data-lucide={toast.icon} style={{ color: 'var(--color-cf-orange)', width: 18, height: 18 }}></i>
            <span>{toast.message}</span>
          </div>
        </div>
      )}

      {/* Glass Top Navigation Bar */}
      <header className="navbar">
        <div className="nav-brand">
          <svg className="brand-icon" viewBox="0 0 24 24" fill="currentColor">
            <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
          </svg>
          <span>Cloudflare Fabric</span>
          <span className="brand-badge">Pages Native</span>
        </div>

        <ul className="nav-menu">
          <li 
            className={`nav-item ${activeTab === 'overview' ? 'active' : ''}`}
            onClick={() => setActiveTab('overview')}
          >
            Overview
          </li>
          <li 
            className={`nav-item ${activeTab === 'control' ? 'active' : ''}`}
            onClick={() => setActiveTab('control')}
          >
            Control Center
          </li>
          <li 
            className={`nav-item ${activeTab === 'regional' ? 'active' : ''}`}
            onClick={() => setActiveTab('regional')}
          >
            Edge PoP Network
          </li>
        </ul>

        <div className="nav-actions">
          <div className="live-pulse-container">
            <span className="pulse-dot"></span>
            <span>Edge Operational</span>
          </div>

          <button className="theme-toggle-btn" onClick={toggleTheme} title="Toggle Theme">
            <i data-lucide={theme === 'dark' ? 'sun' : 'moon'} style={{ width: 18, height: 18 }}></i>
          </button>
        </div>
      </header>

      {/* Main Dashboard Workspace */}
      <main className="dashboard-main">
        {/* Apple Keynote Style Hero Card */}
        <div className="hero-banner">
          <div className="hero-content">
            <div className="hero-subtitle">Designed for Cloudflare Pages</div>
            <h1 className="hero-title">Edge Native Architecture. Instant Speed.</h1>
            <p className="hero-description">
              서버가 없는 완전히 정적인(Serverless) React 프론트엔드 환경에서 Cloudflare Global Anycast 엣지 네트워크를 통해 초저지연 성능을 경험하세요.
            </p>
            <div className="hero-metrics">
              <div className="metric-pill">
                <span className="metric-value">{metrics.requestsPerSec.toLocaleString()}</span>
                <span className="metric-label">Req / sec (Global)</span>
              </div>
              <div className="metric-pill">
                <span className="metric-value">{metrics.avgLatency} ms</span>
                <span className="metric-label">Average Response Time</span>
              </div>
              <div className="metric-pill">
                <span className="metric-value">{metrics.cacheHitRatio}%</span>
                <span className="metric-label">Cache Hit Ratio</span>
              </div>
            </div>
          </div>

          <div className="hero-actions">
            <button 
              className="btn-primary" 
              onClick={() => showToast('Cache purged across 330+ edge locations!', 'zap')}
            >
              <i data-lucide="zap" style={{ width: 16, height: 16 }}></i>
              Purge Edge Cache
            </button>
            <button 
              className="btn-secondary"
              onClick={() => showToast('Deployment synced via Cloudflare Pages Workers', 'refresh-cw')}
            >
              <i data-lucide="refresh-cw" style={{ width: 16, height: 16 }}></i>
              Sync Status
            </button>
          </div>
        </div>

        {/* Bento Grid Layout */}
        <div className="bento-grid">
          {/* Chart Widget: Realtime Traffic Performance */}
          <div className="bento-card col-span-8">
            <div className="card-header">
              <div>
                <h2 className="card-title">
                  <i data-lucide="activity" style={{ color: 'var(--color-cf-orange)', width: 20, height: 20 }}></i>
                  Global Request Throughput
                </h2>
                <div className="card-subtitle">Real-time throughput metrics powered by Cloudflare Anycast</div>
              </div>
              <span className="card-tag">Live Feed</span>
            </div>
            <TrafficChart theme={theme} />
          </div>

          {/* Apple Control Center Widget */}
          <div className="bento-card col-span-4">
            <div className="card-header">
              <div>
                <h2 className="card-title">
                  <i data-lucide="sliders" style={{ color: 'var(--color-apple-blue)', width: 20, height: 20 }}></i>
                  Control Center
                </h2>
                <div className="card-subtitle">Edge configuration switches</div>
              </div>
              <span className="card-tag">Instant Sync</span>
            </div>

            <div className="control-group">
              <div className="control-row">
                <div className="control-info">
                  <span className="control-label">Under Attack Mode</span>
                  <span className="control-subtext">Enable JS Challenge globally</span>
                </div>
                <label className="switch">
                  <input 
                    type="checkbox" 
                    checked={underAttackMode} 
                    onChange={e => {
                      setUnderAttackMode(e.target.checked);
                      showToast(e.target.checked ? 'Under Attack Mode Activated' : 'Normal Security Restored', 'shield');
                    }} 
                  />
                  <span className="slider"></span>
                </label>
              </div>

              <div className="control-row">
                <div className="control-info">
                  <span className="control-label">Brotli Auto-Minify</span>
                  <span className="control-subtext">Compress HTML, CSS & JS</span>
                </div>
                <label className="switch">
                  <input 
                    type="checkbox" 
                    checked={autoMinify} 
                    onChange={e => {
                      setAutoMinify(e.target.checked);
                      showToast(`Auto-Minify ${e.target.checked ? 'Enabled' : 'Disabled'}`, 'file-text');
                    }} 
                  />
                  <span className="slider"></span>
                </label>
              </div>

              <div style={{ marginTop: '0.5rem' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.4rem' }}>
                  <span className="control-label">Edge Cache TTL</span>
                  <span style={{ fontSize: '0.85rem', fontWeight: 600, color: 'var(--color-cf-orange)' }}>
                    {cacheTTL} Hours
                  </span>
                </div>
                <input 
                  type="range" 
                  className="apple-range" 
                  min="1" 
                  max="24" 
                  value={cacheTTL}
                  onChange={e => setCacheTTL(e.target.value)}
                />
              </div>
            </div>
          </div>

          {/* Cloudflare Native Products Suite Bento */}
          <div className="bento-card col-span-8">
            <div className="card-header">
              <div>
                <h2 className="card-title">
                  <i data-lucide="layers" style={{ color: 'var(--color-apple-cyan)', width: 20, height: 20 }}></i>
                  Cloudflare Serverless Ecosystem
                </h2>
                <div className="card-subtitle">Zero-config serverless services bound to Pages</div>
              </div>
              <span className="card-tag">Native Binding</span>
            </div>

            <div className="products-mini-grid">
              <div className="product-item">
                <div className="product-head">
                  <div className="product-icon-wrap">
                    <i data-lucide="cpu" style={{ width: 20, height: 20 }}></i>
                  </div>
                  <span style={{ fontSize: '0.75rem', color: 'var(--color-apple-green)', fontWeight: 600 }}>Active</span>
                </div>
                <div className="product-title">Cloudflare Workers</div>
                <div className="product-desc">V8 isolate edge serverless execution without container cold starts.</div>
                <div className="product-stat">{workersCount} Functions</div>
              </div>

              <div className="product-item">
                <div className="product-head">
                  <div className="product-icon-wrap" style={{ background: 'rgba(0, 113, 227, 0.12)', color: 'var(--color-apple-blue)' }}>
                    <i data-lucide="database" style={{ width: 20, height: 20 }}></i>
                  </div>
                  <span style={{ fontSize: '0.75rem', color: 'var(--color-apple-green)', fontWeight: 600 }}>Ready</span>
                </div>
                <div className="product-title">KV & R2 Storage</div>
                <div className="product-desc">Global ultra-low latency Key-Value & S3-compatible Object store.</div>
                <div className="product-stat">1.4 GB / 0ms Read</div>
              </div>

              <div className="product-item">
                <div className="product-head">
                  <div className="product-icon-wrap" style={{ background: 'rgba(52, 199, 89, 0.12)', color: 'var(--color-apple-green)' }}>
                    <i data-lucide="globe" style={{ width: 20, height: 20 }}></i>
                  </div>
                  <span style={{ fontSize: '0.75rem', color: 'var(--color-apple-green)', fontWeight: 600 }}>Live</span>
                </div>
                <div className="product-title">Pages Functions</div>
                <div className="product-desc">Fullstack file-based API routing inside /functions directory.</div>
                <div className="product-stat">Native Direct</div>
              </div>

              <div className="product-item">
                <div className="product-head">
                  <div className="product-icon-wrap" style={{ background: 'rgba(175, 82, 222, 0.12)', color: 'var(--color-apple-purple)' }}>
                    <i data-lucide="shield-check" style={{ width: 20, height: 20 }}></i>
                  </div>
                  <span style={{ fontSize: '0.75rem', color: 'var(--color-apple-green)', fontWeight: 600 }}>Protected</span>
                </div>
                <div className="product-title">Turnstile & WAF</div>
                <div className="product-desc">Smart bot protection & CAPTCHA-free web application firewall.</div>
                <div className="product-stat">{metrics.threatsBlocked} Blocked</div>
              </div>
            </div>
          </div>

          {/* Realtime Live Terminal Log Feed */}
          <div className="bento-card col-span-4">
            <div className="card-header">
              <div>
                <h2 className="card-title">
                  <i data-lucide="terminal" style={{ color: 'var(--color-apple-green)', width: 20, height: 20 }}></i>
                  Edge Realtime Logs
                </h2>
                <div className="card-subtitle">Live request stream PoP PoI</div>
              </div>
              <span className="card-tag">Stream</span>
            </div>

            <div className="logs-console">
              {logs.map(log => (
                <div key={log.id} className="log-line">
                  <span className="log-time">{log.time}</span>
                  <span className={`log-status status-${log.status}`}>{log.status}</span>
                  <span className="log-msg">{log.path}</span>
                  <span className="log-latency">{log.latency}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Regional Network Status Table */}
          <div className="bento-card col-span-12">
            <div className="card-header">
              <div>
                <h2 className="card-title">
                  <i data-lucide="map-pin" style={{ color: 'var(--color-cf-orange)', width: 20, height: 20 }}></i>
                  Cloudflare PoP Regional Matrix
                </h2>
                <div className="card-subtitle">Latency performance across top East Asia & Global Edge nodes</div>
              </div>
              <span className="card-tag">330+ Cities</span>
            </div>

            <table className="region-table">
              <thead>
                <tr>
                  <th>Edge PoP Location</th>
                  <th>Node Code</th>
                  <th>HTTP/3 Status</th>
                  <th>Avg Ping Latency</th>
                  <th>Health Status</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td><div className="region-flag">🇰🇷 Seoul / Incheon, Korea</div></td>
                  <td><code>ICN</code></td>
                  <td>Enabled (QUIC)</td>
                  <td style={{ color: 'var(--color-apple-green)', fontWeight: 600 }}>2.4 ms</td>
                  <td><span className="live-pulse-container" style={{ padding: '2px 8px' }}>Operational</span></td>
                </tr>
                <tr>
                  <td><div className="region-flag">🇯🇵 Tokyo, Japan</div></td>
                  <td><code>NRT</code></td>
                  <td>Enabled (QUIC)</td>
                  <td style={{ color: 'var(--color-apple-green)', fontWeight: 600 }}>11.8 ms</td>
                  <td><span className="live-pulse-container" style={{ padding: '2px 8px' }}>Operational</span></td>
                </tr>
                <tr>
                  <td><div className="region-flag">🇸🇬 Singapore</div></td>
                  <td><code>SIN</code></td>
                  <td>Enabled (QUIC)</td>
                  <td style={{ color: 'var(--color-apple-green)', fontWeight: 600 }}>28.5 ms</td>
                  <td><span className="live-pulse-container" style={{ padding: '2px 8px' }}>Operational</span></td>
                </tr>
                <tr>
                  <td><div className="region-flag">🇺🇸 San Jose, USA</div></td>
                  <td><code>SJC</code></td>
                  <td>Enabled (QUIC)</td>
                  <td style={{ color: 'var(--color-apple-cyan)', fontWeight: 600 }}>110.2 ms</td>
                  <td><span className="live-pulse-container" style={{ padding: '2px 8px' }}>Operational</span></td>
                </tr>
                <tr>
                  <td><div className="region-flag">🇩🇪 Frankfurt, Germany</div></td>
                  <td><code>FRA</code></td>
                  <td>Enabled (QUIC)</td>
                  <td style={{ color: 'var(--color-apple-cyan)', fontWeight: 600 }}>142.0 ms</td>
                  <td><span className="live-pulse-container" style={{ padding: '2px 8px' }}>Operational</span></td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </main>

      {/* Serverless Native Footer */}
      <footer className="footer">
        <p>© 2026 Cloudflare Edge Fabric — Crafted with Apple UI Philosophy & React Serverless Static Architecture.</p>
        <p style={{ marginTop: '0.4rem' }}>
          Deploys natively to <a href="https://pages.cloudflare.com" target="_blank" rel="noreferrer">Cloudflare Pages</a> & Cloudflare Workers Network.
        </p>
      </footer>
    </div>
  );
}

// Chart.js Subcomponent for Smooth Glowing Edge Traffic Curve
function TrafficChart({ theme }) {
  const canvasRef = useRef(null);
  const chartInstanceRef = useRef(null);

  useEffect(() => {
    if (!canvasRef.current || !window.Chart) return;

    const ctx = canvasRef.current.getContext('2d');

    // Create Gradient Fill
    const gradient = ctx.createLinearGradient(0, 0, 0, 240);
    if (theme === 'dark') {
      gradient.addColorStop(0, 'rgba(243, 128, 32, 0.45)');
      gradient.addColorStop(1, 'rgba(243, 128, 32, 0.0)');
    } else {
      gradient.addColorStop(0, 'rgba(243, 128, 32, 0.35)');
      gradient.addColorStop(1, 'rgba(243, 128, 32, 0.02)');
    }

    const labels = ['21:40', '21:43', '21:46', '21:49', '21:52', '21:55', '21:58'];
    const dataPoints = [12400, 13100, 12800, 14200, 13900, 15100, 14820];

    if (chartInstanceRef.current) {
      chartInstanceRef.current.destroy();
    }

    const textColor = theme === 'dark' ? '#86868b' : '#6e6e73';
    const gridColor = theme === 'dark' ? 'rgba(255, 255, 255, 0.06)' : 'rgba(0, 0, 0, 0.05)';

    chartInstanceRef.current = new window.Chart(ctx, {
      type: 'line',
      data: {
        labels: labels,
        datasets: [{
          label: 'Requests / Sec',
          data: dataPoints,
          borderColor: '#F38020',
          borderWidth: 3,
          tension: 0.4,
          fill: true,
          backgroundColor: gradient,
          pointBackgroundColor: '#F38020',
          pointBorderColor: '#ffffff',
          pointHoverRadius: 6,
          pointRadius: 4
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            backgroundColor: theme === 'dark' ? 'rgba(20, 20, 25, 0.9)' : 'rgba(255, 255, 255, 0.9)',
            titleColor: theme === 'dark' ? '#fff' : '#000',
            bodyColor: '#F38020',
            borderColor: 'rgba(243, 128, 32, 0.3)',
            borderWidth: 1,
            padding: 10,
            displayColors: false,
            callbacks: {
              label: (context) => `${context.parsed.y.toLocaleString()} req/s`
            }
          }
        },
        scales: {
          x: {
            grid: { color: gridColor },
            ticks: { color: textColor, font: { family: '-apple-system, sans-serif', size: 11 } }
          },
          y: {
            grid: { color: gridColor },
            ticks: { color: textColor, font: { family: '-apple-system, sans-serif', size: 11 } }
          }
        }
      }
    });

    return () => {
      if (chartInstanceRef.current) {
        chartInstanceRef.current.destroy();
      }
    };
  }, [theme]);

  return (
    <div className="chart-container">
      <canvas ref={canvasRef}></canvas>
    </div>
  );
}

// Render React App
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);
