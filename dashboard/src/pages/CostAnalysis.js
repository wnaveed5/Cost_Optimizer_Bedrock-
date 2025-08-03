import React from 'react';
import { useQuery } from 'react-query';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import './CostAnalysis.css';

const mockCostBreakdown = [
  { name: 'EC2 Instances', value: 650, color: '#0088FE' },
  { name: 'EKS Control Plane', value: 150, color: '#00C49F' },
  { name: 'Load Balancers', value: 120, color: '#FFBB28' },
  { name: 'Storage', value: 80, color: '#FF8042' },
  { name: 'Data Transfer', value: 50, color: '#8884D8' }
];

const mockCostHistory = [
  { date: '2024-01-01', ec2: 700, eks: 150, lb: 120, storage: 80, transfer: 50 },
  { date: '2024-01-02', ec2: 680, eks: 150, lb: 120, storage: 80, transfer: 50 },
  { date: '2024-01-03', ec2: 660, eks: 150, lb: 120, storage: 80, transfer: 50 },
  { date: '2024-01-04', ec2: 640, eks: 150, lb: 120, storage: 80, transfer: 50 },
  { date: '2024-01-05', ec2: 620, eks: 150, lb: 120, storage: 80, transfer: 50 },
  { date: '2024-01-06', ec2: 600, eks: 150, lb: 120, storage: 80, transfer: 50 },
  { date: '2024-01-07', ec2: 580, eks: 150, lb: 120, storage: 80, transfer: 50 }
];

const CostAnalysis = () => {
  const { data: costBreakdown, isLoading: breakdownLoading } = useQuery('costBreakdown', () => {
    return new Promise(resolve => {
      setTimeout(() => resolve(mockCostBreakdown), 800);
    });
  });

  const { data: costHistory, isLoading: historyLoading } = useQuery('costHistory', () => {
    return new Promise(resolve => {
      setTimeout(() => resolve(mockCostHistory), 600);
    });
  });

  if (breakdownLoading || historyLoading) {
    return (
      <div className="loading">
        <div className="spinner"></div>
      </div>
    );
  }

  return (
    <div className="cost-analysis">
      <div className="page-header">
        <h2>Cost Analysis</h2>
        <p>Detailed breakdown of AWS costs and optimization opportunities</p>
      </div>

      {/* Cost Overview */}
      <div className="grid grid-3 mb-6">
        <div className="stats-card">
          <h3>$1,050</h3>
          <p>Total Monthly Cost</p>
        </div>
        <div className="stats-card">
          <h3>$150</h3>
          <p>Monthly Savings</p>
        </div>
        <div className="stats-card">
          <h3>12.5%</h3>
          <p>Savings Percentage</p>
        </div>
      </div>

      {/* Charts */}
      <div className="grid grid-2 mb-6">
        <div className="card">
          <div className="card-header">
            <h3 className="card-title">Cost Breakdown</h3>
            <p className="card-subtitle">Current month's cost distribution</p>
          </div>
          <div className="chart-container">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={costBreakdown}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {costBreakdown.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="card">
          <div className="card-header">
            <h3 className="card-title">Cost Trend</h3>
            <p className="card-subtitle">Daily cost breakdown over time</p>
          </div>
          <div className="chart-container">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={costHistory}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Line type="monotone" dataKey="ec2" stroke="#0088FE" name="EC2" />
                <Line type="monotone" dataKey="eks" stroke="#00C49F" name="EKS" />
                <Line type="monotone" dataKey="lb" stroke="#FFBB28" name="Load Balancers" />
                <Line type="monotone" dataKey="storage" stroke="#FF8042" name="Storage" />
                <Line type="monotone" dataKey="transfer" stroke="#8884D8" name="Data Transfer" />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Cost Details Table */}
      <div className="card">
        <div className="card-header">
          <h3 className="card-title">Cost Details</h3>
          <button className="btn btn-primary">Export Report</button>
        </div>
        <table className="table">
          <thead>
            <tr>
              <th>Service</th>
              <th>Current Cost</th>
              <th>Previous Month</th>
              <th>Change</th>
              <th>Optimization Potential</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>EC2 Instances</td>
              <td>$650</td>
              <td>$700</td>
              <td className="text-success">-$50 (-7.1%)</td>
              <td>$120</td>
              <td>
                <button className="btn btn-success btn-sm">Optimize</button>
              </td>
            </tr>
            <tr>
              <td>EKS Control Plane</td>
              <td>$150</td>
              <td>$150</td>
              <td>$0 (0%)</td>
              <td>$0</td>
              <td>
                <span className="text-muted">Fixed Cost</span>
              </td>
            </tr>
            <tr>
              <td>Load Balancers</td>
              <td>$120</td>
              <td>$120</td>
              <td>$0 (0%)</td>
              <td>$30</td>
              <td>
                <button className="btn btn-success btn-sm">Optimize</button>
              </td>
            </tr>
            <tr>
              <td>Storage</td>
              <td>$80</td>
              <td>$80</td>
              <td>$0 (0%)</td>
              <td>$15</td>
              <td>
                <button className="btn btn-success btn-sm">Optimize</button>
              </td>
            </tr>
            <tr>
              <td>Data Transfer</td>
              <td>$50</td>
              <td>$50</td>
              <td>$0 (0%)</td>
              <td>$10</td>
              <td>
                <button className="btn btn-success btn-sm">Optimize</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      {/* Optimization Opportunities */}
      <div className="card">
        <div className="card-header">
          <h3 className="card-title">Optimization Opportunities</h3>
        </div>
        <div className="optimization-opportunities">
          <div className="opportunity-item">
            <div className="opportunity-header">
              <h4>EC2 Instance Right-sizing</h4>
              <span className="badge badge-warning">High Priority</span>
            </div>
            <p>3 instances are underutilized and can be downsized</p>
            <div className="opportunity-details">
              <span>Potential Savings: $120/month</span>
              <span>Risk: Low</span>
            </div>
          </div>
          
          <div className="opportunity-item">
            <div className="opportunity-header">
              <h4>Load Balancer Optimization</h4>
              <span className="badge badge-info">Medium Priority</span>
            </div>
            <p>2 load balancers can be consolidated</p>
            <div className="opportunity-details">
              <span>Potential Savings: $30/month</span>
              <span>Risk: Medium</span>
            </div>
          </div>
          
          <div className="opportunity-item">
            <div className="opportunity-header">
              <h4>Storage Optimization</h4>
              <span className="badge badge-info">Medium Priority</span>
            </div>
            <p>Unused EBS volumes can be deleted</p>
            <div className="opportunity-details">
              <span>Potential Savings: $15/month</span>
              <span>Risk: Low</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CostAnalysis; 