import React from 'react';
import './Header.css';

const Header = () => {
  return (
    <header className="header">
      <div>
        <h1>Cost Optimization Dashboard</h1>
        <p className="header-subtitle">AI-Driven AWS EKS Cost Management</p>
      </div>
      <div className="header-status">
        <div className="status">
          <div className="status-indicator"></div>
          <span>Agent Active</span>
        </div>
        <div className="header-actions">
          <button className="btn btn-secondary btn-sm">
            Refresh
          </button>
        </div>
      </div>
    </header>
  );
};

export default Header; 