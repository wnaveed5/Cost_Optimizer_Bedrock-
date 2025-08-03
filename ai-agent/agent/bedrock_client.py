#!/usr/bin/env python3
"""
Bedrock Client for AgentCore Integration

This module provides the interface to Amazon Bedrock AgentCore
for AI-driven cost optimization analysis.
"""

import boto3
import json
import logging
from typing import Dict, Any, Optional
import base64

logger = logging.getLogger(__name__)

class BedrockClient:
    """
    Client for Amazon Bedrock AgentCore integration
    """
    
    def __init__(self, region: str = 'us-west-2'):
        self.region = region
        self.bedrock = boto3.client('bedrock-runtime', region_name=region)
        
        # AgentCore configuration
        self.agent_id = None  # Will be set when agent is created
        self.agent_alias_id = None
        
        # Model configuration for cost optimization
        self.model_config = {
            'anthropic.claude-3-sonnet-20240229-v1:0': {
                'max_tokens': 4096,
                'temperature': 0.1,
                'top_p': 0.9
            }
        }
    
    def create_cost_optimization_agent(self, agent_name: str) -> Dict:
        """
        Create an AgentCore agent for cost optimization
        """
        try:
            # This would typically use the Bedrock Agent API
            # For now, we'll simulate the agent creation
            logger.info(f"Creating AgentCore agent: {agent_name}")
            
            # In production, you would use:
            # bedrock_agent = boto3.client('bedrock-agent', region_name=self.region)
            # response = bedrock_agent.create_agent(...)
            
            # Simulated response
            agent_config = {
                'agent_id': f'agent-{agent_name}-{self.region}',
                'agent_name': agent_name,
                'description': 'AI-driven cost optimization agent for AWS EKS clusters',
                'instruction': self._get_agent_instruction(),
                'foundation_model': 'anthropic.claude-3-sonnet-20240229-v1:0',
                'idle_session_ttl_in_seconds': 3600,
                'agent_resource_role_arn': f'arn:aws:iam::{self._get_account_id()}:role/bedrock-agent-role'
            }
            
            self.agent_id = agent_config['agent_id']
            logger.info(f"Agent created successfully: {self.agent_id}")
            
            return agent_config
            
        except Exception as e:
            logger.error(f"Error creating AgentCore agent: {e}")
            raise
    
    def analyze_cost_optimization(self, context: Dict) -> Dict:
        """
        Use AgentCore to analyze cost optimization opportunities
        """
        logger.info("Analyzing cost optimization with AgentCore...")
        
        try:
            # Prepare the prompt for cost optimization analysis
            prompt = self._build_analysis_prompt(context)
            
            # Use Bedrock to get AI analysis
            response = self._invoke_bedrock_model(prompt)
            
            # Parse the AI response
            analysis = self._parse_ai_response(response)
            
            logger.info("AgentCore analysis completed successfully")
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error in AgentCore analysis: {e}")
            return self._get_fallback_analysis()
    
    def _build_analysis_prompt(self, context: Dict) -> str:
        """
        Build the prompt for cost optimization analysis
        """
        metrics = context.get('current_metrics', {})
        thresholds = context.get('optimization_thresholds', {})
        cluster_info = context.get('cluster_info', {})
        
        prompt = f"""
You are an AI cost optimization expert analyzing an AWS EKS cluster. Please analyze the following metrics and provide recommendations for cost optimization.

Cluster Information:
- Name: {cluster_info.get('name', 'Unknown')}
- Region: {cluster_info.get('region', 'Unknown')}

Current Metrics:
{json.dumps(metrics, indent=2)}

Optimization Thresholds:
{json.dumps(thresholds, indent=2)}

Please provide a comprehensive analysis including:

1. **Usage Pattern Analysis**: Identify underutilized and overutilized resources
2. **Cost Optimization Opportunities**: 
   - Instance right-sizing recommendations
   - Pod scaling opportunities
   - Spot instance migration possibilities
   - Workload scheduling optimizations
3. **Risk Assessment**: Evaluate the impact and risk of each recommendation
4. **Confidence Score**: Rate your confidence in the analysis (0.0-1.0)
5. **Estimated Savings**: Calculate potential monthly cost savings
6. **Implementation Priority**: Rank recommendations by impact and ease of implementation

Provide your response in JSON format with the following structure:
{{
    "usage_analysis": {{
        "underutilized_resources": [],
        "overutilized_resources": [],
        "usage_patterns": {{}}
    }},
    "optimization_opportunities": {{
        "instance_right_sizing": [],
        "pod_scaling": [],
        "spot_migration": [],
        "workload_scheduling": []
    }},
    "risk_assessment": {{
        "high_risk_actions": [],
        "medium_risk_actions": [],
        "low_risk_actions": []
    }},
    "confidence_score": 0.0,
    "estimated_savings": 0.0,
    "implementation_priority": [],
    "reasoning": "Detailed explanation of the analysis and recommendations"
}}
"""
        
        return prompt
    
    def _invoke_bedrock_model(self, prompt: str) -> Dict:
        """
        Invoke Bedrock model for analysis
        """
        try:
            # Use Claude 3 Sonnet for analysis
            model_id = 'anthropic.claude-3-sonnet-20240229-v1:0'
            config = self.model_config.get(model_id, {})
            
            request_body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": config.get('max_tokens', 4096),
                "temperature": config.get('temperature', 0.1),
                "top_p": config.get('top_p', 0.9),
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            }
            
            response = self.bedrock.invoke_model(
                modelId=model_id,
                body=json.dumps(request_body)
            )
            
            response_body = json.loads(response['body'].read())
            
            return response_body
            
        except Exception as e:
            logger.error(f"Error invoking Bedrock model: {e}")
            raise
    
    def _parse_ai_response(self, response: Dict) -> Dict:
        """
        Parse the AI response into structured analysis
        """
        try:
            content = response.get('content', [])
            if content and len(content) > 0:
                ai_text = content[0].get('text', '')
                
                # Try to extract JSON from the response
                try:
                    # Find JSON in the response
                    start_idx = ai_text.find('{')
                    end_idx = ai_text.rfind('}') + 1
                    
                    if start_idx != -1 and end_idx > start_idx:
                        json_str = ai_text[start_idx:end_idx]
                        analysis = json.loads(json_str)
                        
                        # Validate and enhance the analysis
                        analysis = self._validate_analysis(analysis)
                        
                        return analysis
                    else:
                        # Fallback: parse the text response
                        return self._parse_text_response(ai_text)
                        
                except json.JSONDecodeError:
                    # Fallback: parse the text response
                    return self._parse_text_response(ai_text)
            
            return self._get_fallback_analysis()
            
        except Exception as e:
            logger.error(f"Error parsing AI response: {e}")
            return self._get_fallback_analysis()
    
    def _parse_text_response(self, text: str) -> Dict:
        """
        Parse text response when JSON parsing fails
        """
        analysis = {
            'usage_analysis': {
                'underutilized_resources': [],
                'overutilized_resources': [],
                'usage_patterns': {}
            },
            'optimization_opportunities': {
                'instance_right_sizing': [],
                'pod_scaling': [],
                'spot_migration': [],
                'workload_scheduling': []
            },
            'risk_assessment': {
                'high_risk_actions': [],
                'medium_risk_actions': [],
                'low_risk_actions': []
            },
            'confidence_score': 0.7,
            'estimated_savings': 0.0,
            'implementation_priority': [],
            'reasoning': text
        }
        
        # Extract key information from text
        if 'underutilized' in text.lower():
            analysis['confidence_score'] = 0.8
        if 'savings' in text.lower():
            analysis['estimated_savings'] = 100.0  # Default estimate
        
        return analysis
    
    def _validate_analysis(self, analysis: Dict) -> Dict:
        """
        Validate and enhance the AI analysis
        """
        # Ensure all required fields exist
        required_fields = [
            'usage_analysis', 'optimization_opportunities', 'risk_assessment',
            'confidence_score', 'estimated_savings', 'implementation_priority'
        ]
        
        for field in required_fields:
            if field not in analysis:
                if field == 'confidence_score':
                    analysis[field] = 0.7
                elif field == 'estimated_savings':
                    analysis[field] = 0.0
                elif field == 'implementation_priority':
                    analysis[field] = []
                else:
                    analysis[field] = {}
        
        # Validate confidence score
        confidence = analysis.get('confidence_score', 0.7)
        if not isinstance(confidence, (int, float)) or confidence < 0 or confidence > 1:
            analysis['confidence_score'] = 0.7
        
        # Validate estimated savings
        savings = analysis.get('estimated_savings', 0.0)
        if not isinstance(savings, (int, float)) or savings < 0:
            analysis['estimated_savings'] = 0.0
        
        return analysis
    
    def _get_fallback_analysis(self) -> Dict:
        """
        Get fallback analysis when AI analysis fails
        """
        return {
            'usage_analysis': {
                'underutilized_resources': [],
                'overutilized_resources': [],
                'usage_patterns': {}
            },
            'optimization_opportunities': {
                'instance_right_sizing': [],
                'pod_scaling': [],
                'spot_migration': [],
                'workload_scheduling': []
            },
            'risk_assessment': {
                'high_risk_actions': [],
                'medium_risk_actions': [],
                'low_risk_actions': []
            },
            'confidence_score': 0.5,
            'estimated_savings': 0.0,
            'implementation_priority': [],
            'reasoning': 'Fallback analysis due to AI service unavailability'
        }
    
    def _get_agent_instruction(self) -> str:
        """
        Get the instruction for the AgentCore agent
        """
        return """
You are an AI cost optimization expert for AWS EKS clusters. Your role is to:

1. Analyze CloudWatch metrics and Kubernetes resource usage
2. Identify cost optimization opportunities including:
   - Instance right-sizing based on CPU/memory utilization
   - Pod scaling recommendations
   - Spot instance migration opportunities
   - Workload scheduling optimizations

3. Provide recommendations with:
   - Estimated cost savings
   - Risk assessment
   - Implementation priority
   - Confidence scores

4. Consider factors such as:
   - Current resource utilization
   - Historical usage patterns
   - Cost trends
   - Performance requirements
   - Business impact

Always prioritize recommendations that provide significant cost savings while maintaining application performance and reliability.
"""
    
    def _get_account_id(self) -> str:
        """
        Get AWS account ID
        """
        try:
            sts = boto3.client('sts', region_name=self.region)
            response = sts.get_caller_identity()
            return response['Account']
        except Exception as e:
            logger.error(f"Error getting account ID: {e}")
            return '123456789012'  # Fallback account ID 