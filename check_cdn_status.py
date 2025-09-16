#!/usr/bin/env python3
import boto3
import requests

def check_cdn_status():
    cloudfront = boto3.client('cloudfront')
    
    # Novo CDN
    new_cdn_id = 'E2ZZ1HR0QLWOAO'
    new_domain = 'd14rytve54170x.cloudfront.net'
    
    print("VERIFICACAO CDN NOVO")
    print("=" * 40)
    
    try:
        # Status do CDN
        response = cloudfront.get_distribution(Id=new_cdn_id)
        status = response['Distribution']['Status']
        
        print(f"ID: {new_cdn_id}")
        print(f"Domain: {new_domain}")
        print(f"Status: {status}")
        
        if status == 'Deployed':
            print("PRONTO para uso!")
            
            # Testar acesso
            print("\nTestando acesso...")
            try:
                test_response = requests.get(f"https://{new_domain}", timeout=10)
                print(f"HTTP Status: {test_response.status_code}")
                
                if test_response.status_code == 200:
                    print("SUCESSO: CDN funcionando!")
                else:
                    print("Aguardando propagacao...")
                    
            except Exception as e:
                print(f"Ainda propagando: {e}")
                
        else:
            print("Ainda em deploy... aguarde mais alguns minutos")
            
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    check_cdn_status()