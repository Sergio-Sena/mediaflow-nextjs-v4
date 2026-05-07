"""
MidiaFlow - AI Audit (runs in CI/CD pipeline)
Invokes Bedrock agents to audit code, security and costs before deploy.
"""
import boto3
import json
import os
import glob

REGION = os.environ.get('AWS_REGION', 'us-east-1')
AGENT_IDS = {
    'security': 'QUPFUXIZLB',
    'finops': 'GBV310SOWB',
    'code': 'BDX5I9BDUK'
}

bedrock_runtime = boto3.client('bedrock-runtime', region_name=REGION)


def get_code_summary():
    """Collect key files for audit."""
    files_to_audit = []

    # Lambda functions
    for f in glob.glob('aws-setup/lambda-functions/*/lambda_function.py'):
        content = open(f, 'r', encoding='utf-8').read()[:2000]
        files_to_audit.append(f"### {f}\n{content}")

    for f in glob.glob('aws-setup/lambda-functions/*/index.py'):
        content = open(f, 'r', encoding='utf-8').read()[:2000]
        files_to_audit.append(f"### {f}\n{content}")

    # Terraform
    for f in glob.glob('infra/modules/*/main.tf'):
        content = open(f, 'r', encoding='utf-8').read()[:2000]
        files_to_audit.append(f"### {f}\n{content}")

    return "\n\n".join(files_to_audit[:15])  # Limit to avoid token overflow


def invoke_audit(role, prompt):
    """Invoke Bedrock Claude for audit."""
    try:
        resp = bedrock_runtime.invoke_model(
            modelId='anthropic.claude-3-haiku-20240307-v1:0',
            contentType='application/json',
            accept='application/json',
            body=json.dumps({
                'anthropic_version': 'bedrock-2023-05-31',
                'max_tokens': 1000,
                'messages': [{'role': 'user', 'content': prompt}]
            })
        )
        result = json.loads(resp['body'].read())
        return result['content'][0]['text']
    except Exception as e:
        return json.dumps({"status": "ERROR", "message": str(e)})


def main():
    print("=" * 50)
    print("MidiaFlow - AI Audit")
    print("=" * 50)

    code_summary = get_code_summary()

    if not code_summary:
        print("No files found to audit. Skipping.")
        return

    # Security Audit
    print("\n[1/5] Security Audit...")
    security_result = invoke_audit('security',
        f"You are a Security auditor. Analyze this AWS infrastructure code for vulnerabilities. "
        f"Check for: exposed secrets, overly permissive IAM, missing encryption, missing auth. "
        f"Respond ONLY with JSON: {{\"status\": \"PASS\" or \"FAIL\", \"findings\": [{{\"severity\": \"HIGH/MEDIUM/LOW\", \"resource\": \"...\", \"issue\": \"...\", \"fix\": \"...\"}}]}}\n\n"
        f"CODE:\n{code_summary[:8000]}"
    )
    print(f"  Result: {security_result[:200]}")

    # FinOps Audit
    print("\n[2/5] FinOps Audit...")
    finops_result = invoke_audit('finops',
        f"You are a FinOps auditor. Analyze this AWS infrastructure for cost optimization. "
        f"Check for: over-provisioned resources, storage optimization, right-sizing. "
        f"Current cost: $0.83/month. "
        f"Respond ONLY with JSON: {{\"status\": \"OPTIMIZED\" or \"NEEDS_OPTIMIZATION\", \"recommendations\": [{{\"resource\": \"...\", \"recommended\": \"...\", \"savings\": \"$X.XX\"}}]}}\n\n"
        f"CODE:\n{code_summary[:8000]}"
    )
    print(f"  Result: {finops_result[:200]}")

    # Code Quality Audit
    print("\n[3/5] Code Quality Audit...")
    code_result = invoke_audit('code',
        f"You are a Code Quality auditor. Analyze these Python Lambda functions for: "
        f"missing error handling, hardcoded values, missing validation, performance issues. "
        f"Respond ONLY with JSON: {{\"status\": \"PASS\" or \"NEEDS_REVIEW\", \"findings\": [{{\"severity\": \"HIGH/MEDIUM/LOW\", \"file\": \"...\", \"issue\": \"...\", \"fix\": \"...\"}}]}}\n\n"
        f"CODE:\n{code_summary[:8000]}"
    )
    print(f"  Result: {code_result[:200]}")

    # Compliance Audit
    print("\n[4/5] Compliance Audit (LGPD/GDPR)...")
    compliance_result = invoke_audit('compliance',
        f"You are a Compliance auditor for LGPD and GDPR. Analyze this code for: "
        f"personal data stored without encryption, user data exposed in logs, missing data retention, "
        f"missing consent mechanisms, data shared without authorization. "
        f"Respond ONLY with JSON: {{\"status\": \"COMPLIANT\" or \"NON_COMPLIANT\", \"findings\": [{{\"severity\": \"HIGH/MEDIUM/LOW\", \"regulation\": \"LGPD/GDPR\", \"issue\": \"...\", \"fix\": \"...\"}}]}}\n\n"
        f"CODE:\n{code_summary[:8000]}"
    )
    print(f"  Result: {compliance_result[:200]}")

    # Performance Audit
    print("\n[5/5] Performance Audit...")
    performance_result = invoke_audit('performance',
        f"You are a Performance auditor for serverless AWS. Analyze this code for: "
        f"Lambda cold start issues, SDK initializations inside handlers, missing connection reuse, "
        f"N+1 queries, oversized payloads, synchronous calls that could be async. "
        f"Respond ONLY with JSON: {{\"status\": \"OPTIMIZED\" or \"NEEDS_OPTIMIZATION\", \"findings\": [{{\"severity\": \"HIGH/MEDIUM/LOW\", \"resource\": \"...\", \"issue\": \"...\", \"fix\": \"...\"}}]}}\n\n"
        f"CODE:\n{code_summary[:8000]}"
    )
    print(f"  Result: {performance_result[:200]}")

    # Summary
    print("\n" + "=" * 50)
    print("AUDIT SUMMARY")
    print("=" * 50)

    all_pass = True
    for name, result in [('Security', security_result), ('FinOps', finops_result), ('Code', code_result), ('Compliance', compliance_result), ('Performance', performance_result)]:
        try:
            parsed = json.loads(result)
            status = parsed.get('status', 'UNKNOWN')
            findings = len(parsed.get('findings', parsed.get('recommendations', [])))
            icon = "PASS" if status in ['PASS', 'OPTIMIZED'] else "WARN"
            if status == 'FAIL':
                all_pass = False
                icon = "FAIL"
            print(f"  [{icon}] {name}: {status} ({findings} findings)")
        except:
            print(f"  [WARN] {name}: Could not parse response")

    if all_pass:
        print("\n  APPROVED - Deploy can proceed")
    else:
        print("\n  NEEDS ATTENTION - Review findings before deploy")
        # Don't block pipeline for now, just warn
        # exit(1)  # Uncomment to block deploys on FAIL

    print("=" * 50)


if __name__ == '__main__':
    main()
