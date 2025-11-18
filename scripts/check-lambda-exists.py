import boto3

lambda_client = boto3.client('lambda', region_name='us-east-1')

try:
    response = lambda_client.get_function(FunctionName='view-handler')
    print(f"[OK] Lambda existe: {response['Configuration']['FunctionName']}")
    print(f"[INFO] Runtime: {response['Configuration']['Runtime']}")
    print(f"[INFO] Handler: {response['Configuration']['Handler']}")
    print(f"[INFO] Last Modified: {response['Configuration']['LastModified']}")
except lambda_client.exceptions.ResourceNotFoundException:
    print("[ERRO] Lambda 'view-handler' nao existe!")
    print("\n[INFO] Listando Lambdas disponiveis:")
    
    lambdas = lambda_client.list_functions()
    for func in lambdas['Functions']:
        if 'view' in func['FunctionName'].lower():
            print(f"  - {func['FunctionName']}")
