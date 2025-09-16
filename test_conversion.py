#!/usr/bin/env python3
import requests
import json

def test_conversion():
    api_url = "https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod"
    
    # Testar conversão do arquivo que falhou
    test_file = "ShyBlanche/Tente_N_o_Gozar_DESAFIO._Se_....ts"
    
    print("TESTE DE CONVERSAO")
    print("=" * 40)
    print(f"Arquivo: {test_file}")
    
    try:
        response = requests.post(
            f"{api_url}/convert",
            json={"key": test_file},
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("SUCESSO: Conversao iniciada!")
                print(f"Job ID: {data.get('jobId')}")
            else:
                print(f"ERRO: {data.get('message')}")
        else:
            print("ERRO: Falha na requisicao")
            
    except Exception as e:
        print(f"ERRO: {e}")

if __name__ == "__main__":
    test_conversion()