#!/usr/bin/env python3
import boto3
import json

def configure_cleanup_eventbridge():
    """Configure EventBridge rule for MediaConvert job completion"""
    
    events_client = boto3.client('events')
    lambda_client = boto3.client('lambda')
    
    # Load config
    with open('mediaflow-config.json', 'r') as f:
        config = json.load(f)
    
    cleanup_function = 'mediaflow-cleanup-handler'
    rule_name = 'mediaflow-conversion-complete'
    
    print(f"Configuring EventBridge cleanup for: {cleanup_function}")
    
    # 1. Create EventBridge rule for MediaConvert job completion
    try:
        events_client.put_rule(
            Name=rule_name,
            EventPattern=json.dumps({
                "source": ["aws.mediaconvert"],
                "detail-type": ["MediaConvert Job State Change"],
                "detail": {
                    "status": ["COMPLETE"]
                }
            }),
            State='ENABLED',
            Description='Trigger cleanup when MediaConvert job completes'
        )
        print("[OK] EventBridge rule created")
    except Exception as e:
        print(f"[ERROR] EventBridge rule: {str(e)}")
        return False
    
    # 2. Add Lambda permission for EventBridge
    try:
        lambda_client.add_permission(
            FunctionName=cleanup_function,
            StatementId='eventbridge-cleanup-trigger',
            Action='lambda:InvokeFunction',
            Principal='events.amazonaws.com',
            SourceArn=f'arn:aws:events:us-east-1:{config["account_id"]}:rule/{rule_name}'
        )
        print("[OK] Lambda permission added")
    except lambda_client.exceptions.ResourceConflictException:
        print("[OK] Lambda permission already exists")
    except Exception as e:
        print(f"[ERROR] Lambda permission: {str(e)}")
        return False
    
    # 3. Add target to EventBridge rule
    try:
        events_client.put_targets(
            Rule=rule_name,
            Targets=[
                {
                    'Id': '1',
                    'Arn': f'arn:aws:lambda:us-east-1:{config["account_id"]}:function:{cleanup_function}'
                }
            ]
        )
        print("[OK] EventBridge target configured")
    except Exception as e:
        print(f"[ERROR] EventBridge target: {str(e)}")
        return False
    
    return True

if __name__ == "__main__":
    success = configure_cleanup_eventbridge()
    if success:
        print("\n[SUCCESS] Cleanup EventBridge configured!")
        print("[INFO] MediaConvert jobs will now trigger automatic cleanup")
    else:
        print("\n[FAILED] Configuration failed!")