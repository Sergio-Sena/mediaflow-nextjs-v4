# -*- coding: utf-8 -*-
import subprocess
import sys
import os
from datetime import datetime, timedelta

sys.stdout.reconfigure(encoding='utf-8')

print('=' * 60)
print('DIAGNÓSTICO DE REINICIALIZAÇÕES / BSOD')
print('=' * 60)

def run(cmd):
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, shell=True, encoding='utf-8', errors='ignore')
        return result.stdout.strip()
    except:
        return ''

# 1. Último BSOD no Event Log
print('\n=== ÚLTIMOS CRASHES (Event Log) ===')
cmd = '''powershell -command "Get-WinEvent -FilterHashtable @{LogName='System'; Id=41,1001,6008} -MaxEvents 10 | Select-Object TimeCreated, Id, Message | Format-List"'''
out = run(cmd)
print(out if out else '  Nenhum evento encontrado.')

# 2. Minidumps
print('\n=== MINIDUMP FILES ===')
dump_path = r'C:\Windows\Minidump'
if os.path.exists(dump_path):
    files = sorted(os.listdir(dump_path), reverse=True)
    if files:
        for f in files[:5]:
            fp = os.path.join(dump_path, f)
            mtime = datetime.fromtimestamp(os.path.getmtime(fp))
            size = os.path.getsize(fp) / 1024
            print(f'  {f} — {mtime.strftime("%d/%m/%Y %H:%M")} — {size:.0f} KB')
    else:
        print('  Pasta vazia.')
else:
    print('  Pasta Minidump não encontrada.')

# 3. Último shutdown inesperado
print('\n=== SHUTDOWNS INESPERADOS ===')
cmd = '''powershell -command "Get-WinEvent -FilterHashtable @{LogName='System'; Id=6008} -MaxEvents 5 | Select-Object TimeCreated, Message | Format-List"'''
out = run(cmd)
print(out if out else '  Nenhum shutdown inesperado recente.')

# 4. Temperatura e hardware (via WMIC)
print('\n=== USO DE MEMÓRIA ATUAL ===')
cmd = 'wmic OS get FreePhysicalMemory,TotalVisibleMemorySize /Value'
out = run(cmd)
lines = [l for l in out.splitlines() if '=' in l]
for l in lines:
    key, val = l.split('=')
    mb = int(val.strip()) // 1024
    print(f'  {key.strip()}: {mb} MB')

# 5. Processos com alto uso de memória
print('\n=== TOP 10 PROCESSOS POR MEMÓRIA ===')
cmd = '''powershell -command "Get-Process | Sort-Object WorkingSet64 -Descending | Select-Object -First 10 Name, @{N='MB';E={[math]::Round($_.WorkingSet64/1MB,1)}} | Format-Table -AutoSize"'''
out = run(cmd)
print(out if out else '  Não foi possível obter.')

# 6. Erros críticos nas últimas 24h
print('\n=== ERROS CRÍTICOS (últimas 24h) ===')
cmd = '''powershell -command "Get-WinEvent -FilterHashtable @{LogName='System'; Level=1,2; StartTime=(Get-Date).AddHours(-24)} -MaxEvents 10 -ErrorAction SilentlyContinue | Select-Object TimeCreated, LevelDisplayName, Message | Format-List"'''
out = run(cmd)
print(out if out else '  Nenhum erro crítico nas últimas 24h.')

# 7. Verificar integridade do sistema
print('\n=== VERIFICAÇÃO DE INTEGRIDADE (SFC - último resultado) ===')
cmd = '''powershell -command "Get-WinEvent -FilterHashtable @{LogName='Application'; ProviderName='Microsoft-Windows-WER-SystemErrorReporting'} -MaxEvents 3 -ErrorAction SilentlyContinue | Format-List"'''
out = run(cmd)
print(out if out else '  Sem registros WER recentes.')

print('\n' + '=' * 60)
print('Para análise detalhada do minidump, rode:')
print('  windbg -z C:\\Windows\\Minidump\\<arquivo>.dmp')
print('=' * 60)
