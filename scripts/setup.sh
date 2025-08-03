#!/bin/bash

# AI-Driven Cost Optimization Agent Setup Script
# This script sets up the complete project environment

set -e

echo "🚀 Setting up AI-Driven Cost Optimization Agent..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if required tools are installed
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    # Check AWS CLI
    if ! command -v aws &> /dev/null; then
        print_error "AWS CLI is not installed. Please install it first."
        exit 1
    fi
    
    # Check Terraform
    if ! command -v terraform &> /dev/null; then
        print_error "Terraform is not installed. Please install it first."
        exit 1
    fi
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install it first."
        exit 1
    fi
    
    # Check kubectl
    if ! command -v kubectl &> /dev/null; then
        print_error "kubectl is not installed. Please install it first."
        exit 1
    fi
    
    # Check Node.js
    if ! command -v node &> /dev/null; then
        print_error "Node.js is not installed. Please install it first."
        exit 1
    fi
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is not installed. Please install it first."
        exit 1
    fi
    
    print_success "All prerequisites are installed!"
}

# Setup Python environment for AI agent
setup_python_env() {
    print_status "Setting up Python environment for AI agent..."
    
    cd ai-agent
    
    # Create virtual environment
    python3 -m venv venv
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Install dependencies
    pip install -r requirements.txt
    
    print_success "Python environment setup complete!"
    cd ..
}

# Setup Node.js environment for dashboard
setup_node_env() {
    print_status "Setting up Node.js environment for dashboard..."
    
    cd dashboard
    
    # Install dependencies
    npm install
    
    print_success "Node.js environment setup complete!"
    cd ..
}

# Setup sample workload
setup_sample_workload() {
    print_status "Setting up sample workload..."
    
    cd sample-workload
    
    # Install dependencies
    npm install
    
    print_success "Sample workload setup complete!"
    cd ..
}

# Create necessary directories
create_directories() {
    print_status "Creating necessary directories..."
    
    mkdir -p logs
    mkdir -p config
    mkdir -p data
    
    print_success "Directories created!"
}

# Setup AWS configuration
setup_aws_config() {
    print_status "Setting up AWS configuration..."
    
    # Check if AWS credentials are configured
    if ! aws sts get-caller-identity &> /dev/null; then
        print_warning "AWS credentials not configured. Please run 'aws configure' first."
        print_status "You can also set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables."
    else
        print_success "AWS credentials are configured!"
    fi
}

# Create configuration files
create_config_files() {
    print_status "Creating configuration files..."
    
    # Create .env file for the AI agent
    cat > ai-agent/.env << EOF
# AI Agent Configuration
CLUSTER_NAME=cost-optimizer-cluster
AWS_REGION=us-west-2
OPTIMIZATION_INTERVAL_MINUTES=15
BEDROCK_MODEL_ID=anthropic.claude-3-sonnet-20240229-v1:0
LOG_LEVEL=INFO
EOF
    
    # Create .env file for the dashboard
    cat > dashboard/.env << EOF
# Dashboard Configuration
REACT_APP_API_URL=http://localhost:3001
REACT_APP_CLUSTER_NAME=cost-optimizer-cluster
REACT_APP_AWS_REGION=us-west-2
EOF
    
    print_success "Configuration files created!"
}

# Build Docker images
build_docker_images() {
    print_status "Building Docker images..."
    
    # Build AI agent image
    cd ai-agent
    docker build -t cost-optimizer-agent:latest .
    cd ..
    
    # Build sample workload image
    cd sample-workload
    docker build -t sample-ecommerce-app:latest .
    cd ..
    
    print_success "Docker images built successfully!"
}

# Create deployment scripts
create_deployment_scripts() {
    print_status "Creating deployment scripts..."
    
    # Create deployment script
    cat > scripts/deploy.sh << 'EOF'
#!/bin/bash

# Deploy the complete cost optimization system

set -e

echo "🚀 Deploying AI-Driven Cost Optimization Agent..."

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

# Deploy infrastructure
print_status "Deploying infrastructure with Terraform..."
cd infrastructure
terraform init
terraform plan
terraform apply -auto-approve
cd ..

# Get cluster info
CLUSTER_NAME=$(terraform -chdir=infrastructure output -raw cluster_name)
AWS_REGION=$(terraform -chdir=infrastructure output -raw aws_region)

# Configure kubectl
print_status "Configuring kubectl..."
aws eks update-kubeconfig --region $AWS_REGION --name $CLUSTER_NAME

# Deploy sample workload
print_status "Deploying sample workload..."
kubectl apply -f sample-workload/k8s/

# Deploy AI agent
print_status "Deploying AI agent..."
kubectl apply -f ai-agent/k8s/

# Build and deploy dashboard
print_status "Building and deploying dashboard..."
cd dashboard
npm run build
aws s3 sync build/ s3://$(terraform -chdir=../infrastructure output -raw dashboard_bucket_name) --delete
cd ..

print_success "Deployment completed successfully!"
echo "Dashboard URL: $(terraform -chdir=infrastructure output -raw dashboard_website_endpoint)"
EOF
    
    chmod +x scripts/deploy.sh
    
    # Create destroy script
    cat > scripts/destroy.sh << 'EOF'
#!/bin/bash

# Destroy the cost optimization infrastructure

set -e

echo "🗑️  Destroying AI-Driven Cost Optimization Agent..."

# Colors for output
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${RED}[WARNING]${NC} $1"
}

# Confirm destruction
read -p "Are you sure you want to destroy all resources? This action cannot be undone. (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Destruction cancelled."
    exit 1
fi

# Destroy infrastructure
print_status "Destroying infrastructure..."
cd infrastructure
terraform destroy -auto-approve
cd ..

print_warning "All resources have been destroyed!"
EOF
    
    chmod +x scripts/destroy.sh
    
    print_success "Deployment scripts created!"
}

# Main setup function
main() {
    echo "=========================================="
    echo "AI-Driven Cost Optimization Agent Setup"
    echo "=========================================="
    echo ""
    
    check_prerequisites
    create_directories
    setup_aws_config
    create_config_files
    setup_python_env
    setup_node_env
    setup_sample_workload
    build_docker_images
    create_deployment_scripts
    
    echo ""
    echo "=========================================="
    print_success "Setup completed successfully!"
    echo "=========================================="
    echo ""
    echo "Next steps:"
    echo "1. Configure your AWS credentials: aws configure"
    echo "2. Deploy the infrastructure: ./scripts/deploy.sh"
    echo "3. Access the dashboard at the URL provided after deployment"
    echo ""
    echo "For more information, see the README.md file."
}

# Run main function
main "$@" 