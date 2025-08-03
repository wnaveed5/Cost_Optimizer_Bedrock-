# CloudWatch Log Group for EKS
resource "aws_cloudwatch_log_group" "eks" {
  name              = var.cloudwatch_log_group_name
  retention_in_days = 30

  tags = merge(var.tags, {
    Name = var.cloudwatch_log_group_name
  })
}

# S3 Bucket for Cost Optimization Data
resource "aws_s3_bucket" "cost_optimization" {
  bucket = var.cost_optimization_bucket_name

  tags = merge(var.tags, {
    Name = var.cost_optimization_bucket_name
  })
}

# S3 Bucket Versioning
resource "aws_s3_bucket_versioning" "cost_optimization" {
  bucket = aws_s3_bucket.cost_optimization.id
  versioning_configuration {
    status = "Enabled"
  }
}

# S3 Bucket Server Side Encryption
resource "aws_s3_bucket_server_side_encryption_configuration" "cost_optimization" {
  bucket = aws_s3_bucket.cost_optimization.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# S3 Bucket Public Access Block
resource "aws_s3_bucket_public_access_block" "cost_optimization" {
  bucket = aws_s3_bucket.cost_optimization.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# CloudWatch Dashboard for Cost Optimization
resource "aws_cloudwatch_dashboard" "cost_optimization" {
  dashboard_name = "${var.cluster_name}-cost-optimization"

  dashboard_body = jsonencode({
    widgets = [
      {
        type   = "metric"
        x      = 0
        y      = 0
        width  = 12
        height = 6
        properties = {
          metrics = [
            ["AWS/EKS", "cluster_failed_node_count", "ClusterName", var.cluster_name],
            [".", "cluster_node_count", ".", "."],
            [".", "cluster_scheduler_binding_errors", ".", "."]
          ]
          period = 300
          stat   = "Average"
          region = data.aws_region.current.name
          title  = "EKS Cluster Metrics"
        }
      },
      {
        type   = "metric"
        x      = 12
        y      = 0
        width  = 12
        height = 6
        properties = {
          metrics = [
            ["AWS/EC2", "CPUUtilization", "AutoScalingGroupName", "${var.cluster_name}-general"],
            [".", ".", ".", "${var.cluster_name}-spot"]
          ]
          period = 300
          stat   = "Average"
          region = data.aws_region.current.name
          title  = "EC2 CPU Utilization"
        }
      },
      {
        type   = "metric"
        x      = 0
        y      = 6
        width  = 12
        height = 6
        properties = {
          metrics = [
            ["AWS/EC2", "NetworkIn", "AutoScalingGroupName", "${var.cluster_name}-general"],
            [".", "NetworkOut", ".", "."]
          ]
          period = 300
          stat   = "Average"
          region = data.aws_region.current.name
          title  = "Network Traffic"
        }
      },
      {
        type   = "metric"
        x      = 12
        y      = 6
        width  = 12
        height = 6
        properties = {
          metrics = [
            ["AWS/EC2", "DiskReadOps", "AutoScalingGroupName", "${var.cluster_name}-general"],
            [".", "DiskWriteOps", ".", "."]
          ]
          period = 300
          stat   = "Average"
          region = data.aws_region.current.name
          title  = "Disk Operations"
        }
      }
    ]
  })
}

# CloudWatch Alarms for Cost Optimization
resource "aws_cloudwatch_metric_alarm" "high_cpu" {
  alarm_name          = "${var.cluster_name}-high-cpu"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "2"
  metric_name         = "CPUUtilization"
  namespace           = "AWS/EC2"
  period              = "300"
  statistic           = "Average"
  threshold           = "80"
  alarm_description   = "This metric monitors EC2 CPU utilization"
  alarm_actions       = [aws_sns_topic.cost_optimization.arn]

  dimensions = {
    AutoScalingGroupName = "${var.cluster_name}-general"
  }
}

resource "aws_cloudwatch_metric_alarm" "low_cpu" {
  alarm_name          = "${var.cluster_name}-low-cpu"
  comparison_operator = "LessThanThreshold"
  evaluation_periods  = "4"
  metric_name         = "CPUUtilization"
  namespace           = "AWS/EC2"
  period              = "300"
  statistic           = "Average"
  threshold           = "20"
  alarm_description   = "This metric monitors low EC2 CPU utilization for cost optimization"
  alarm_actions       = [aws_sns_topic.cost_optimization.arn]

  dimensions = {
    AutoScalingGroupName = "${var.cluster_name}-general"
  }
}

# SNS Topic for Cost Optimization Alerts
resource "aws_sns_topic" "cost_optimization" {
  name = "${var.cluster_name}-cost-optimization-alerts"

  tags = merge(var.tags, {
    Name = "${var.cluster_name}-cost-optimization-alerts"
  })
}

# SNS Topic Policy
resource "aws_sns_topic_policy" "cost_optimization" {
  arn = aws_sns_topic.cost_optimization.arn

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "cloudwatch.amazonaws.com"
        }
        Action   = "SNS:Publish"
        Resource = aws_sns_topic.cost_optimization.arn
      }
    ]
  })
}

# Data source for current AWS region
data "aws_region" "current" {} 