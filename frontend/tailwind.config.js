/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        'onyx': {
          50: '#F5F5F5',
          100: '#EAEAEA',
          200: '#D9D9D9',
          300: '#B8B8B8',
          400: '#A0A0A0',
          500: '#666666',
          600: '#2A2A2A',
          700: '#1A1A1A',
          800: '#121212',
          900: '#0A0A0A',
          950: '#050505',
        },
        'emerald': {
          50: '#F0FFF5',
          100: '#E0FFE0',
          200: '#C0FFD0',
          300: '#80FFB0',
          400: '#40FF90',
          500: '#00FFAA',
          600: '#00E699',
          700: '#00B377',
          800: '#008055',
          900: '#004D33',
        },
        'amber': {
          50: '#FFF8E1',
          100: '#FFEDB3',
          200: '#FFDC70',
          300: '#FFCC66',
          400: '#FFB74D',
          500: '#FFAA00',
          600: '#FF9800',
          700: '#F57C00',
          800: '#EF6C00',
          900: '#E65100',
        },
        'rose': {
          50: '#FFF1F2',
          100: '#FFE4E6',
          200: '#FECDD3',
          300: '#FDA4AF',
          400: '#FB7185',
          500: '#F43F5E',
          600: '#E11D48',
          700: '#BE123C',
          800: '#9E1B4B',
          900: '#881337',
        }
      },
      boxShadow: {
        'black-touch': '0 4px 20px rgba(0, 0, 0, 0.3), 0 1px 3px rgba(0, 0, 0, 0.2)',
        'black-hover': '0 6px 30px rgba(0, 0, 0, 0.4), 0 2px 6px rgba(0, 0, 0, 0.3)',
        'emerald-glow': '0 0 15px rgba(0, 255, 170, 0.3)',
      },
      backdropBlur: {
        'xs': '2px',
      },
      gradientColorStops: {
        'emerald-start': '#00FFAA',
        'emerald-end': '#00E699',
        'amber-start': '#FFCC66',
        'amber-end': '#FFBB44',
      }
    },
  },
  plugins: [],
};
