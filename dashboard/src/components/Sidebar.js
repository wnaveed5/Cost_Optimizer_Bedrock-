import React from 'react';
import { NavLink } from 'react-router-dom';
import './Sidebar.css';

const Sidebar = () => {
  const navItems = [
    {
      path: '/',
      label: 'Dashboard',
      icon: 'D'
    },
    {
      path: '/cost-analysis',
      label: 'Cost Analysis',
      icon: 'C'
    },
    {
      path: '/recommendations',
      label: 'AI Recommendations',
      icon: 'A'
    },
    {
      path: '/metrics',
      label: 'Metrics',
      icon: 'M'
    },
    {
      path: '/settings',
      label: 'Settings',
      icon: 'S'
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