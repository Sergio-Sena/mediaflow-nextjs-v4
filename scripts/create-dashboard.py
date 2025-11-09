import boto3
import json

cloudwatch = boto3.client('cloudwatch', region_name='us-east-1')

LAMBDAS = [
    'auth-handler', 'upload-handler', 'files-handler',
    'convert-handler', 'multipart-handler', 'folder-operations',
    'create-user', 'approve-user', 'cleanup-handler'
]

def create_dashboard():
    """Create CloudWatch Dashboard for Mídiaflow"""
    
    widgets = []
    
    # Errors widget
    widgets.append({
        "type": "metric",
        "properties": {
            "metrics": [[{"expression": f"SUM(METRICS())", "label": "Total Errors", "id": "e1"}]] + 
                       [[f"AWS/Lambda", "Errors", {"stat": "Sum", "id": f"m{i}"}] for i in range(len(LAMBDAS))],
            "view": "timeSeries",
            "region": "us-east-1",
            "title": "Lambda Errors",
            "period": 300
        }
    })
    
    # Invocations widget
    widgets.append({
        "type": "metric",
        "properties": {
            "metrics": [[f"AWS/Lambda", "Invocations", {"stat": "Sum"}] for _ in LAMBDAS],
            "view": "timeSeries",
            "region": "us-east-1",
            "title": "Lambda Invocations",
            "period": 300
        }
    })
    
    # Duration widget
    widgets.append({
        "type": "metric",
        "properties": {
            "metrics": [[f"AWS/Lambda", "Duration", {"stat": "Average"}] for _ in LAMBDAS],
            "view": "timeSeries",
            "region": "us-east-1",
            "title": "Lambda Duration (ms)",
            "period": 300
        }
    })
    
    dashboard_body = {
        "widgets": widgets
    }
    
    try:
        cloudwatch.put_dashboard(
            DashboardName='Midiaflow-Monitoring',
            DashboardBody=json.dumps(dashboard_body)
        )
        print("OK - Dashboard created: Midiaflow-Monitoring")
        print("https://console.aws.amazon.com/cloudwatch/home?region=us-east-1#dashboards:name=Midiaflow-Monitoring")
    except Exception as e:
        print(f"ERROR - Dashboard creation failed: {e}")

if __name__ == '__main__':
    print("Creating CloudWatch Dashboard\n")
    create_dashboard()
