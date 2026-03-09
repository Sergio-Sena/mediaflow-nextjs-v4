'use client'

import { useState } from 'react'

export default function DiagnosticPage() {
  const [results, setResults] = useState<any[]>([])
  const [token, setToken] = useState('')

  const addResult = (name: string, data: any) => {
    setResults(prev => [...prev, { name, data, time: new Date().toLocaleTimeString() }])
  }

  const testEndpoint = async (name: string, url: string, options: RequestInit = {}) => {
    try {
      const start = performance.now()
      const response = await fetch(url, options)
      const elapsed = performance.now() - start
      const data = await response.json()
      
      addResult(name, {
        status: response.status,
        time: `${elapsed.toFixed(0)}ms`,
        data
      })
    } catch (error) {
      addResult(name, { error: error instanceof Error ? error.message : 'Unknown error' })
    }
  }

  const runTests = async () => {
    setResults([])
    const storedToken = localStorage.getItem('token')
    setToken(storedToken || '')

    if (storedToken) {
      await testEndpoint('1. Files (Bearer)', 'https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/files', {
        headers: { 'Authorization': `Bearer ${storedToken}` }
      })

      await testEndpoint('2. Users (Bearer)', 'https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/users', {
        headers: { 'Authorization': `Bearer ${storedToken}` }
      })
    }
  }

  return (
    <div className="min-h-screen bg-gray-900 text-white p-8">
      <h1 className="text-3xl font-bold mb-4">API Diagnostic</h1>
      
      <button 
        onClick={runTests}
        className="bg-cyan-500 hover:bg-cyan-600 px-6 py-2 rounded mb-4"
      >
        Run Tests
      </button>

      {token && (
        <div className="mb-4 p-4 bg-gray-800 rounded">
          <p className="text-sm">Token: {token.substring(0, 50)}...</p>
        </div>
      )}

      <div className="space-y-4">
        {results.map((result, i) => (
          <div key={i} className="bg-gray-800 p-4 rounded">
            <div className="flex justify-between mb-2">
              <span className="font-bold">{result.name}</span>
              <span className="text-sm">{result.time}</span>
            </div>
            <pre className="text-xs overflow-auto bg-gray-900 p-2 rounded">
              {JSON.stringify(result.data, null, 2)}
            </pre>
          </div>
        ))}
      </div>
    </div>
  )
}
