/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        eden: {
          50: '#f4f7f4',
          100: '#e5ebe5',
          200: '#ced9ce',
          300: '#a9bfa9',
          400: '#7e9f7e',
          500: '#5b815b',
          600: '#486848', // Color principal similar al logo
          700: '#3a533a',
          800: '#304330',
          900: '#283728',
          950: '#151e15',
        }
      }
    },
  },
  plugins: [],
}
