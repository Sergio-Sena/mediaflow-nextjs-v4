# -*- coding: utf-8 -*-
"""
Script de teste para Lambda multipart-handler
Valida se os uploads estao indo para users/{username}/ corretamente
"""

import boto3
import json

def test_multipart_lambda():
    """Testa a Lambda multipart-handler"""
    
    lambda_client = boto3.client('lambda', region_name='us-east-1')
    
    # Simular evento de inicializacao de upload
    test_event = {
        'httpMethod': 'POST',
        'path': '/multipart/init',
        'headers': {
            'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InVzZXJfYWRtaW4iLCJpYXQiOjE3MDAwMDAwMDB9.test'
        },
        'body': json.dumps({
            'filename': 'test-folder/test-video.mp4',
            'fileSize': 150000000
        })
    }
    
    print("Testando Lambda multipart-handler...")
    print(f"Filename: test-folder/test-video.mp4")
    print(f"Username esperado: user_admin")
    print(f"Key esperada: users/user_admin/test-folder/test-video.mp4")
    print()
    
    try:
        response = lambda_client.invoke(
            FunctionName='mediaflow-multipart-handler',
            InvocationType='RequestResponse',
            Payload=json.dumps(test_event)
        )
        
        payload = json.loads(response['Payload'].read())
        print(f"Status Code: {payload['statusCode']}")
        
        if payload['statusCode'] == 200:
            body = json.loads(payload['body'])
            key = body.get('key', '')
            
            print(f"Key retornada: {key}")
            
            if key.corporativotswith('users/user_admin/'):
                print("\n[OK] Lambda corrigida! Upload vai para users/user_admin/")
                return True
            else:
                print(f"\n[ERRO] Key incorreta: {key}")
                return False
        else:
            print(f"\n[ERRO] Status code: {payload['statusCode']}")
            print(f"Body: {payload.get('body', '')}")
            return False
            
    except Exception as e:
        print(f"\n[ERRO] Excecao: {e}")
        return False

if __name__ == '__main__':
    success = test_multipart_lambda()
    exit(0 if success else 1)
