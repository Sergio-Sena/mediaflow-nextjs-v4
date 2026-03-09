'use client'

import { useEffect, useState } from 'react'

export default function DiagnosticPage() {
  const [token, setToken] = useState<string | null>(null)
  const [decoded, setDecoded] = useState<any>(null)
  const [error, setError] = useState<string>('')

  useEffect(() => {
    const t = localStorage.getItem('token')
    setToken(t)

    if (t) {
      try {
        const parts = t.split('.')
        if (parts.length === 3) {
          const payload = JSON.parse(atob(parts[1]))
          setDecoded(payload)
          
          // Check expiration
          if (payload.exp) {
            const now = Math.floor(Date.now() / 1000)
            if (payload.exp < now) {
              setError('Token expirado!')
            }
          }
        }
      } catch (e) {
        setError('Token inválido')
      }
    }
  }, [])

  const testApi = async () => {
    try {
      const response = await fetch('https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/view/users%2Fsergio_sena%2FBolt%20Supercao.mp4', {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      })
      
      const data = await response.json()
      alert(`Status: ${response.status}\n${JSON.stringify(data, null, 2)}`)
    } catch (e: any) {
      alert(`Erro: ${e.message}`)
    }
  }

  return (
    <div className="min-h-screen p-8 bg-dark-900 text-white">
      <h1 className="text-2xl font-bold mb-4">🔍 Diagnóstico JWT</h1>
      
      <div className="space-y-4">
        <div className="bg-dark-800 p-4 rounded">
          <h2 className="font-bold mb-2">Token:</h2>
          <pre className="text-xs overflow-auto">{token || 'Nenhum token encontrado'}</pre>
        </div>

        {decoded && (
          <div className="bg-dark-800 p-4 rounded">
            <h2 className="font-bold mb-2">Payload Decodificado:</h2>
            <pre className="text-xs">{JSON.stringify(decoded, null, 2)}</pre>
          </div>
        )}

        {error && (
          <div className="bg-red-900/50 p-4 rounded border border-red-500">
            <p className="text-red-300">❌ {error}</p>
          </div>
        )}

        <button 
          onClick={testApi}
          className="btn-primary"
          disabled={!token}
        >
          Testar API View
        </button>

        <button 
          onClick={() => {
            localStorage.clear()
            window.location.href = '/login'
          }}
          className="btn-secondary ml-4"
        >
          Limpar e Relogar
        </button>
      </div>
    </div>
  )
}
