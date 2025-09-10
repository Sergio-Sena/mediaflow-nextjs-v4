import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Mediaflow - Sistema de Streaming Modular',
  description: 'Sistema de streaming completo com upload, conversão automática e player híbrido',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="pt-BR">
      <body className="bg-dark-950 text-white antialiased overflow-x-hidden">
        <div className="min-h-screen relative">
          {/* Background gradiente animado */}
          <div className="fixed inset-0 bg-gradient-to-br from-dark-950 via-dark-900 to-dark-850 -z-20"></div>
          <div className="fixed inset-0 bg-gradient-to-tr from-neon-cyan/5 via-transparent to-neon-purple/5 -z-10 animate-pulse-neon"></div>
          
          {/* Elementos decorativos */}
          <div className="fixed top-1/4 left-1/4 w-96 h-96 bg-neon-cyan/3 rounded-full blur-3xl animate-float -z-10"></div>
          <div className="fixed bottom-1/4 right-1/4 w-80 h-80 bg-neon-purple/3 rounded-full blur-3xl animate-float -z-10" style={{animationDelay: '2s'}}></div>
          
          <div className="relative z-10">
            {children}
          </div>
        </div>
      </body>
    </html>
  )
}