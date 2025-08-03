import React, { useState } from 'react';
import { useQuery } from 'react-query';
import './Recommendations.css';

const mockRecommendations = [
  {
    id: 1,
    type: 'Instance Right-sizing',
    description: 'Scale down t3.large to t3.medium for instance i-1234567890abcdef0',
    savings: 45.50,
    priority: 'high',
    status: 'pending',
    confidence: 0.85,
    risk: 'low',
    aiReasoning: 'CPU utilization consistently below 30% for the past 24 hours',
    estimatedImpact: '15% cost reduction',
    implementationTime: '5 minutes'
  },
  {
    id: 2,
    type: 'Pod Scaling',
    description: 'Reduce replicas for ecommerce-app from 3 to 2',
    savings: 12.30,
    priority: 'medium',
    status: 'applied',
    confidence: 0.78,
    risk: 'low',
    aiReasoning: 'Average response time remains under 200ms with reduced load',
    estimatedImpact: '8% resource savings',
    implementationTime: '2 minutes'
  },
  {
    id: 3,
    type: 'Spot Migration',
    description: 'Migrate workload to spot instances during off-peak hours',
    savings: 78.90,
    priority: 'low',
    status: 'pending',
    confidence: 0.65,
    risk: 'medium',
    aiReasoning: 'Workload can tolerate interruptions during maintenance windows',
    estimatedImpact: '25% cost reduction',
    implementationTime: '15 minutes'
  },
  {
    id: 4,
    type: 'Storage Optimization',
    description: 'Delete unused EBS volumes and snapshots',
    savings: 23.40,
    priority: 'medium',
    status: 'pending',
    confidence: 0.92,
    risk: 'low',
    aiReasoning: 'Identified 5 unused volumes and 12 old snapshots',
    estimatedImpact: '12% storage cost reduction',
    implementationTime: '10 minutes'
  }
];

