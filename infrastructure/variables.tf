variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-west-2"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "cost-optimization"
}

variable "cluster_name" {
  description = "Name of the EKS cluster"
  type        = string
  default     = "cost-optimizer-cluster"
}

variable "cluster_version" {
  description = "Kubernetes version for EKS cluster"
  type        = string
  default     = "1.28"
}

variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "availability_zones" {
  description = "Availability zones"
  type        = list(string)
  default     = ["us-west-2a", "us-west-2b", "us-west-2c"]
}

variable "private_subnet_cidrs" {
  description = "CIDR blocks for private subnets"
  type        = list(string)
  default     = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
}

variable "public_subnet_cidrs" {
  description = "CIDR blocks for public subnets"
  type        = list(string)
  default     = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]
}

variable "node_groups" {
  description = "EKS node groups configuration"
  type = map(object({
    desired_capacity = number
    max_capacity     = number
    min_capacity     = number
    instance_types   = list(string)
    capacity_type    = string
    labels           = map(string)
    tags             = map(string)
  }))
  default = {}
}

variable "enable_spot_instances" {
  description = "Enable spot instances for cost optimization"
  type        = bool
  default     = true
}

variable "ai_agent_image" {
  description = "Docker image for AI agent"
  type        = string
  default     = "cost-optimizer-agent:latest"
}

variable "dashboard_domain" {
  description = "Domain for dashboard (optional)"
  type        = string
  default     = ""
}

variable "enable_cloudwatch_logs" {
  description = "Enable CloudWatch logs for EKS"
  type        = bool
  default     = true
}

variable "enable_s3_vectors" {
  description = "Enable S3 Vectors for embeddings storage"
  type        = bool
  default     = true
}

variable "cost_optimization_schedule" {
  description = "Cron schedule for cost optimization checks"
  type        = string
  default     = "*/15 * * * *"  # Every 15 minutes
}

variable "tags" {
  description = "Tags to apply to all resources"
  type        = map(string)
  default = {
    Project     = "cost-optimization"
    Environment = "cost-optimization"
    ManagedBy   = "terraform"
  }
} 