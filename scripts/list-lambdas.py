import boto3

def list_lambdas():
    lambda_client = boto3.client('lambda', region_name='us-east-1')
    
    try:
        response = lambda_client.list_functions()
        
        print("FUNCOES LAMBDA DISPONIVEIS:")
        print("-" * 50)
        
        for func in response['Functions']:
            if 'view' in func['FunctionName'].lower():
                print(f"[VIEW] {func['FunctionName']}")
            else:
                print(f"       {func['FunctionName']}")
                
    except Exception as e:
        print(f"Erro: {str(e)}")

if __name__ == "__main__":
    list_lambdas()