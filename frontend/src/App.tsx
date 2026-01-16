import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Homepage from './pages/Homepage';
import ScenarioBuilder from './pages/ScenarioBuilder';
import SimulationPage from './pages/SimulationPage';
import Leaderboard from './pages/Leaderboard';
import './index.css';

function App() {
  const [darkMode] = useState(true); // Always dark mode for this app

  return (
    <Router>
      <div className="app" style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
        {/* Header / Navigation */}
        <nav style={{
          background: 'var(--bg-secondary)',
          borderBottom: '1px solid var(--border-color)',
          padding: 'var(--spacing-md) var(--spacing-xl)',
        }}>
          <div className="container" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <Link to="/" style={{ fontSize: '1.5rem', fontWeight: 700, color: 'var(--text-primary)', textDecoration: 'none' }}>
              🌍 Disaster Prep Simulator
            </Link>
            <div style={{ display: 'flex', gap: 'var(--spacing-lg)' }}>
              <Link to="/" className="nav-link">Home</Link>
              <Link to="/scenarios" className="nav-link">Scenarios</Link>
              <Link to="/leaderboard" className="nav-link">Leaderboard</Link>
            </div>
          </div>
        </nav>

        {/* Main Content */}
        <main style={{ flex: 1 }}>
          <Routes>
            <Route path="/" element={<Homepage />} />
            <Route path="/scenarios" element={<ScenarioBuilder />} />
            <Route path="/simulation/:id" element={<SimulationPage />} />
            <Route path="/leaderboard" element={<Leaderboard />} />
          </Routes>
        </main>

        {/* Footer */}
        <footer style={{
          background: 'var(--bg-secondary)',
          borderTop: '1px solid var(--border-color)',
          padding: 'var(--spacing-lg)',
          textAlign: 'center'
        }}>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.875rem' }}>
            © 2026 Disaster Preparedness Simulator | Powered by Reinforcement Learning
          </p>
        </footer>
      </div>

      <style>{`
        .nav-link {
          color: var(--text-secondary);
          font-weight: 500;
          transition: color var(--transition-fast);
        }
        .nav-link:hover {
          color: var(--color-primary);
        }
      `}</style>
    </Router>
  );
}

export default App;
