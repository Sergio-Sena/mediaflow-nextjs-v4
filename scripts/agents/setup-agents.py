"""
MidiaFlow - Setup Bedrock Agents
"""
import boto3
import json
import time

REGION = 'us-east-1'
ACCOUNT_ID = '969430605054'
ROLE_ARN = f'arn:aws:iam::{ACCOUNT_ID}:role/midiaflow-bedrock-agent-role'

bedrock_agent = boto3.client('bedrock-agent', region_name=REGION)


def create_agent(name, instruction):
    """Create a Bedrock Agent."""
    print(f"  Creating agent: {name}...")

    try:
        resp = bedrock_agent.create_agent(
            agentName=name,
            agentResourceRoleArn=ROLE_ARN,
            foundationModel='anthropic.claude-3-haiku-20240307-v1:0',
            instruction=instruction,
            idleSessionTTLInSeconds=600
        )
        agent_id = resp['agent']['agentId']
        print(f"  Created: {agent_id}")

        time.sleep(3)
        bedrock_agent.prepare_agent(agentId=agent_id)
        print(f"  Prepared: {agent_id}")
        return agent_id
    except Exception as e:
        if 'ConflictException' in str(type(e)) or 'already' in str(e).lower():
            agents = bedrock_agent.list_agents()
            for a in agents['agentSummaries']:
                if a['agentName'] == name:
                    print(f"  Already exists: {a['agentId']}")
                    return a['agentId']
        print(f"  Error: {e}")
        return None


def main():
    print("=" * 50)
    print("MidiaFlow - Bedrock Agents Setup")
    print("=" * 50)

    security_id = create_agent(
        'midiaflow-security-auditor',
        "You are a Security and Compliance auditor for AWS infrastructure. "
        "Analyze Terraform code, Lambda functions, and IAM policies to find: "
        "exposed secrets, overly permissive IAM, missing encryption, missing HTTPS, "
        "CORS misconfigurations, missing authentication. "
        "Respond with JSON: {\"status\": \"PASS\" or \"FAIL\", \"findings\": [{\"severity\": \"HIGH/MEDIUM/LOW\", \"resource\": \"...\", \"issue\": \"...\", \"fix\": \"...\"}]}"
    )

    finops_id = create_agent(
        'midiaflow-finops-auditor',
        "You are a FinOps auditor for AWS infrastructure. "
        "Analyze Terraform code and AWS configurations to find cost optimization: "
        "over-provisioned Lambda memory, S3 storage class optimization, "
        "DynamoDB capacity analysis, CloudFront cache optimization, unused resources. "
        "Respond with JSON: {\"status\": \"OPTIMIZED\" or \"NEEDS_OPTIMIZATION\", \"current_cost\": \"$X.XX/month\", \"potential_savings\": \"$X.XX/month\", \"recommendations\": [{\"resource\": \"...\", \"recommended\": \"...\", \"savings\": \"$X.XX\"}]}"
    )

    code_id = create_agent(
        'midiaflow-code-auditor',
        "You are a Code Quality auditor for serverless applications. "
        "Analyze Python Lambda functions and TypeScript/React code to find: "
        "missing error handling, hardcoded values, missing input validation, "
        "performance issues, dead code, missing logging. "
        "Respond with JSON: {\"status\": \"PASS\" or \"NEEDS_REVIEW\", \"findings\": [{\"severity\": \"HIGH/MEDIUM/LOW\", \"file\": \"...\", \"issue\": \"...\", \"fix\": \"...\"}]}"
    )

    leader_id = create_agent(
        'midiaflow-leader',
        "You are the Lead Orchestrator for the MidiaFlow audit team. "
        "Coordinate 3 specialists: Security Auditor, FinOps Auditor, Code Auditor. "
        "Compile their reports into a summary with: overall status (APPROVED/NEEDS_ATTENTION/BLOCKED), "
        "critical findings that block deployment, recommendations by impact, cost impact. "
        "If all agents PASS, approve deployment. If any HIGH severity, block deployment."
    )

    print("\n" + "=" * 50)
    print("Setup complete!")
    print(f"  Security: {security_id}")
    print(f"  FinOps:   {finops_id}")
    print(f"  Code:     {code_id}")
    print(f"  Leader:   {leader_id}")
    print("=" * 50)


if __name__ == '__main__':
    main()
