import React from 'react';
import { useQuery } from 'react-query';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, AreaChart, Area } from 'recharts';
import './Metrics.css';

const mockMetricsData = [
  { timestamp: '2024-01-01 00:00', cpu: 65, memory: 72, network: 45, disk: 30 },
  { timestamp: '2024-01-01 06:00', cpu: 58, memory: 68, network: 42, disk: 28 },
  { timestamp: '2024-01-01 12:00', cpu: 78, memory: 85, network: 65, disk: 45 },
  { timestamp: '2024-01-01 18:00', cpu: 82, memory: 88, network: 72, disk: 52 },
  { timestamp: '2024-01-02 00:00', cpu: 70, memory: 75, network: 48, disk: 35 },
  { timestamp: '2024-01-02 06:00', cpu: 62, memory: 70, network: 44, disk: 32 },
  { timestamp: '2024-01-02 12:00', cpu: 75, memory: 82, network: 68, disk: 48 },
  { timestamp: '2024-01-02 18:00', cpu: 79, memory: 86, network: 75, disk: 55 }
];

const mockNodeMetrics = [
  {
    name: 'node-1',
    instanceType: 't3.large',
    cpu: 65,
    memory: 72,
    pods: 8,
    status: 'healthy'
  },
  {
    name: 'node-2',
    instanceType: 't3.large',
    cpu: 58,
    memory: 68,
    pods: 6,
    status: 'healthy'
  },
  {
    name: 'node-3',
    instanceType: 't3.medium',
    cpu: 45,
    memory: 52,
    pods: 4,
    status: 'healthy'
  }
];

