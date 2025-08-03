#!/usr/bin/env python3
"""
Cost Analyzer for AWS EKS Cluster

This module collects and analyzes CloudWatch metrics to identify
cost optimization opportunities.
"""

import boto3
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import numpy as np

logger = logging.getLogger(__name__)

class CostAnalyzer:
    """
    Analyzes AWS costs and usage patterns for optimization
    """
    
    def __init__(self, cluster_name: str, region: str = 'us-west-2'):
        self.cluster_name = cluster_name
        self.region = region
        self.cloudwatch = boto3.client('cloudwatch', region_name=region)
        self.ec2 = boto3.client('ec2', region_name=region)
        self.ce = boto3.client('ce', region_name=region)
        
        # Instance type pricing (simplified - in production, use AWS Pricing API)
        self.instance_pricing = {
            't3.medium': 0.0416,   # per hour
            't3.large': 0.0832,
            't3.xlarge': 0.1664,
            'm5.large': 0.096,
            'm5.xlarge': 0.192,
            'c5.large': 0.085,
            'c5.xlarge': 0.17
        }
    
    def get_node_metrics(self) -> Dict:
        """
        Get EKS node metrics from CloudWatch
        """
        logger.info("Collecting node metrics...")
        
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(hours=1)
        
        metrics = {}
        
        try:
            # Get EKS cluster metrics
            eks_metrics = self.cloudwatch.get_metric_data(
                MetricDataQueries=[
                    {
                        'Id': 'cluster_node_count',
                        'MetricStat': {
                            'Metric': {
                                'Namespace': 'AWS/EKS',
                                'MetricName': 'cluster_node_count',
                                'Dimensions': [
                                    {
                                        'Name': 'ClusterName',
                                        'Value': self.cluster_name
                                    }
                                ]
                            },
                            'Period': 300,
                            'Stat': 'Average'
                        }
                    },
                    {
                        'Id': 'cluster_failed_node_count',
                        'MetricStat': {
                            'Metric': {
                                'Namespace': 'AWS/EKS',
                                'MetricName': 'cluster_failed_node_count',
                                'Dimensions': [
                                    {
                                        'Name': 'ClusterName',
                                        'Value': self.cluster_name
                                    }
                                ]
                            },
                            'Period': 300,
                            'Stat': 'Average'
                        }
                    }
                ],
                StartTime=start_time,
                EndTime=end_time
            )
            
            # Process EKS metrics
            for result in eks_metrics['MetricDataResults']:
                if result['Id'] == 'cluster_node_count' and result['Values']:
                    metrics['total_nodes'] = result['Values'][-1]
                elif result['Id'] == 'cluster_failed_node_count' and result['Values']:
                    metrics['failed_nodes'] = result['Values'][-1]
            
            # Get EC2 instance metrics for nodes
            instances = self._get_eks_instances()
            
            for instance in instances:
                instance_id = instance['InstanceId']
                instance_type = instance['InstanceType']
                
                # Get CPU utilization
                cpu_metrics = self.cloudwatch.get_metric_data(
                    MetricDataQueries=[
                        {
                            'Id': 'cpu_utilization',
                            'MetricStat': {
                                'Metric': {
                                    'Namespace': 'AWS/EC2',
                                    'MetricName': 'CPUUtilization',
                                    'Dimensions': [
                                        {
                                            'Name': 'InstanceId',
                                            'Value': instance_id
                                        }
                                    ]
                                },
                                'Period': 300,
                                'Stat': 'Average'
                            }
                        }
                    ],
                    StartTime=start_time,
                    EndTime=end_time
                )
                
                # Get memory metrics (if available)
                memory_metrics = self.cloudwatch.get_metric_data(
                    MetricDataQueries=[
                        {
                            'Id': 'memory_utilization',
                            'MetricStat': {
                                'Metric': {
                                    'Namespace': 'System/Linux',
                                    'MetricName': 'MemoryUtilization',
                                    'Dimensions': [
                                        {
                                            'Name': 'InstanceId',
                                            'Value': instance_id
                                        }
                                    ]
                                },
                                'Period': 300,
                                'Stat': 'Average'
                            }
                        }
                    ],
                    StartTime=start_time,
                    EndTime=end_time
                )
                
                instance_metrics = {
                    'instance_id': instance_id,
                    'instance_type': instance_type,
                    'availability_zone': instance['Placement']['AvailabilityZone'],
                    'state': instance['State']['Name'],
                    'cpu_utilization': cpu_metrics['MetricDataResults'][0]['Values'][-1] if cpu_metrics['MetricDataResults'][0]['Values'] else 0,
                    'memory_utilization': memory_metrics['MetricDataResults'][0]['Values'][-1] if memory_metrics['MetricDataResults'][0]['Values'] else 0,
                    'hourly_cost': self.instance_pricing.get(instance_type, 0.1),
                    'spot_instance': instance.get('InstanceLifecycle') == 'spot'
                }
                
                metrics[f'instance_{instance_id}'] = instance_metrics
            
            logger.info(f"Collected metrics for {len(instances)} instances")
            
        except Exception as e:
            logger.error(f"Error collecting node metrics: {e}")
        
        return metrics
    
    def get_pod_metrics(self) -> Dict:
        """
        Get Kubernetes pod metrics
        """
        logger.info("Collecting pod metrics...")
        
        metrics = {
            'deployments': {},
            'pods': {}
        }
        
        try:
            # This would typically use the Kubernetes metrics API
            # For now, we'll return a simplified structure
            # In production, you'd query the metrics server
            
            # Example structure
            metrics['deployments'] = {
                'sample-app': {
                    'replicas': 3,
                    'available_replicas': 3,
                    'cpu_request': 0.5,
                    'memory_request': '512Mi',
                    'cpu_usage': 0.3,
                    'memory_usage': '256Mi'
                }
            }
            
            metrics['pods'] = {
                'sample-app-pod-1': {
                    'namespace': 'default',
                    'deployment': 'sample-app',
                    'cpu_usage': 0.1,
                    'memory_usage': '128Mi',
                    'status': 'Running'
                }
            }
            
        except Exception as e:
            logger.error(f"Error collecting pod metrics: {e}")
        
        return metrics
    
    def get_cost_metrics(self) -> Dict:
        """
        Get AWS cost and usage metrics
        """
        logger.info("Collecting cost metrics...")
        
        end_date = datetime.utcnow().date()
        start_date = end_date - timedelta(days=7)
        
        metrics = {}
        
        try:
            # Get cost and usage data
            cost_data = self.ce.get_cost_and_usage(
                TimePeriod={
                    'Start': start_date.strftime('%Y-%m-%d'),
                    'End': end_date.strftime('%Y-%m-%d')
                },
                Granularity='DAILY',
                Metrics=['UnblendedCost'],
                GroupBy=[
                    {
                        'Type': 'DIMENSION',
                        'Key': 'SERVICE'
                    }
                ]
            )
            
            # Process cost data
            total_cost = 0
            service_costs = {}
            
            for result in cost_data['ResultsByTime']:
                date = result['TimePeriod']['Start']
                for group in result['Groups']:
                    service = group['Keys'][0]
                    cost = float(group['Metrics']['UnblendedCost']['Amount'])
                    
                    if service not in service_costs:
                        service_costs[service] = 0
                    service_costs[service] += cost
                    total_cost += cost
            
            metrics = {
                'total_cost_7_days': total_cost,
                'daily_average_cost': total_cost / 7,
                'service_breakdown': service_costs,
                'ec2_cost': service_costs.get('Amazon Elastic Compute Cloud - Compute', 0),
                'eks_cost': service_costs.get('Amazon Elastic Container Service for Kubernetes', 0)
            }
            
            # Calculate cost trends
            if len(cost_data['ResultsByTime']) > 1:
                recent_costs = [float(result['Total']['UnblendedCost']['Amount']) 
                              for result in cost_data['ResultsByTime'][-3:]]
                if len(recent_costs) >= 2:
                    cost_trend = (recent_costs[-1] - recent_costs[0]) / len(recent_costs)
                    metrics['cost_trend'] = cost_trend
                    metrics['cost_trend_percentage'] = (cost_trend / recent_costs[0]) * 100 if recent_costs[0] > 0 else 0
            
        except Exception as e:
            logger.error(f"Error collecting cost metrics: {e}")
        
        return metrics
    
    def analyze_usage_patterns(self, node_metrics: Dict) -> Dict:
        """
        Analyze usage patterns to identify optimization opportunities
        """
        logger.info("Analyzing usage patterns...")
        
        analysis = {
            'underutilized_instances': [],
            'overutilized_instances': [],
            'spot_opportunities': [],
            'right_sizing_opportunities': []
        }
        
        try:
            for instance_id, metrics in node_metrics.items():
                if instance_id.startswith('instance_'):
                    cpu_util = metrics.get('cpu_utilization', 0)
                    memory_util = metrics.get('memory_utilization', 0)
                    instance_type = metrics.get('instance_type', '')
                    is_spot = metrics.get('spot_instance', False)
                    
                    # Identify underutilized instances
                    if cpu_util < 20 and memory_util < 30:
                        analysis['underutilized_instances'].append({
                            'instance_id': metrics['instance_id'],
                            'instance_type': instance_type,
                            'cpu_utilization': cpu_util,
                            'memory_utilization': memory_util,
                            'estimated_savings': self._calculate_right_sizing_savings(instance_type, cpu_util)
                        })
                    
                    # Identify overutilized instances
                    if cpu_util > 80 or memory_util > 85:
                        analysis['overutilized_instances'].append({
                            'instance_id': metrics['instance_id'],
                            'instance_type': instance_type,
                            'cpu_utilization': cpu_util,
                            'memory_utilization': memory_util,
                            'recommended_upgrade': self._get_recommended_instance_type(instance_type, cpu_util, memory_util)
                        })
                    
                    # Identify spot opportunities
                    if not is_spot and cpu_util < 50 and memory_util < 60:
                        analysis['spot_opportunities'].append({
                            'instance_id': metrics['instance_id'],
                            'instance_type': instance_type,
                            'estimated_savings': self._calculate_spot_savings(instance_type)
                        })
                    
                    # Right-sizing opportunities
                    if 20 <= cpu_util <= 60 and 30 <= memory_util <= 70:
                        recommended_type = self._get_optimal_instance_type(cpu_util, memory_util)
                        if recommended_type != instance_type:
                            analysis['right_sizing_opportunities'].append({
                                'instance_id': metrics['instance_id'],
                                'current_type': instance_type,
                                'recommended_type': recommended_type,
                                'estimated_savings': self._calculate_right_sizing_savings(instance_type, cpu_util)
                            })
            
            logger.info(f"Analysis completed: {len(analysis['underutilized_instances'])} underutilized, "
                       f"{len(analysis['overutilized_instances'])} overutilized instances found")
            
        except Exception as e:
            logger.error(f"Error analyzing usage patterns: {e}")
        
        return analysis
    
    def _get_eks_instances(self) -> List[Dict]:
        """
        Get EC2 instances that are part of the EKS cluster
        """
        try:
            response = self.ec2.describe_instances(
                Filters=[
                    {
                        'Name': 'tag:kubernetes.io/cluster/' + self.cluster_name,
                        'Values': ['owned', 'shared']
                    },
                    {
                        'Name': 'instance-state-name',
                        'Values': ['running', 'stopped']
                    }
                ]
            )
            
            instances = []
            for reservation in response['Reservations']:
                instances.extend(reservation['Instances'])
            
            return instances
            
        except Exception as e:
            logger.error(f"Error getting EKS instances: {e}")
            return []
    
    def _calculate_right_sizing_savings(self, current_type: str, cpu_utilization: float) -> float:
        """
        Calculate potential savings from right-sizing
        """
        current_cost = self.instance_pricing.get(current_type, 0.1)
        
        # Simple logic: if CPU < 30%, recommend smaller instance
        if cpu_utilization < 30:
            if current_type.startswith('t3.'):
                if current_type == 't3.xlarge':
                    return current_cost - self.instance_pricing.get('t3.large', 0.0832)
                elif current_type == 't3.large':
                    return current_cost - self.instance_pricing.get('t3.medium', 0.0416)
        
        return 0.0
    
    def _calculate_spot_savings(self, instance_type: str) -> float:
        """
        Calculate potential savings from using spot instances
        """
        on_demand_cost = self.instance_pricing.get(instance_type, 0.1)
        # Assume 60% savings with spot instances
        spot_cost = on_demand_cost * 0.4
        return on_demand_cost - spot_cost
    
    def _get_recommended_instance_type(self, current_type: str, cpu_util: float, memory_util: float) -> str:
        """
        Get recommended instance type based on usage
        """
        if current_type.startswith('t3.'):
            if cpu_util > 80 or memory_util > 85:
                if current_type == 't3.medium':
                    return 't3.large'
                elif current_type == 't3.large':
                    return 't3.xlarge'
        
        return current_type
    
    def _get_optimal_instance_type(self, cpu_util: float, memory_util: float) -> str:
        """
        Get optimal instance type based on usage patterns
        """
        if cpu_util < 30 and memory_util < 40:
            return 't3.medium'
        elif cpu_util < 60 and memory_util < 70:
            return 't3.large'
        else:
            return 't3.xlarge' 