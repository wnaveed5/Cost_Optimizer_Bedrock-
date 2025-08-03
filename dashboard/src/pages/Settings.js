import React, { useState } from 'react';
import './Settings.css';

const Settings = () => {
  const [activeTab, setActiveTab] = useState('general');
  const [settings, setSettings] = useState({
    clusterName: 'cost-optimizer-cluster',
    region: 'us-west-2',
    optimizationInterval: 15,
    confidenceThreshold: 0.7,
    autoApply: false,
    notifications: true,
    emailAlerts: false,
    slackWebhook: '',
    costThreshold: 100,
    cpuThreshold: 80,
    memoryThreshold: 85
  });

  const handleSettingChange = (key, value) => {
    setSettings(prev => ({
      ...prev,
      [key]: value
    }));
  };

  const handleSave = () => {
    // In a real app, this would save to backend
    console.log('Saving settings:', settings);
    alert('Settings saved successfully!');
  };

  return (
    <div className="settings-page">
      <div className="page-header">
        <h2>Settings</h2>
        <p>Configure your cost optimization preferences</p>
      </div>

      {/* Settings Tabs */}
      <div className="settings-tabs">
        <button 
          className={`tab ${activeTab === 'general' ? 'active' : ''}`}
          onClick={() => setActiveTab('general')}
        >
          General
        </button>
        <button 
          className={`tab ${activeTab === 'optimization' ? 'active' : ''}`}
          onClick={() => setActiveTab('optimization')}
        >
          Optimization
        </button>
        <button 
          className={`tab ${activeTab === 'notifications' ? 'active' : ''}`}
          onClick={() => setActiveTab('notifications')}
        >
          Notifications
        </button>
        <button 
          className={`tab ${activeTab === 'thresholds' ? 'active' : ''}`}
          onClick={() => setActiveTab('thresholds')}
        >
          Thresholds
        </button>
      </div>

      {/* Settings Content */}
      <div className="settings-content">
        {activeTab === 'general' && (
          <div className="settings-section">
            <h3>General Configuration</h3>
            
            <div className="setting-group">
              <label>Cluster Name</label>
              <input 
                type="text" 
                value={settings.clusterName}
                onChange={(e) => handleSettingChange('clusterName', e.target.value)}
                placeholder="Enter cluster name"
              />
            </div>
            
            <div className="setting-group">
              <label>AWS Region</label>
              <select 
                value={settings.region}
                onChange={(e) => handleSettingChange('region', e.target.value)}
              >
                <option value="us-west-2">US West (Oregon)</option>
                <option value="us-east-1">US East (N. Virginia)</option>
                <option value="eu-west-1">Europe (Ireland)</option>
                <option value="ap-southeast-1">Asia Pacific (Singapore)</option>
              </select>
            </div>
            
            <div className="setting-group">
              <label>Optimization Interval (minutes)</label>
              <input 
                type="number" 
                value={settings.optimizationInterval}
                onChange={(e) => handleSettingChange('optimizationInterval', parseInt(e.target.value))}
                min="5"
                max="60"
              />
            </div>
          </div>
        )}

        {activeTab === 'optimization' && (
          <div className="settings-section">
            <h3>Optimization Settings</h3>
            
            <div className="setting-group">
              <label>Confidence Threshold</label>
              <div className="slider-container">
                <input 
                  type="range" 
                  min="0.5" 
                  max="0.95" 
                  step="0.05"
                  value={settings.confidenceThreshold}
                  onChange={(e) => handleSettingChange('confidenceThreshold', parseFloat(e.target.value))}
                />
                <span className="slider-value">{(settings.confidenceThreshold * 100).toFixed(0)}%</span>
              </div>
            </div>
            
            <div className="setting-group">
              <label>
                <input 
                  type="checkbox" 
                  checked={settings.autoApply}
                  onChange={(e) => handleSettingChange('autoApply', e.target.checked)}
                />
                Auto-apply recommendations
              </label>
              <p className="setting-description">
                Automatically apply recommendations that meet the confidence threshold
              </p>
            </div>
            
            <div className="setting-group">
              <h4>Optimization Types</h4>
              <div className="checkbox-group">
                <label>
                  <input type="checkbox" defaultChecked />
                  Instance right-sizing
                </label>
                <label>
                  <input type="checkbox" defaultChecked />
                  Pod scaling
                </label>
                <label>
                  <input type="checkbox" defaultChecked />
                  Spot instance migration
                </label>
                <label>
                  <input type="checkbox" defaultChecked />
                  Storage optimization
                </label>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'notifications' && (
          <div className="settings-section">
            <h3>Notification Settings</h3>
            
            <div className="setting-group">
              <label>
                <input 
                  type="checkbox" 
                  checked={settings.notifications}
                  onChange={(e) => handleSettingChange('notifications', e.target.checked)}
                />
                Enable in-app notifications
              </label>
            </div>
            
            <div className="setting-group">
              <label>
                <input 
                  type="checkbox" 
                  checked={settings.emailAlerts}
                  onChange={(e) => handleSettingChange('emailAlerts', e.target.checked)}
                />
                Email alerts
              </label>
              {settings.emailAlerts && (
                <input 
                  type="email" 
                  placeholder="Enter email address"
                  className="mt-2"
                />
              )}
            </div>
            
            <div className="setting-group">
              <label>Slack Webhook URL</label>
              <input 
                type="url" 
                value={settings.slackWebhook}
                onChange={(e) => handleSettingChange('slackWebhook', e.target.value)}
                placeholder="https://hooks.slack.com/services/..."
              />
            </div>
            
            <div className="setting-group">
              <h4>Notification Events</h4>
              <div className="checkbox-group">
                <label>
                  <input type="checkbox" defaultChecked />
                  New recommendations
                </label>
                <label>
                  <input type="checkbox" defaultChecked />
                  Applied optimizations
                </label>
                <label>
                  <input type="checkbox" defaultChecked />
                  Cost threshold exceeded
                </label>
                <label>
                  <input type="checkbox" defaultChecked />
                  System errors
                </label>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'thresholds' && (
          <div className="settings-section">
            <h3>Alert Thresholds</h3>
            
            <div className="setting-group">
              <label>Cost Threshold ($/month)</label>
              <input 
                type="number" 
                value={settings.costThreshold}
                onChange={(e) => handleSettingChange('costThreshold', parseInt(e.target.value))}
                min="0"
                step="10"
              />
            </div>
            
            <div className="setting-group">
              <label>CPU Usage Threshold (%)</label>
              <input 
                type="number" 
                value={settings.cpuThreshold}
                onChange={(e) => handleSettingChange('cpuThreshold', parseInt(e.target.value))}
                min="0"
                max="100"
              />
            </div>
            
            <div className="setting-group">
              <label>Memory Usage Threshold (%)</label>
              <input 
                type="number" 
                value={settings.memoryThreshold}
                onChange={(e) => handleSettingChange('memoryThreshold', parseInt(e.target.value))}
                min="0"
                max="100"
              />
            </div>
            
            <div className="setting-group">
              <h4>Resource Alerts</h4>
              <div className="checkbox-group">
                <label>
                  <input type="checkbox" defaultChecked />
                  High CPU usage
                </label>
                <label>
                  <input type="checkbox" defaultChecked />
                  High memory usage
                </label>
                <label>
                  <input type="checkbox" defaultChecked />
                  Low disk space
                </label>
                <label>
                  <input type="checkbox" defaultChecked />
                  Network issues
                </label>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Save Button */}
      <div className="settings-actions">
        <button className="btn btn-primary" onClick={handleSave}>
          Save Settings
        </button>
        <button className="btn btn-secondary">
          Reset to Defaults
        </button>
      </div>
    </div>
  );
};

export default Settings; 