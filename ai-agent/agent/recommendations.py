#!/usr/bin/env python3
"""
Recommendation Engine for Cost Optimization

This module generates specific cost optimization recommendations
based on AI analysis and usage patterns.
"""

import logging
from typing import Dict, List, Optional
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class RecommendationEngine:
    """
    Generates cost optimization recommendations
    """
    
    def __init__(self, cluster_name: str, region: str = 'us-west-2'):
        self.cluster_name = cluster_name
        self.region = region
        
        # Recommendation priorities
        self.priority_weights = {
            'high': 1.0,
            'medium': 0.7,
            'low': 0.4
        }
    
    def generate_recommendations(self, metrics: Dict, ai_analysis: Dict) -> List[Dict]:
        """
        Generate cost optimization recommendations based on metrics and AI analysis
        """
        logger.info("Generating cost optimization recommendations...")
        
        recommendations = []
        
        try:
            # Extract AI insights
            ai_insights = ai_analysis.get('ai_analysis', {})
            confidence_score = ai_analysis.get('confidence_score', 0.0)
            
            # Generate pod scaling recommendations
            pod_recommendations = self._generate_pod_scaling_recommendations(metrics)
            recommendations.extend(pod_recommendations)
            
            # Generate instance right-sizing recommendations
            instance_recommendations = self._generate_instance_recommendations(metrics)
            recommendations.extend(instance_recommendations)
            
            # Generate spot instance recommendations
            spot_recommendations = self._generate_spot_recommendations(metrics)
            recommendations.extend(spot_recommendations)
            
            # Generate workload scheduling recommendations
            scheduling_recommendations = self._generate_scheduling_recommendations(metrics)
            recommendations.extend(scheduling_recommendations)
            
            # Apply AI insights to enhance recommendations
            recommendations = self._apply_ai_insights(recommendations, ai_insights, confidence_score)
            
            # Sort by priority and estimated savings
            recommendations.sort(key=lambda x: (
                self.priority_weights.get(x.get('priority', 'low'), 0.4),
                x.get('estimated_savings', 0)
            ), reverse=True)
            
            logger.info(f"Generated {len(recommendations)} recommendations")
            
        except Exception as e:
            logger.error(f"Error generating recommendations: {e}")
        
        return recommendations
    
    def _generate_pod_scaling_recommendations(self, metrics: Dict) -> List[Dict]:
        """
        Generate pod scaling recommendations based on usage
        """
        recommendations = []
        
        try:
            pod_metrics = metrics.get('pod_metrics', {})
            deployments = pod_metrics.get('deployments', {})
            
            for deployment_name, deployment_data in deployments.items():
                replicas = deployment_data.get('replicas', 0)
                cpu_usage = deployment_data.get('cpu_usage', 0)
                memory_usage = deployment_data.get('memory_usage', 0)
                
                # Scale down if underutilized
                if replicas > 1 and cpu_usage < 0.2 and memory_usage < 0.3:
                    target_replicas = max(1, replicas - 1)
                    savings = self._calculate_pod_scaling_savings(replicas, target_replicas)
                    
                    recommendations.append({
                        'action_type': 'scale_pods',
                        'action': f'Scale down {deployment_name} from {replicas} to {target_replicas} replicas',
                        'deployment_name': deployment_name,
                        'namespace': 'default',
                        'target_replicas': target_replicas,
                        'reason': 'Low CPU and memory utilization',
                        'estimated_savings': savings,
                        'priority': 'medium',
                        'confidence_score': 0.8,
                        'risk_level': 'low'
                    })
                
                # Scale up if overutilized
                elif cpu_usage > 0.8 or memory_usage > 0.85:
                    target_replicas = replicas + 1
                    
                    recommendations.append({
                        'action_type': 'scale_pods',
                        'action': f'Scale up {deployment_name} from {replicas} to {target_replicas} replicas',
                        'deployment_name': deployment_name,
                        'namespace': 'default',
                        'target_replicas': target_replicas,
                        'reason': 'High CPU or memory utilization',
                        'estimated_savings': 0,  # Scaling up increases cost but improves performance
                        'priority': 'high',
                        'confidence_score': 0.9,
                        'risk_level': 'low'
                    })
            
        except Exception as e:
            logger.error(f"Error generating pod scaling recommendations: {e}")
        
        return recommendations
    
    def _generate_instance_recommendations(self, metrics: Dict) -> List[Dict]:
        """
        Generate instance right-sizing recommendations
        """
        recommendations = []
        
        try:
            node_metrics = metrics.get('node_metrics', {})
            
            for instance_id, instance_data in node_metrics.items():
                if not instance_id.startswith('instance_'):
                    continue
                
                instance_type = instance_data.get('instance_type', '')
                cpu_util = instance_data.get('cpu_utilization', 0)
                memory_util = instance_data.get('memory_utilization', 0)
                hourly_cost = instance_data.get('hourly_cost', 0)
                
                # Right-size underutilized instances
                if cpu_util < 0.3 and memory_util < 0.4:
                    recommended_type = self._get_smaller_instance_type(instance_type)
                    if recommended_type and recommended_type != instance_type:
                        savings = self._calculate_instance_savings(instance_type, recommended_type)
                        
                        recommendations.append({
                            'action_type': 'right_size_instance',
                            'action': f'Right-size {instance_id} from {instance_type} to {recommended_type}',
                            'instance_id': instance_data.get('instance_id'),
                            'current_instance_type': instance_type,
                            'target_instance_type': recommended_type,
                            'reason': f'Low utilization (CPU: {cpu_util:.1%}, Memory: {memory_util:.1%})',
                            'estimated_savings': savings,
                            'priority': 'medium',
                            'confidence_score': 0.85,
                            'risk_level': 'medium'
                        })
                
                # Upgrade overutilized instances
                elif cpu_util > 0.8 or memory_util > 0.85:
                    recommended_type = self._get_larger_instance_type(instance_type)
                    if recommended_type and recommended_type != instance_type:
                        cost_increase = self._calculate_instance_cost_increase(instance_type, recommended_type)
                        
                        recommendations.append({
                            'action_type': 'right_size_instance',
                            'action': f'Upgrade {instance_id} from {instance_type} to {recommended_type}',
                            'instance_id': instance_data.get('instance_id'),
                            'current_instance_type': instance_type,
                            'target_instance_type': recommended_type,
                            'reason': f'High utilization (CPU: {cpu_util:.1%}, Memory: {memory_util:.1%})',
                            'estimated_savings': -cost_increase,  # Negative for cost increase
                            'priority': 'high',
                            'confidence_score': 0.9,
                            'risk_level': 'low'
                        })
            
        except Exception as e:
            logger.error(f"Error generating instance recommendations: {e}")
        
        return recommendations
    
    def _generate_spot_recommendations(self, metrics: Dict) -> List[Dict]:
        """
        Generate spot instance migration recommendations
        """
        recommendations = []
        
        try:
            node_metrics = metrics.get('node_metrics', {})
            
            for instance_id, instance_data in node_metrics.items():
                if not instance_id.startswith('instance_'):
                    continue
                
                instance_type = instance_data.get('instance_type', '')
                cpu_util = instance_data.get('cpu_utilization', 0)
                memory_util = instance_data.get('memory_utilization', 0)
                is_spot = instance_data.get('spot_instance', False)
                
                # Recommend spot for suitable workloads
                if not is_spot and cpu_util < 0.6 and memory_util < 0.7:
                    savings = self._calculate_spot_savings(instance_type)
                    
                    recommendations.append({
                        'action_type': 'migrate_to_spot',
                        'action': f'Migrate {instance_id} to spot instance',
                        'instance_id': instance_data.get('instance_id'),
                        'instance_type': instance_type,
                        'reason': f'Moderate utilization suitable for spot (CPU: {cpu_util:.1%}, Memory: {memory_util:.1%})',
                        'estimated_savings': savings,
                        'priority': 'medium',
                        'confidence_score': 0.75,
                        'risk_level': 'medium'
                    })
            
        except Exception as e:
            logger.error(f"Error generating spot recommendations: {e}")
        
        return recommendations
    
    def _generate_scheduling_recommendations(self, metrics: Dict) -> List[Dict]:
        """
        Generate workload scheduling recommendations
        """
        recommendations = []
        
        try:
            # Analyze usage patterns for scheduling opportunities
            cost_metrics = metrics.get('cost_metrics', {})
            daily_average_cost = cost_metrics.get('daily_average_cost', 0)
            
            # Simple scheduling logic based on time patterns
            current_hour = datetime.utcnow().hour
            
            # Recommend scheduling during off-peak hours (2-6 AM UTC)
            if 2 <= current_hour <= 6:
                recommendations.append({
                    'action_type': 'schedule_workload',
                    'action': 'Schedule batch jobs during off-peak hours',
                    'reason': 'Current time is in off-peak window (2-6 AM UTC)',
                    'estimated_savings': daily_average_cost * 0.1,  # 10% savings
                    'priority': 'low',
                    'confidence_score': 0.6,
                    'risk_level': 'low'
                })
            
        except Exception as e:
            logger.error(f"Error generating scheduling recommendations: {e}")
        
        return recommendations
    
    def _apply_ai_insights(self, recommendations: List[Dict], ai_insights: Dict, confidence_score: float) -> List[Dict]:
        """
        Apply AI insights to enhance recommendations
        """
        try:
            for recommendation in recommendations:
                # Adjust confidence based on AI analysis
                if ai_insights.get('recommendation_confidence', 0) > 0.8:
                    recommendation['confidence_score'] = min(1.0, recommendation['confidence_score'] * 1.1)
                
                # Adjust savings estimates based on AI predictions
                ai_savings_multiplier = ai_insights.get('savings_multiplier', 1.0)
                recommendation['estimated_savings'] *= ai_savings_multiplier
                
                # Add AI reasoning if available
                if ai_insights.get('reasoning'):
                    recommendation['ai_reasoning'] = ai_insights['reasoning']
            
        except Exception as e:
            logger.error(f"Error applying AI insights: {e}")
        
        return recommendations
    
    def _calculate_pod_scaling_savings(self, current_replicas: int, target_replicas: int) -> float:
        """
        Calculate savings from pod scaling
        """
        # Simplified calculation - in production, use actual resource costs
        cpu_per_replica = 0.5  # CPU cores
        memory_per_replica = 0.5  # GB
        cpu_cost_per_core_hour = 0.05
        memory_cost_per_gb_hour = 0.01
        
        replicas_diff = current_replicas - target_replicas
        hourly_savings = replicas_diff * (cpu_per_replica * cpu_cost_per_core_hour + 
                                        memory_per_replica * memory_cost_per_gb_hour)
        
        return hourly_savings * 24 * 30  # Monthly savings
    
    def _calculate_instance_savings(self, current_type: str, target_type: str) -> float:
        """
        Calculate savings from instance right-sizing
        """
        # Simplified pricing - in production, use AWS Pricing API
        pricing = {
            't3.medium': 0.0416,
            't3.large': 0.0832,
            't3.xlarge': 0.1664
        }
        
        current_cost = pricing.get(current_type, 0.1)
        target_cost = pricing.get(target_type, 0.1)
        
        hourly_savings = current_cost - target_cost
        return hourly_savings * 24 * 30  # Monthly savings
    
    def _calculate_instance_cost_increase(self, current_type: str, target_type: str) -> float:
        """
        Calculate cost increase from instance upgrade
        """
        return -self._calculate_instance_savings(current_type, target_type)
    
    def _calculate_spot_savings(self, instance_type: str) -> float:
        """
        Calculate savings from spot instance migration
        """
        # Assume 60% savings with spot instances
        on_demand_cost = self._get_instance_cost(instance_type)
        spot_cost = on_demand_cost * 0.4
        
        hourly_savings = on_demand_cost - spot_cost
        return hourly_savings * 24 * 30  # Monthly savings
    
    def _get_instance_cost(self, instance_type: str) -> float:
        """
        Get hourly cost for instance type
        """
        pricing = {
            't3.medium': 0.0416,
            't3.large': 0.0832,
            't3.xlarge': 0.1664
        }
        return pricing.get(instance_type, 0.1)
    
    def _get_smaller_instance_type(self, current_type: str) -> Optional[str]:
        """
        Get smaller instance type for right-sizing
        """
        size_mapping = {
            't3.xlarge': 't3.large',
            't3.large': 't3.medium'
        }
        return size_mapping.get(current_type)
    
    def _get_larger_instance_type(self, current_type: str) -> Optional[str]:
        """
        Get larger instance type for upgrades
        """
        size_mapping = {
            't3.medium': 't3.large',
            't3.large': 't3.xlarge'
        }
        return size_mapping.get(current_type) 