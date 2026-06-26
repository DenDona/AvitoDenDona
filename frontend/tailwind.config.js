/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        avito: {
          blue: '#0468FF',
          orange: '#FF7800',
          bg: '#f4f4f5',
          card: '#ffffff',
          border: '#e0e0e0',
          text: '#1a1a1a',
          muted: '#757575',
        },
      },
    },
  },
  plugins: [],
}