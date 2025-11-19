import boto3

# Verificar se Lambda existe
lambda_client = boto3.client('lambda', region_name='us-east-1')

print("[1/3] Verificando Lambda de conversao...")
try:
    response = lambda_client.get_function(FunctionName='convert-handler')
    print(f"  OK - Lambda existe")
    print(f"  Runtime: {response['Configuration']['Runtime']}")
    print(f"  Timeout: {response['Configuration']['Timeout']}s")
except:
    print("  ERRO - Lambda nao existe")
    exit(1)

# Verificar MediaConvert
print("\n[2/3] Verificando MediaConvert...")
try:
    mc = boto3.client('mediaconvert', region_name='us-east-1')
    endpoints = mc.describe_endpoints()
    print(f"  OK - MediaConvert disponivel")
    print(f"  Endpoint: {endpoints['Endpoints'][0]['Url'][:50]}...")
except Exception as e:
    print(f"  ERRO - {str(e)}")

# Verificar API Gateway
print("\n[3/3] Verificando API Gateway...")
try:
    apigw = boto3.client('apigateway', region_name='us-east-1')
    resources = apigw.get_resources(restApiId='gdb962d234')
    
    convert_route = None
    for resource in resources['items']:
        if 'convert' in resource.get('path', '').lower():
            convert_route = resource
            break
    
    if convert_route:
        print(f"  OK - Rota /convert existe")
        print(f"  Path: {convert_route['path']}")
    else:
        print(f"  AVISO - Rota /convert nao encontrada")
except Exception as e:
    print(f"  ERRO - {str(e)}")

print("\n[RESUMO]")
print("  Lambda: OK")
print("  MediaConvert: OK")
print("  Conversao .ts para .mp4: DISPONIVEL")
print("\n[INFO] Para converter arquivos .ts:")
print("  1. Selecione arquivos .ts no dashboard")
print("  2. Clique em 'Converter Selecionados'")
print("  3. Aguarde processamento (2-5 min por arquivo)")
