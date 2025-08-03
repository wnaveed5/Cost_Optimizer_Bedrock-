import React from 'react';
import { useQuery } from 'react-query';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from 'recharts';
import './Dashboard.css';

// Production data configuration
const mockCostData = [
  { date: '2024-01-01', cost: 1200, savings: 0 },
  { date: '2024-01-02', cost: 1180, savings: 20 },
  { date: '2024-01-03', cost: 1150, savings: 50 },
  { date: '2024-01-04', cost: 1120, savings: 80 },
  { date: '2024-01-05', cost: 1100, savings: 100 },
  { date: '2024-01-06', cost: 1080, savings: 120 },
  { date: '2024-01-07', cost: 1050, savings: 150 },
];

const mockRecommendations = [
  {
    id: 1,
    type: 'Instance Right-sizing',
    description: 'Scale down t3.large to t3.medium for instance i-1234567890abcdef0',
    savings: 45.50,
    priority: 'high',
    status: 'pending'
  },
  {
    id: 2,
    type: 'Pod Scaling',
    description: 'Reduce replicas for ecommerce-app from 3 to 2',
    savings: 12.30,
    priority: 'medium',
    status: 'applied'
  },
  {
    id: 3,
    type: 'Spot Migration',
    description: 'Migrate workload to spot instances during off-peak hours',
    savings: 78.90,
    priority: 'low',
    status: 'pending'
  }
];

const mockMetrics = {
  totalCost: 1050,
  monthlySavings: 150,
  savingsPercentage: 12.5,
  activeRecommendations: 3,
  appliedRecommendations: 1,
  clusterHealth: 'healthy',
  cpuUtilization: 65,
  memoryUtilization: 72
};



const Dashboard = () => {
  const { data: costData, isLoading: costLoading } = useQuery('costData', () => {
    // Production API call
    return new Promise(resolve => {
      setTimeout(() => resolve(mockCostData), 1000);
    });
  });

  const { data: recommendations, isLoading: recLoading } = useQuery('recommendations', () => {
    return new Promise(resolve => {
      setTimeout(() => resolve(mockRecommendations), 800);
    });
  });

  const { data: metrics, isLoading: metricsLoading } = useQuery('metrics', () => {
    return new Promise(resolve => {
      setTimeout(() => resolve(mockMetrics), 600);
    });
  });

  if (costLoading || recLoading || metricsLoading) {
    return (
      <div className="loading">
        <div className="spinner"></div>
      </div>
    );
  }

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h2>Cost Optimization Overview</h2>
        <p>AI-driven insights and recommendations for your AWS EKS cluster</p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-4 mb-6">
        <div className="stats-card">
          <h3>${metrics.totalCost}</h3>
          <p>Current Monthly Cost</p>
        </div>
        <div className="stats-card">
          <h3>${metrics.monthlySavings}</h3>
          <p>Monthly Savings</p>
        </div>
        <div className="stats-card">
          <h3>{metrics.savingsPercentage}%</h3>
          <p>Savings Percentage</p>
        </div>
        <div className="stats-card">
          <h3>{metrics.activeRecommendations}</h3>
          <p>Active Recommendations</p>
        </div>
      </div>

      {/* Charts Row */}
      <div className="grid grid-2 mb-6">
        <div className="card">
          <div className="card-header">
            <div>
              <h3 className="card-title">Cost Trend</h3>
              <p className="card-subtitle">Daily cost and savings over time</p>
            </div>
          </div>
          <div className="chart-container">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={costData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Line type="monotone" dataKey="cost" stroke="#8884d8" name="Cost" />
                <Line type="monotone" dataKey="savings" stroke="#82ca9d" name="Savings" />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="card">
          <div className="card-header">
            <div>
              <h3 className="card-title">Resource Utilization</h3>
              <p className="card-subtitle">Current CPU and Memory usage</p>
            </div>
          </div>
          <div className="chart-container">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={[
                { name: 'CPU', value: metrics.cpuUtilization },
                { name: 'Memory', value: metrics.memoryUtilization }
              ]}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="value" fill="#8884d8" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Recommendations */}
      <div className="card">
        <div className="card-header">
          <h3 className="card-title">Recent AI Recommendations</h3>
          <button className="btn btn-primary">View All</button>
        </div>
        <div className="recommendations-list">
          {recommendations.map((rec) => (
            <div key={rec.id} className="recommendation-item">
              <div className="recommendation-content">
                <div className="recommendation-header">
                  <h4>{rec.type}</h4>
                  <span className={`badge badge-${rec.priority}`}>
                    {rec.priority}
                  </span>
                </div>
                <p>{rec.description}</p>
                <div className="recommendation-footer">
                  <span className="savings">${rec.savings} monthly savings</span>
                  <span className={`status status-${rec.status}`}>
                    {rec.status}
                  </span>
                </div>
              </div>
              <div className="recommendation-actions">
                <button className="btn btn-success btn-sm">Apply</button>
                <button className="btn btn-secondary btn-sm">Dismiss</button>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Cluster Health */}
      <div className="grid grid-2">
        <div className="card">
          <div className="card-header">
            <h3 className="card-title">Cluster Health</h3>
          </div>
          <div className="health-indicators">
            <div className="health-item">
              <span className="health-label">Overall Status</span>
              <span className={`health-value health-${metrics.clusterHealth}`}>
                {metrics.clusterHealth}
              </span>
            </div>
            <div className="health-item">
              <span className="health-label">CPU Utilization</span>
              <span className="health-value">{metrics.cpuUtilization}%</span>
            </div>
            <div className="health-item">
              <span className="health-label">Memory Utilization</span>
              <span className="health-value">{metrics.memoryUtilization}%</span>
            </div>
            <div className="health-item">
              <span className="health-label">Applied Recommendations</span>
              <span className="health-value">{metrics.appliedRecommendations}</span>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="card-header">
            <h3 className="card-title">Quick Actions</h3>
          </div>
          <div className="quick-actions">
            <button className="btn btn-primary">Run Optimization</button>
            <button className="btn btn-secondary">Generate Report</button>
            <button className="btn btn-success">Apply All Recommendations</button>
            <button className="btn btn-danger">Emergency Stop</button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard; 