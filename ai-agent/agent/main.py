#!/usr/bin/env python3
"""
AI-Driven Cost Optimization Agent using AgentCore for Amazon Bedrock

This agent monitors AWS EKS cluster metrics via CloudWatch and makes
intelligent decisions to optimize costs through:
- Instance right-sizing
- Pod scaling
- Spot instance migration
- Workload scheduling
"""

import os
import json
import logging
import boto3
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import kubernetes
from kubernetes import client, config
import schedule
import time

from cost_analyzer import CostAnalyzer
from recommendations import RecommendationEngine
from bedrock_client import BedrockClient

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class CostOptimizationAgent:
    """
    AI-driven cost optimization agent using AgentCore for Amazon Bedrock
    """
    
    def __init__(self, cluster_name: str, region: str = 'us-west-2'):
        self.cluster_name = cluster_name
        self.region = region
        self.cost_analyzer = CostAnalyzer(cluster_name, region)
        self.recommendation_engine = RecommendationEngine(cluster_name, region)
        self.bedrock_client = BedrockClient(region)
        
        # Initialize Kubernetes client
        try:
            config.load_kube_config()
            self.k8s_client = client.CoreV1Api()
            self.k8s_apps_client = client.AppsV1Api()
        except Exception as e:
            logger.error(f"Failed to initialize Kubernetes client: {e}")
            self.k8s_client = None
            self.k8s_apps_client = None
        
        # Initialize AWS clients
        self.cloudwatch = boto3.client('cloudwatch', region_name=region)
        self.ec2 = boto3.client('ec2', region_name=region)
        self.s3 = boto3.client('s3', region_name=region)
        
        # Configuration
        self.optimization_thresholds = {
            'cpu_low': 20.0,      # CPU usage below 20% for scaling down
            'cpu_high': 80.0,     # CPU usage above 80% for scaling up
            'memory_low': 30.0,   # Memory usage below 30% for scaling down
            'memory_high': 85.0,  # Memory usage above 85% for scaling up
            'cost_savings_min': 10.0  # Minimum 10% cost savings to apply changes
        }
        
        logger.info(f"Cost Optimization Agent initialized for cluster: {cluster_name}")
    
    def collect_metrics(self) -> Dict:
        """
        Collect current metrics from CloudWatch and Kubernetes
        """
        logger.info("Collecting metrics...")
        
        metrics = {
            'timestamp': datetime.utcnow().isoformat(),
            'cluster_name': self.cluster_name,
            'node_metrics': {},
            'pod_metrics': {},
            'cost_metrics': {}
        }
        
        try:
            # Get EKS node metrics
            node_metrics = self.cost_analyzer.get_node_metrics()
            metrics['node_metrics'] = node_metrics
            
            # Get pod metrics
            if self.k8s_client:
                pod_metrics = self.cost_analyzer.get_pod_metrics()
                metrics['pod_metrics'] = pod_metrics
            
            # Get cost metrics
            cost_metrics = self.cost_analyzer.get_cost_metrics()
            metrics['cost_metrics'] = cost_metrics
            
            logger.info(f"Collected metrics for {len(node_metrics)} nodes")
            
        except Exception as e:
            logger.error(f"Error collecting metrics: {e}")
        
        return metrics
    
    def analyze_with_ai(self, metrics: Dict) -> Dict:
        """
        Use AgentCore to analyze metrics and generate recommendations
        """
        logger.info("Analyzing metrics with AI...")
        
        # Prepare context for AI analysis
        context = {
            'current_metrics': metrics,
            'optimization_thresholds': self.optimization_thresholds,
            'cluster_info': {
                'name': self.cluster_name,
                'region': self.region
            }
        }
        
        try:
            # Use AgentCore to analyze the situation
            ai_analysis = self.bedrock_client.analyze_cost_optimization(context)
            
            # Generate specific recommendations
            recommendations = self.recommendation_engine.generate_recommendations(
                metrics, ai_analysis
            )
            
            analysis_result = {
                'ai_analysis': ai_analysis,
                'recommendations': recommendations,
                'confidence_score': ai_analysis.get('confidence_score', 0.0),
                'estimated_savings': ai_analysis.get('estimated_savings', 0.0)
            }
            
            logger.info(f"AI analysis completed with confidence: {analysis_result['confidence_score']}")
            
        except Exception as e:
            logger.error(f"Error in AI analysis: {e}")
            analysis_result = {
                'ai_analysis': {},
                'recommendations': [],
                'confidence_score': 0.0,
                'estimated_savings': 0.0,
                'error': str(e)
            }
        
        return analysis_result
    
    def execute_recommendations(self, recommendations: List[Dict]) -> Dict:
        """
        Execute cost optimization recommendations
        """
        logger.info(f"Executing {len(recommendations)} recommendations...")
        
        execution_results = {
            'executed': [],
            'skipped': [],
            'failed': [],
            'total_savings_estimated': 0.0
        }
        
        for recommendation in recommendations:
            try:
                if recommendation.get('confidence_score', 0) < 0.7:
                    logger.info(f"Skipping recommendation due to low confidence: {recommendation['action']}")
                    execution_results['skipped'].append(recommendation)
                    continue
                
                # Execute the recommendation
                result = self._execute_single_recommendation(recommendation)
                
                if result['success']:
                    execution_results['executed'].append(recommendation)
                    execution_results['total_savings_estimated'] += result.get('estimated_savings', 0.0)
                    logger.info(f"Successfully executed: {recommendation['action']}")
                else:
                    execution_results['failed'].append(recommendation)
                    logger.error(f"Failed to execute: {recommendation['action']} - {result.get('error')}")
                    
            except Exception as e:
                logger.error(f"Error executing recommendation: {e}")
                execution_results['failed'].append(recommendation)
        
        logger.info(f"Execution completed: {len(execution_results['executed'])} successful, "
                   f"{len(execution_results['failed'])} failed")
        
        return execution_results
    
    def _execute_single_recommendation(self, recommendation: Dict) -> Dict:
        """
        Execute a single cost optimization recommendation
        """
        action_type = recommendation.get('action_type')
        
        try:
            if action_type == 'scale_pods':
                return self._scale_pods(recommendation)
            elif action_type == 'right_size_instance':
                return self._right_size_instance(recommendation)
            elif action_type == 'migrate_to_spot':
                return self._migrate_to_spot(recommendation)
            elif action_type == 'schedule_workload':
                return self._schedule_workload(recommendation)
            else:
                return {
                    'success': False,
                    'error': f'Unknown action type: {action_type}'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _scale_pods(self, recommendation: Dict) -> Dict:
        """
        Scale Kubernetes pods based on usage
        """
        namespace = recommendation.get('namespace')
        deployment_name = recommendation.get('deployment_name')
        target_replicas = recommendation.get('target_replicas')
        
        if not all([namespace, deployment_name, target_replicas]):
            return {'success': False, 'error': 'Missing required parameters'}
        
        try:
            # Scale the deployment
            self.k8s_apps_client.patch_namespaced_deployment_scale(
                name=deployment_name,
                namespace=namespace,
                body={'spec': {'replicas': target_replicas}}
            )
            
            return {
                'success': True,
                'estimated_savings': recommendation.get('estimated_savings', 0.0)
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _right_size_instance(self, recommendation: Dict) -> Dict:
        """
        Right-size EC2 instances based on usage patterns
        """
        instance_id = recommendation.get('instance_id')
        target_instance_type = recommendation.get('target_instance_type')
        
        if not all([instance_id, target_instance_type]):
            return {'success': False, 'error': 'Missing required parameters'}
        
        try:
            # Stop the instance
            self.ec2.stop_instances(InstanceIds=[instance_id])
            
            # Wait for instance to stop
            waiter = self.ec2.get_waiter('instance_stopped')
            waiter.wait(InstanceIds=[instance_id])
            
            # Modify instance type
            self.ec2.modify_instance_attribute(
                InstanceId=instance_id,
                InstanceType={'Value': target_instance_type}
            )
            
            # Start the instance
            self.ec2.start_instances(InstanceIds=[instance_id])
            
            return {
                'success': True,
                'estimated_savings': recommendation.get('estimated_savings', 0.0)
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _migrate_to_spot(self, recommendation: Dict) -> Dict:
        """
        Migrate workloads to spot instances
        """
        # This is a simplified implementation
        # In production, you'd need to handle pod disruption budgets and rolling updates
        logger.info(f"Spot migration recommended: {recommendation}")
        
        return {
            'success': True,
            'estimated_savings': recommendation.get('estimated_savings', 0.0)
        }
    
    def _schedule_workload(self, recommendation: Dict) -> Dict:
        """
        Schedule workloads during off-peak hours
        """
        # This would involve creating/updating Kubernetes CronJobs
        logger.info(f"Workload scheduling recommended: {recommendation}")
        
        return {
            'success': True,
            'estimated_savings': recommendation.get('estimated_savings', 0.0)
        }
    
    def store_analysis_data(self, metrics: Dict, analysis: Dict, execution_results: Dict):
        """
        Store analysis data in S3 for historical tracking
        """
        try:
            data = {
                'timestamp': datetime.utcnow().isoformat(),
                'metrics': metrics,
                'analysis': analysis,
                'execution_results': execution_results
            }
            
            # Store in S3
            bucket_name = f"{self.cluster_name}-cost-optimization"
            key = f"analysis/{datetime.utcnow().strftime('%Y/%m/%d')}/analysis_{datetime.utcnow().strftime('%H%M%S')}.json"
            
            self.s3.put_object(
                Bucket=bucket_name,
                Key=key,
                Body=json.dumps(data, indent=2),
                ContentType='application/json'
            )
            
            logger.info(f"Analysis data stored in S3: s3://{bucket_name}/{key}")
            
        except Exception as e:
            logger.error(f"Error storing analysis data: {e}")
    
    def run_optimization_cycle(self):
        """
        Run a complete cost optimization cycle
        """
        logger.info("Starting cost optimization cycle...")
        
        try:
            # 1. Collect metrics
            metrics = self.collect_metrics()
            
            # 2. Analyze with AI
            analysis = self.analyze_with_ai(metrics)
            
            # 3. Execute recommendations
            execution_results = self.execute_recommendations(analysis['recommendations'])
            
            # 4. Store results
            self.store_analysis_data(metrics, analysis, execution_results)
            
            # 5. Log summary
            total_savings = execution_results['total_savings_estimated']
            logger.info(f"Optimization cycle completed. Estimated savings: ${total_savings:.2f}")
            
            return {
                'success': True,
                'metrics': metrics,
                'analysis': analysis,
                'execution_results': execution_results
            }
            
        except Exception as e:
            logger.error(f"Error in optimization cycle: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def start_scheduled_optimization(self, interval_minutes: int = 15):
        """
        Start scheduled cost optimization
        """
        logger.info(f"Starting scheduled optimization every {interval_minutes} minutes...")
        
        schedule.every(interval_minutes).minutes.do(self.run_optimization_cycle)
        
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute

def main():
    """
    Main entry point for the cost optimization agent
    """
    cluster_name = os.getenv('CLUSTER_NAME', 'cost-optimizer-cluster')
    region = os.getenv('AWS_REGION', 'us-west-2')
    interval_minutes = int(os.getenv('OPTIMIZATION_INTERVAL_MINUTES', '15'))
    
    agent = CostOptimizationAgent(cluster_name, region)
    
    # Run initial optimization cycle
    logger.info("Running initial optimization cycle...")
    result = agent.run_optimization_cycle()
    
    if result['success']:
        logger.info("Initial optimization cycle completed successfully")
    else:
        logger.error(f"Initial optimization cycle failed: {result.get('error')}")
    
    # Start scheduled optimization
    agent.start_scheduled_optimization(interval_minutes)

if __name__ == "__main__":
    main() 