const Metrics = () => {
  const { data: metricsData, isLoading: metricsLoading } = useQuery('metricsData', () => {
    return new Promise(resolve => {
      setTimeout(() => resolve(mockMetricsData), 600);
    });
  });

  const { data: nodeMetrics, isLoading: nodeLoading } = useQuery('nodeMetrics', () => {
    return new Promise(resolve => {
      setTimeout(() => resolve(mockNodeMetrics), 800);
    });
  });

  if (metricsLoading || nodeLoading) {
    return (
      <div className="loading">
        <div className="spinner"></div>
      </div>
    );
  }

  return (
    <div className="metrics-page">
      <div className="page-header">
        <h2>Cluster Metrics</h2>
        <p>Real-time monitoring and performance metrics</p>
      </div>

      {/* Overview Stats */}
      <div className="grid grid-4 mb-6">
        <div className="stats-card">
          <h3>3</h3>
          <p>Active Nodes</p>
        </div>
        <div className="stats-card">
          <h3>18</h3>
          <p>Running Pods</p>
        </div>
        <div className="stats-card">
          <h3>65%</h3>
          <p>Avg CPU Usage</p>
        </div>
        <div className="stats-card">
          <h3>72%</h3>
          <p>Avg Memory Usage</p>
        </div>
      </div>

      {/* Resource Utilization Charts */}
      <div className="grid grid-2 mb-6">
        <div className="card">
          <div className="card-header">
            <h3 className="card-title">CPU & Memory Utilization</h3>
            <p className="card-subtitle">24-hour resource usage trends</p>
          </div>
          <div className="chart-container">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={metricsData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="timestamp" />
                <YAxis />
                <Tooltip />
                <Area type="monotone" dataKey="cpu" stackId="1" stroke="#8884d8" fill="#8884d8" name="CPU" />
                <Area type="monotone" dataKey="memory" stackId="1" stroke="#82ca9d" fill="#82ca9d" name="Memory" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="card">
          <div className="card-header">
            <h3 className="card-title">Network & Disk I/O</h3>
            <p className="card-subtitle">Network and storage performance</p>
          </div>
          <div className="chart-container">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={metricsData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="timestamp" />
                <YAxis />
                <Tooltip />
                <Line type="monotone" dataKey="network" stroke="#ffc658" name="Network" />
                <Line type="monotone" dataKey="disk" stroke="#ff7300" name="Disk" />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Node Details */}
      <div className="card">
        <div className="card-header">
          <h3 className="card-title">Node Performance</h3>
          <button className="btn btn-primary">Refresh</button>
        </div>
        <table className="table">
          <thead>
            <tr>
              <th>Node Name</th>
              <th>Instance Type</th>
              <th>CPU Usage</th>
              <th>Memory Usage</th>
              <th>Running Pods</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {nodeMetrics?.map((node) => (
              <tr key={node.name}>
                <td>{node.name}</td>
                <td>{node.instanceType}</td>
                <td>
                  <div className="usage-bar">
                    <div 
                      className="usage-fill cpu"
                      style={{ width: `${node.cpu}%` }}
                    ></div>
                    <span>{node.cpu}%</span>
                  </div>
                </td>
                <td>
                  <div className="usage-bar">
                    <div 
                      className="usage-fill memory"
                      style={{ width: `${node.memory}%` }}
                    ></div>
                    <span>{node.memory}%</span>
                  </div>
                </td>
                <td>{node.pods}</td>
                <td>
                  <span className={`status status-${node.status}`}>
                    {node.status}
                  </span>
                </td>
                <td>
                  <button className="btn btn-primary btn-sm">Details</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Performance Alerts */}
      <div className="card">
        <div className="card-header">
          <h3 className="card-title">Performance Alerts</h3>
        </div>
        <div className="alerts-list">
          <div className="alert-item warning">
            <div className="alert-icon">⚠️</div>
            <div className="alert-content">
              <h4>High CPU Usage</h4>
              <p>Node node-1 is experiencing high CPU utilization (82%)</p>
              <span className="alert-time">2 hours ago</span>
            </div>
            <div className="alert-actions">
              <button className="btn btn-warning btn-sm">Scale Up</button>
            </div>
          </div>
          
          <div className="alert-item info">
            <div className="alert-icon">ℹ️</div>
            <div className="alert-content">
              <h4>Memory Usage Normal</h4>
              <p>All nodes are operating within normal memory ranges</p>
              <span className="alert-time">1 hour ago</span>
            </div>
            <div className="alert-actions">
              <button className="btn btn-info btn-sm">View Details</button>
            </div>
          </div>
          
          <div className="alert-item success">
            <div className="alert-icon">✅</div>
            <div className="alert-content">
              <h4>Optimization Applied</h4>
              <p>Pod scaling recommendation applied successfully</p>
              <span className="alert-time">30 minutes ago</span>
            </div>
            <div className="alert-actions">
              <button className="btn btn-success btn-sm">View Results</button>
            </div>
          </div>
        </div>
      </div>

      {/* Metrics Configuration */}
      <div className="grid grid-2">
        <div className="card">
          <div className="card-header">
            <h3 className="card-title">Metrics Configuration</h3>
          </div>
          <div className="config-section">
            <h4>Collection Intervals</h4>
            <div className="config-item">
              <label>CPU & Memory:</label>
              <select defaultValue="5">
                <option value="1">1 minute</option>
                <option value="5">5 minutes</option>
                <option value="15">15 minutes</option>
              </select>
            </div>
            <div className="config-item">
              <label>Network & Disk:</label>
              <select defaultValue="10">
                <option value="5">5 minutes</option>
                <option value="10">10 minutes</option>
                <option value="30">30 minutes</option>
              </select>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="card-header">
            <h3 className="card-title">Alert Thresholds</h3>
          </div>
          <div className="config-section">
            <h4>Resource Limits</h4>
            <div className="config-item">
              <label>CPU Warning:</label>
              <input type="number" defaultValue="70" min="0" max="100" />%
            </div>
            <div className="config-item">
              <label>CPU Critical:</label>
              <input type="number" defaultValue="85" min="0" max="100" />%
            </div>
            <div className="config-item">
              <label>Memory Warning:</label>
              <input type="number" defaultValue="75" min="0" max="100" />%
            </div>
            <div className="config-item">
              <label>Memory Critical:</label>
              <input type="number" defaultValue="90" min="0" max="100" />%
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Metrics; 