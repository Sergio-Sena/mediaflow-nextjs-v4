'use client'

import { Component, ReactNode } from 'react'

interface Props {
  children: ReactNode
  fallback?: ReactNode
}

interface State {
  hasError: boolean
  error?: Error
}

export class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props)
    this.state = { hasError: false }
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error }
  }

  componentDidCatch(error: Error, errorInfo: any) {
    console.error('ErrorBoundary caught:', error, errorInfo)
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback || (
        <div className="flex items-center justify-center min-h-[400px] p-8">
          <div className="text-center">
            <h2 className="text-2xl font-bold text-red-600 mb-4">Algo deu errado</h2>
            <p className="text-gray-600 mb-4">Ocorreu um erro inesperado.</p>
            <button
              onClick={() => this.setState({ hasError: false })}
              className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
            >
              Tentar novamente
            </button>
          </div>
        </div>
      )
    }

    return this.props.children
  }
}
