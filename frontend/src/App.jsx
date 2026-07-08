import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import AgentChat from './pages/AgentChat';
import { Briefcase, MessageSquare } from 'lucide-react';
import './App.css'; // Optional extra App styling

function App() {
  return (
    <Router>
      <div className="app-container" style={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
        {/* Navigation Bar */}
        <nav className="glass-panel" style={{ 
          margin: '1rem', 
          padding: '1rem 2rem', 
          display: 'flex', 
          justifyContent: 'space-between',
          alignItems: 'center',
          position: 'sticky',
          top: '1rem',
          zIndex: 50
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', fontWeight: 'bold', fontSize: '1.25rem', color: 'var(--accent-primary)' }}>
            <Briefcase size={24} />
            Job Agent Suite
          </div>
          <div style={{ display: 'flex', gap: '1.5rem' }}>
            <Link to="/" style={{ color: 'var(--text-primary)', textDecoration: 'none', fontWeight: 500, display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <Briefcase size={18} /> Dashboard
            </Link>
            <Link to="/chat" style={{ color: 'var(--text-primary)', textDecoration: 'none', fontWeight: 500, display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <MessageSquare size={18} /> AI Agent
            </Link>
          </div>
        </nav>

        {/* Main Content */}
        <main style={{ flex: 1, padding: '0 1rem 2rem 1rem', maxWidth: '1200px', margin: '0 auto', width: '100%' }}>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/chat" element={<AgentChat />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
