/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        neon: {
          cyan: '#00ffff',
          purple: '#bf00ff', 
          pink: '#ff0080',
          blue: '#0080ff',
          green: '#00ff80',
          orange: '#ff8000',
          yellow: '#ffff00',
        },
        dark: {
          900: '#0a0a0a',
          800: '#1a1a1a', 
          700: '#2a2a2a',
          600: '#3a3a3a',
          500: '#4a4a4a',
        },
        accent: {
          primary: '#00ffff',
          secondary: '#bf00ff',
          success: '#00ff80',
          warning: '#ffff00',
          error: '#ff0080',
        }
      },
      boxShadow: {
        'neon-cyan': '0 0 20px rgba(0, 255, 255, 0.5), 0 0 40px rgba(0, 255, 255, 0.3)',
        'neon-purple': '0 0 20px rgba(191, 0, 255, 0.5), 0 0 40px rgba(191, 0, 255, 0.3)',
        'neon-pink': '0 0 20px rgba(255, 0, 128, 0.5), 0 0 40px rgba(255, 0, 128, 0.3)',
        'neon-blue': '0 0 20px rgba(0, 128, 255, 0.5), 0 0 40px rgba(0, 128, 255, 0.3)',
      },
      animation: {
        'pulse-neon': 'pulse-neon 3s ease-in-out infinite alternate',
        'glow': 'glow 4s ease-in-out infinite alternate',
        'float': 'float 6s ease-in-out infinite',
        'fade-in': 'fade-in 0.6s ease-out',
        'shimmer': 'shimmer 2s linear infinite',
      },
      keyframes: {
        'pulse-neon': {
          '0%': { 
            boxShadow: '0 0 20px rgba(0, 255, 255, 0.4), 0 0 40px rgba(0, 255, 255, 0.2)',
            transform: 'scale(1)'
          },
          '100%': { 
            boxShadow: '0 0 30px rgba(0, 255, 255, 0.8), 0 0 60px rgba(0, 255, 255, 0.4)',
            transform: 'scale(1.02)'
          }
        },
        'glow': {
          '0%': { 
            textShadow: '0 0 10px rgba(0, 255, 255, 0.6), 0 0 20px rgba(0, 255, 255, 0.4)' 
          },
          '100%': { 
            textShadow: '0 0 20px rgba(0, 255, 255, 0.9), 0 0 30px rgba(0, 255, 255, 0.6)' 
          }
        },
        'float': {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-10px)' }
        },
        'fade-in': {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' }
        },
        'shimmer': {
          '0%': { backgroundPosition: '-200% 0' },
          '100%': { backgroundPosition: '200% 0' }
        }
      }
    },
  },
  plugins: [],
}