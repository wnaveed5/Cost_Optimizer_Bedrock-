import React from 'react';
import { NavLink } from 'react-router-dom';
import './Sidebar.css';

const Sidebar = () => {
  const navItems = [
    {
      path: '/',
      label: 'Dashboard',
      icon: '📊'
    },
    {
      path: '/cost-analysis',
      label: 'Cost Analysis',
      icon: '💰'
    },
    {
      path: '/recommendations',
      label: 'AI Recommendations',
      icon: '🤖'
    },
    {
      path: '/metrics',
      label: 'Metrics',
      icon: '📈'
    },
    {
      path: '/settings',
      label: 'Settings',
      icon: '⚙️'
    }
  ];

  return (
    <aside className="sidebar">
      <nav>
        <ul className="sidebar-nav">
          {navItems.map((item) => (
            <li key={item.path}>
              <NavLink
                to={item.path}
                className={({ isActive }) => isActive ? 'active' : ''}
              >
                <span className="nav-icon">{item.icon}</span>
                {item.label}
              </NavLink>
            </li>
          ))}
        </ul>
      </nav>
      
      <div className="sidebar-footer">
        <div className="cluster-info">
          <h4>Cluster Info</h4>
          <p>cost-optimizer-cluster</p>
          <p>us-west-2</p>
        </div>
      </div>
    </aside>
  );
};

export default Sidebar; 