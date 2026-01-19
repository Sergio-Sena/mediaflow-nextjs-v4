import time
import requests
import statistics
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

def test_performance(url, name, runs=5):
    """Testa performance de carregamento"""
    print(f"\nTestando {name}...")
    print(f"URL: {url}")
    print("-" * 60)
    
    times = []
    sizes = []
    
    for i in range(runs):
        try:
            start = time.time()
            response = requests.get(url, timeout=10, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            end = time.time()
            
            load_time = (end - start) * 1000  # em ms
            size = len(response.content) / 1024  # em KB
            
            times.append(load_time)
            sizes.append(size)
            
            print(f"  Run {i+1}: {load_time:.0f}ms | {size:.1f}KB | Status: {response.status_code}")
            time.sleep(1)  # Pausa entre requests
            
        except Exception as e:
            print(f"  Run {i+1}: ERRO - {e}")
    
    if times:
        return {
            'name': name,
            'url': url,
            'avg_time': statistics.mean(times),
            'min_time': min(times),
            'max_time': max(times),
            'median_time': statistics.median(times),
            'avg_size': statistics.mean(sizes),
            'total_runs': len(times)
        }
    return None

def test_cdn_resources():
    """Testa recursos do CDN"""
    print("\n" + "=" * 60)
    print("TESTE DE RECURSOS CDN")
    print("=" * 60)
    
    resources = {
        'CloudFront (Midiaflow)': 'https://d3v8quh3b2nner.cloudfront.net/',
        'Vimeo CDN': 'https://i.vimeocdn.com/video/placeholder.jpg',
        'Netflix CDN': 'https://assets.nflxext.com/ffe/siteui/vlv3/placeholder.jpg'
    }
    
    results = []
    for name, url in resources.items():
        result = test_performance(url, name, runs=3)
        if result:
            results.append(result)
    
    return results

def test_page_load():
    """Testa carregamento de páginas"""
    print("\n" + "=" * 60)
    print("TESTE DE CARREGAMENTO DE PAGINAS")
    print("=" * 60)
    
    pages = {
        'Midiaflow - Home': 'https://midiaflow.sstechnologies-cloud.com',
        'Midiaflow - Login': 'https://midiaflow.sstechnologies-cloud.com/login',
        'Midiaflow - Dashboard': 'https://midiaflow.sstechnologies-cloud.com/dashboard',
    }
    
    results = []
    for name, url in pages.items():
        result = test_performance(url, name, runs=5)
        if result:
            results.append(result)
    
    return results

def print_comparison(results):
    """Imprime comparação de resultados"""
    if not results:
        return
    
    print("\n" + "=" * 60)
    print("RESUMO COMPARATIVO")
    print("=" * 60)
    
    # Ordena por tempo médio
    results.sort(key=lambda x: x['avg_time'])
    
    print(f"\n{'Plataforma':<30} {'Tempo Medio':<15} {'Min':<10} {'Max':<10} {'Tamanho'}")
    print("-" * 80)
    
    for r in results:
        print(f"{r['name']:<30} {r['avg_time']:>10.0f}ms   {r['min_time']:>6.0f}ms  {r['max_time']:>6.0f}ms  {r['avg_size']:>6.1f}KB")
    
    # Análise
    print("\n" + "=" * 60)
    print("ANALISE")
    print("=" * 60)
    
    fastest = results[0]
    print(f"\nMais rapido: {fastest['name']} ({fastest['avg_time']:.0f}ms)")
    
    midiaflow = [r for r in results if 'Midiaflow' in r['name']]
    if midiaflow:
        avg_midiaflow = statistics.mean([r['avg_time'] for r in midiaflow])
        print(f"\nMedia Midiaflow: {avg_midiaflow:.0f}ms")
        
        # Classificação
        if avg_midiaflow < 500:
            rating = "EXCELENTE"
            emoji = "🚀"
        elif avg_midiaflow < 1000:
            rating = "BOM"
            emoji = "✅"
        elif avg_midiaflow < 2000:
            rating = "ACEITAVEL"
            emoji = "⚠️"
        else:
            rating = "PRECISA MELHORAR"
            emoji = "❌"
        
        print(f"\nClassificacao: {emoji} {rating}")
        
        # Recomendações
        print("\n" + "=" * 60)
        print("RECOMENDACOES")
        print("=" * 60)
        
        if avg_midiaflow < 500:
            print("\n✅ Performance excelente!")
            print("  - Carregamento rapido competitivo")
            print("  - CDN funcionando otimamente")
        elif avg_midiaflow < 1000:
            print("\n✅ Boa performance!")
            print("  - Considere:")
            print("    * Minificar assets adicionais")
            print("    * Lazy loading de componentes")
            print("    * Comprimir imagens")
        else:
            print("\n⚠️ Performance pode melhorar:")
            print("  - Otimizar bundle JavaScript")
            print("  - Implementar code splitting")
            print("  - Revisar cache headers")
            print("  - Comprimir assets com Brotli/Gzip")

def main():
    print("=" * 60)
    print("TESTE DE PERFORMANCE - MIDIAFLOW")
    print("Comparacao com concorrentes")
    print("=" * 60)
    
    # Teste 1: Páginas
    page_results = test_page_load()
    
    # Teste 2: CDN
    cdn_results = test_cdn_resources()
    
    # Comparação final
    all_results = page_results + cdn_results
    print_comparison(all_results)
    
    print("\n" + "=" * 60)
    print("TESTE CONCLUIDO")
    print("=" * 60)

if __name__ == "__main__":
    main()
