/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        zara: {
          dark: '#121212',
          light: '#f5f5f5',
          gold: '#d4af37'
        }
      },
      fontFamily: {
        serif: ['Times New Roman', 'serif'], // Zara style
        sans: ['Inter', 'sans-serif'],
      }
    },
  },
  plugins: [],
}
