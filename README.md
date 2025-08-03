# AI-Driven Cost Optimization Agent with AgentCore for Amazon Bedrock

## Project Overview

This project utilizes an AI-powered cost optimization agent for AWS infrastructure using AgentCore for Amazon Bedrock. The agent is tracking an AWS EKS cluster that is executing a sample workload and assessing usage metrics via CloudWatch in order to recommend and apply cost-saving solutions.

 Architecture


┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐

│   React         │    │   AgentCore     │    │   S3 Vectors    │

│   Dashboard     │◄──►│   AI Agent      │◄──►│   (Embeddings)  │

│   (S3/Amplify)  │    │   (Bedrock)     │    │                 │

└─────────────────┘    └─────────────────┘    └─────────────────┘

│                       │                       │

│                       │                       │

▼                       ▼                       ▼

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐

│   CloudWatch    │    │   EKS Cluster   │    │   Terraform     │

│   Metrics       │    │   (Sample       │    │   Infrastructure│

│                 │    │    Workload)    │    │                 │

└─────────────────┘    └─────────────────┘    └─────────────────┘

│                       │                       │

│                       │                       │

▼                       ▼                       ▼

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐

│   Jenkins       │    │   ArgoCD        │    │   Cost          │

│   CI/CD         │    │   GitOps        │    │   Optimization  │

└─────────────────┘    └─────────────────┘    └─────────────────┘



## Key Features



- AI Agent:  AgentCore in Amazon Bedrock for autonomous decision-making

- Cost Optimization:  Right sizing the EC2 instances, scaling the Kubernetes pods, scheduling the workloads to optimize for cost

- Predictive Analytics: Leveraging the historical data stored as embeddings in S3 Vectors

- GitOps: Uses ArgoCD for Kubernetes manifest management for easy fix and rollback.

- CI/CD* Uses Jenkins automation for deployments

- Dashboard: Built a  React frontend for cost visualization and AI recommendations


Project Structure


Cost_Optimizer_Bedrock-/

├── infrastructure/          # Terraform configurations

│   ├── main.tf

│   ├── variables.tf

│   ├── outputs.tf

│   └── modules/

│       ├── vpc/

│       ├── eks/

│       └── monitoring/

├── ai-agent/                # AgentCore AI agent

│   ├── agent/

│   │   ├── main.py

│   │   ├── cost_analyzer.py

│   │   └── recommendations.py

│   ├── requirements.txt

│   └── Dockerfile

├── sample-workload/         # Sample Node.js application

│   ├── app/

│   ├── Dockerfile

│   └── k8s/

├── dashboard/               # React frontend

│   ├── src/

│   ├── public/

│   └── package.json

├── jenkins/                 # Jenkins pipeline configurations

│   └── Jenkinsfile

├── argocd/                   # ArgoCD application manifests

│   └── applications/

├── scripts/                  # Utility scripts

│   ├── setup.sh

│   └── deploy.sh

└── docs/                    # Documentation

    ├── architecture.md

    └── api.md



Prerequisites



- AWS CLI with appropriate permissions setup

- Terraform >= 1.0

- Docker

- Node.js >= 18

- Python >= 3.9

- kubectl

- Jenkins (or access to a Jenkins server)



## Quick Start



1. **Clone and Setup**:

   ```bash

   git clone <repository-url>

cd Cost_Optimizer_Bedrock-

   ./scripts/setup.sh

   ```



2. **Deploy Infrastructure**:

   ```bash

   cd infrastructure

   terraform init

   terraform plan

   terraform apply

   ```



3. **Deploy AI Agent**:

   ```bash

   cd ai-agent

   docker build -t cost-optimizer-agent .

   docker run -d --name cost-agent cost-optimizer-agent

   ```



4. **Deploy Dashboard**:

   ```bash

cd dashboard

   npm install

   npm run build

   aws s3 sync build/ s3://your-dashboard-bucket

   ```

## Cost Optimization Features


### AI Agent Capabilities

- **Instance Right-sizing**: Analyze CPU/memory usage to recommend optimal instance types

- **Pod Scaling**: Scale down unused Kubernetes pods during low usage periods

- **Spot Instance Migration**: Migrate workloads to Spot instances where appropriate

- **Scheduling Optimization**: Run non-essential workloads during off-peak hours



### Predictive Analytics

- Store historical CloudWatch metrics as embeddings in S3 Vectors

- Predict future usage patterns for proactive optimization

- Offer cost-saving recommendations based on historical history


### Dashboard Features

- Real-time cost trend visualization

- Show AI recommendations

- Cost savings metrics

- Infrastructure health monitoring


## Expected Results

- **Cost Reduction**: Svae 20-30% AWS costs with intelligent optimization

- **Response Time**: The AI agent responds to optimization opportunities within 5 minutes of it finding an issue

- **Accuracy**: 85%+ accuracy in cost-saving recommendations

- **Automation**: 90% of optimization actions executed automatically

<img width="1468" height="701" alt="Screenshot 2025-08-03 at 5 38 23 PM" src="https://github.com/user-attachments/assets/f84f91f4-45ca-453b-a986-a960a171ed2a" />
