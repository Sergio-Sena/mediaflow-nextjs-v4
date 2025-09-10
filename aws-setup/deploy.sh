#!/bin/bash

# Mediaflow AWS Infrastructure Deployment
echo "🚀 Deploying Mediaflow AWS Infrastructure..."

# Deploy CloudFormation stack
aws cloudformation deploy \
  --template-file mediaflow-infrastructure.yaml \
  --stack-name mediaflow-infrastructure \
  --capabilities CAPABILITY_NAMED_IAM \
  --region us-east-1

# Get outputs
echo "📋 Getting stack outputs..."
aws cloudformation describe-stacks \
  --stack-name mediaflow-infrastructure \
  --query 'Stacks[0].Outputs' \
  --output table

echo "✅ Deployment complete!"