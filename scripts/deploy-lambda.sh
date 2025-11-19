#!/bin/bash

# Deploy Lambda function
cd aws-setup/lambda-functions/upload-handler

# Create deployment package
rm -f lambda_function.zip
zip -r lambda_function.zip lambda_function.py ../lib/

# Deploy to AWS
aws lambda update-function-code \
  --function-name midiaflow-upload-handler \
  --zip-file fileb://lambda_function.zip \
  --region us-east-1

echo "Lambda deployed successfully!"
