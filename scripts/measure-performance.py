#!/usr/bin/env python3
import requests
import time
import statistics

def measure_endpoint(url, name, headers=None):
    times = []
    print(f"\n[{name}]")
    
    for i in range(3):
        try:
            start = time.time()
            response = requests.get(url, headers=headers, timeout=30)
            elapsed = (time.time() - start) * 1000
            times.append(elapsed)
            
            print(f"  Tentativa {i+1}: {elapsed:.0f}ms - Status: {response.status_code} - Size: {len(response.content)/1024:.1f}KB")
            time.sleep(1)
        except Exception as e:
            print(f"  Tentativa {i+1}: ERRO - {e}")
    
    if times:
        print(f"  Media: {statistics.mean(times):.0f}ms | Min: {min(times):.0f}ms | Max: {max(times):.0f}ms")
    return times

print("=" * 60)
print("ANALISE DE PERFORMANCE - MIDIAFLOW")
print("=" * 60)

# 1. CloudFront (HTML estático)
measure_endpoint(
    "https://midiaflow.sstechnologies-cloud.com",
    "CloudFront - Pagina Inicial"
)

# 2. CloudFront (assets)
measure_endpoint(
    "https://midiaflow.sstechnologies-cloud.com/_next/static/css/app/layout.css",
    "CloudFront - CSS"
)

# 3. API Gateway
measure_endpoint(
    "https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/health",
    "API Gateway - Health Check"
)

# 4. API Gateway - List Users (cold start)
print("\n[API Gateway - List Users (pode ter cold start)]")
try:
    start = time.time()
    response = requests.get(
        "https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/users/list",
        timeout=30
    )
    elapsed = (time.time() - start) * 1000
    print(f"  Tempo: {elapsed:.0f}ms - Status: {response.status_code}")
except Exception as e:
    print(f"  ERRO: {e}")

print("\n" + "=" * 60)
print("DIAGNOSTICO:")
print("=" * 60)
print("- CloudFront < 200ms: Excelente")
print("- CloudFront 200-500ms: Bom (cache miss)")
print("- CloudFront > 500ms: Lento (verificar origem)")
print("- API Gateway < 1000ms: Normal")
print("- API Gateway > 3000ms: Cold start Lambda")
print("=" * 60)
