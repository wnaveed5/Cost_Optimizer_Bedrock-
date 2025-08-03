terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# VPC Module
module "vpc" {
  source = "./modules/vpc"
  
  vpc_cidr             = var.vpc_cidr
  environment          = var.environment
  availability_zones   = var.availability_zones
  private_subnet_cidrs = var.private_subnet_cidrs
  public_subnet_cidrs  = var.public_subnet_cidrs
}

# EKS Module
module "eks" {
  source = "./modules/eks"
  
  cluster_name    = var.cluster_name
  cluster_version = var.cluster_version
  environment     = var.environment
  
  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnet_ids
  
  node_groups = {
    general = {
      desired_capacity = 2
      max_capacity     = 4
      min_capacity     = 1
      
      instance_types = ["t3.medium", "t3.large"]
      capacity_type  = "ON_DEMAND"
      
      labels = {
        Environment = var.environment
        NodeGroup   = "general"
      }
      
      tags = {
        ExtraTag = "eks-node-group"
      }
    }
    
    spot = {
      desired_capacity = 1
      max_capacity     = 3
      min_capacity     = 0
      
      instance_types = ["t3.medium", "t3.large"]
      capacity_type  = "SPOT"
      
      labels = {
        Environment = var.environment
        NodeGroup   = "spot"
      }
      
      tags = {
        ExtraTag = "eks-spot-node-group"
      }
    }
  }
}

# Monitoring Module
module "monitoring" {
  source = "./modules/monitoring"
  
  cluster_name = var.cluster_name
  environment  = var.environment
  
  # CloudWatch Log Group for EKS
  cloudwatch_log_group_name = "/aws/eks/${var.cluster_name}/cluster"
  
  # S3 bucket for cost optimization data
  cost_optimization_bucket_name = "${var.cluster_name}-cost-optimization-${random_string.bucket_suffix.result}"
}

# Random string for unique bucket names
resource "random_string" "bucket_suffix" {
  length  = 8
  special = false
  upper   = false
}

# IAM Role for AI Agent
resource "aws_iam_role" "ai_agent_role" {
  name = "${var.cluster_name}-ai-agent-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      }
    ]
  })
}

# IAM Policy for AI Agent
resource "aws_iam_role_policy" "ai_agent_policy" {
  name = "${var.cluster_name}-ai-agent-policy"
  role = aws_iam_role.ai_agent_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "cloudwatch:GetMetricData",
          "cloudwatch:GetMetricStatistics",
          "cloudwatch:ListMetrics",
          "ec2:DescribeInstances",
          "ec2:DescribeInstanceTypes",
          "ec2:ModifyInstanceAttribute",
          "eks:DescribeCluster",
          "eks:ListClusters",
          "s3:GetObject",
          "s3:PutObject",
          "s3:ListBucket",
          "bedrock:InvokeModel",
          "bedrock:InvokeModelWithResponseStream"
        ]
        Resource = "*"
      }
    ]
  })
}

# S3 Bucket for Dashboard
resource "aws_s3_bucket" "dashboard_bucket" {
  bucket = "${var.cluster_name}-dashboard-${random_string.bucket_suffix.result}"
}

resource "aws_s3_bucket_website_configuration" "dashboard_bucket" {
  bucket = aws_s3_bucket.dashboard_bucket.id

  index_document {
    suffix = "index.html"
  }

  error_document {
    key = "index.html"
  }
}

resource "aws_s3_bucket_public_access_block" "dashboard_bucket" {
  bucket = aws_s3_bucket.dashboard_bucket.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

resource "aws_s3_bucket_policy" "dashboard_bucket" {
  bucket = aws_s3_bucket.dashboard_bucket.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid       = "PublicReadGetObject"
        Effect    = "Allow"
        Principal = "*"
        Action    = "s3:GetObject"
        Resource  = "${aws_s3_bucket.dashboard_bucket.arn}/*"
      }
    ]
  })
} 