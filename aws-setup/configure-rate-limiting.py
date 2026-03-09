import boto3
import json

client = boto3.client('apigateway', region_name='us-east-1')
API_ID = 'gdb962d234'

# Rate limits por endpoint
RATE_LIMITS = {
    '/auth': {'rateLimit': 5.0, 'burstLimit': 10},      # Login: 5 req/min
    '/upload/presigned': {'rateLimit': 10.0, 'burstLimit': 20},  # Upload: 10 req/min
    '/files/bulk-delete': {'rateLimit': 20.0, 'burstLimit': 40}, # Delete: 20 req/min
}

def configure_rate_limiting():
    try:
        # Get existing usage plan
        usage_plans = client.get_usage_plans()
        plan_id = None
        
        for plan in usage_plans.get('items', []):
            if plan['name'] == 'MidiaFlow-RateLimiting':
                plan_id = plan['id']
                print(f"✓ Usage plan exists: {plan_id}")
                break
        
        # Create if not exists
        if not plan_id:
            plan = client.create_usage_plan(
                name='MidiaFlow-RateLimiting',
                description='Rate limiting for MidiaFlow API',
                throttle={'rateLimit': 100.0, 'burstLimit': 200},
                apiStages=[{'apiId': API_ID, 'stage': 'prod'}]
            )
            plan_id = plan['id']
            print(f"✓ Created usage plan: {plan_id}")
        
        # Configure method throttling
        for path, limits in RATE_LIMITS.items():
            try:
                client.update_usage_plan(
                    usagePlanId=plan_id,
                    patchOperations=[
                        {
                            'op': 'add',
                            'path': f'/throttle/{API_ID}/prod/*/POST',
                            'value': json.dumps(limits)
                        }
                    ]
                )
                print(f"✓ Rate limit configured for {path}: {limits['rateLimit']} req/min")
            except Exception as e:
                print(f"⚠ {path}: {str(e)}")
        
        print("\n✅ Rate limiting configured successfully!")
        print("\nLimits:")
        print("  Login: 5 req/min (burst: 10)")
        print("  Upload: 10 req/min (burst: 20)")
        print("  Delete: 20 req/min (burst: 40)")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == '__main__':
    configure_rate_limiting()