const Recommendations = () => {
  const [selectedRecommendation, setSelectedRecommendation] = useState(null);
  const [filter, setFilter] = useState('all');

  const { data: recommendations, isLoading } = useQuery('recommendations', () => {
    return new Promise(resolve => {
      setTimeout(() => resolve(mockRecommendations), 800);
    });
  });

  const filteredRecommendations = recommendations?.filter(rec => {
    if (filter === 'all') return true;
    if (filter === 'pending') return rec.status === 'pending';
    if (filter === 'applied') return rec.status === 'applied';
    if (filter === 'high') return rec.priority === 'high';
    return true;
  });

  const totalSavings = recommendations?.reduce((sum, rec) => sum + rec.savings, 0) || 0;
  const pendingCount = recommendations?.filter(rec => rec.status === 'pending').length || 0;
  const appliedCount = recommendations?.filter(rec => rec.status === 'applied').length || 0;

  if (isLoading) {
    return (
      <div className="loading">
        <div className="spinner"></div>
      </div>
    );
  }

  return (
    <div className="recommendations-page">
      <div className="page-header">
        <h2>AI Recommendations</h2>
        <p>Intelligent cost optimization suggestions from AgentCore</p>
      </div>

      {/* Stats */}
      <div className="grid grid-4 mb-6">
        <div className="stats-card">
          <h3>${totalSavings.toFixed(2)}</h3>
          <p>Total Potential Savings</p>
        </div>
        <div className="stats-card">
          <h3>{recommendations?.length || 0}</h3>
          <p>Total Recommendations</p>
        </div>
        <div className="stats-card">
          <h3>{pendingCount}</h3>
          <p>Pending Actions</p>
        </div>
        <div className="stats-card">
          <h3>{appliedCount}</h3>
          <p>Applied Actions</p>
        </div>
      </div>

      {/* Filters */}
      <div className="filters mb-4">
        <button 
          className={`btn ${filter === 'all' ? 'btn-primary' : 'btn-secondary'}`}
          onClick={() => setFilter('all')}
        >
          All
        </button>
        <button 
          className={`btn ${filter === 'pending' ? 'btn-primary' : 'btn-secondary'}`}
          onClick={() => setFilter('pending')}
        >
          Pending
        </button>
        <button 
          className={`btn ${filter === 'applied' ? 'btn-primary' : 'btn-secondary'}`}
          onClick={() => setFilter('applied')}
        >
          Applied
        </button>
        <button 
          className={`btn ${filter === 'high' ? 'btn-primary' : 'btn-secondary'}`}
          onClick={() => setFilter('high')}
        >
          High Priority
        </button>
      </div>

      {/* Recommendations List */}
      <div className="recommendations-grid">
        {filteredRecommendations?.map((rec) => (
          <div key={rec.id} className="recommendation-card">
            <div className="recommendation-header">
              <div className="recommendation-type">
                <h4>{rec.type}</h4>
                <span className={`badge badge-${rec.priority}`}>
                  {rec.priority}
                </span>
              </div>
              <div className="recommendation-status">
                <span className={`status status-${rec.status}`}>
                  {rec.status}
                </span>
              </div>
            </div>
            
            <p className="recommendation-description">{rec.description}</p>
            
            <div className="recommendation-metrics">
              <div className="metric">
                <span className="metric-label">Savings:</span>
                <span className="metric-value">${rec.savings}/month</span>
              </div>
              <div className="metric">
                <span className="metric-label">Confidence:</span>
                <span className="metric-value">{(rec.confidence * 100).toFixed(0)}%</span>
              </div>
              <div className="metric">
                <span className="metric-label">Risk:</span>
                <span className={`metric-value risk-${rec.risk}`}>{rec.risk}</span>
              </div>
            </div>
            
            <div className="recommendation-actions">
              {rec.status === 'pending' && (
                <>
                  <button className="btn btn-success btn-sm">Apply</button>
                  <button className="btn btn-secondary btn-sm">Dismiss</button>
                </>
              )}
              <button 
                className="btn btn-primary btn-sm"
                onClick={() => setSelectedRecommendation(rec)}
              >
                Details
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* Recommendation Details Modal */}
      {selectedRecommendation && (
        <div className="modal-overlay" onClick={() => setSelectedRecommendation(null)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h3>{selectedRecommendation.type}</h3>
              <button 
                className="modal-close"
                onClick={() => setSelectedRecommendation(null)}
              >
                ×
              </button>
            </div>
            
            <div className="modal-body">
              <div className="detail-section">
                <h4>Description</h4>
                <p>{selectedRecommendation.description}</p>
              </div>
              
              <div className="detail-section">
                <h4>AI Reasoning</h4>
                <p>{selectedRecommendation.aiReasoning}</p>
              </div>
              
              <div className="detail-section">
                <h4>Impact Analysis</h4>
                <div className="impact-grid">
                  <div className="impact-item">
                    <span className="impact-label">Estimated Savings:</span>
                    <span className="impact-value">${selectedRecommendation.savings}/month</span>
                  </div>
                  <div className="impact-item">
                    <span className="impact-label">Cost Impact:</span>
                    <span className="impact-value">{selectedRecommendation.estimatedImpact}</span>
                  </div>
                  <div className="impact-item">
                    <span className="impact-label">Implementation Time:</span>
                    <span className="impact-value">{selectedRecommendation.implementationTime}</span>
                  </div>
                  <div className="impact-item">
                    <span className="impact-label">Risk Level:</span>
                    <span className={`impact-value risk-${selectedRecommendation.risk}`}>
                      {selectedRecommendation.risk}
                    </span>
                  </div>
                </div>
              </div>
              
              <div className="detail-section">
                <h4>Confidence Score</h4>
                <div className="confidence-bar">
                  <div 
                    className="confidence-fill"
                    style={{ width: `${selectedRecommendation.confidence * 100}%` }}
                  ></div>
                  <span className="confidence-text">
                    {(selectedRecommendation.confidence * 100).toFixed(0)}%
                  </span>
                </div>
              </div>
            </div>
            
            <div className="modal-footer">
              {selectedRecommendation.status === 'pending' && (
                <>
                  <button className="btn btn-success">Apply Recommendation</button>
                  <button className="btn btn-secondary">Dismiss</button>
                </>
              )}
              <button 
                className="btn btn-primary"
                onClick={() => setSelectedRecommendation(null)}
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Recommendations; 