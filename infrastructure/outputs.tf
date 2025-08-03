output "cluster_endpoint" {
  description = "Endpoint for EKS control plane"
  value       = module.eks.cluster_endpoint
}

output "cluster_security_group_id" {
  description = "Security group ID attached to the EKS cluster"
  value       = module.eks.cluster_security_group_id
}

output "cluster_iam_role_name" {
  description = "IAM role name associated with EKS cluster"
  value       = module.eks.cluster_iam_role_name
}

output "cluster_certificate_authority_data" {
  description = "Base64 encoded certificate data required to communicate with the cluster"
  value       = module.eks.cluster_certificate_authority_data
}

output "vpc_id" {
  description = "VPC ID"
  value       = module.vpc.vpc_id
}

output "private_subnet_ids" {
  description = "List of private subnet IDs"
  value       = module.vpc.private_subnet_ids
}

output "public_subnet_ids" {
  description = "List of public subnet IDs"
  value       = module.vpc.public_subnet_ids
}

output "ai_agent_role_arn" {
  description = "ARN of the IAM role for AI agent"
  value       = aws_iam_role.ai_agent_role.arn
}

output "dashboard_bucket_name" {
  description = "Name of the S3 bucket for dashboard hosting"
  value       = aws_s3_bucket.dashboard_bucket.bucket
}

output "dashboard_website_endpoint" {
  description = "S3 website endpoint for dashboard"
  value       = aws_s3_bucket_website_configuration.dashboard_bucket.website_endpoint
}

output "cost_optimization_bucket_name" {
  description = "Name of the S3 bucket for cost optimization data"
  value       = module.monitoring.cost_optimization_bucket_name
}

output "cloudwatch_log_group_name" {
  description = "Name of the CloudWatch log group"
  value       = module.monitoring.cloudwatch_log_group_name
}

output "kubeconfig_command" {
  description = "Command to configure kubectl"
  value       = "aws eks update-kubeconfig --region ${var.aws_region} --name ${var.cluster_name}"
}

output "deployment_instructions" {
  description = "Instructions for deploying the application"
  value = <<-EOT
    # Configure kubectl
    aws eks update-kubeconfig --region ${var.aws_region} --name ${var.cluster_name}
    
    # Deploy AI Agent
    cd ai-agent
    docker build -t cost-optimizer-agent .
    kubectl apply -f k8s/
    
    # Deploy Sample Workload
    cd ../sample-workload
    kubectl apply -f k8s/
    
    # Deploy Dashboard
    cd ../dashboard
    npm install
    npm run build
    aws s3 sync build/ s3://${aws_s3_bucket.dashboard_bucket.bucket}
    
    # Dashboard URL: http://${aws_s3_bucket_website_configuration.dashboard_bucket.website_endpoint}
  EOT
} 