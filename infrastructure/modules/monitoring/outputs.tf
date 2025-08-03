output "cloudwatch_log_group_name" {
  description = "Name of the CloudWatch log group"
  value       = aws_cloudwatch_log_group.eks.name
}

output "cost_optimization_bucket_name" {
  description = "Name of the S3 bucket for cost optimization data"
  value       = aws_s3_bucket.cost_optimization.bucket
} 