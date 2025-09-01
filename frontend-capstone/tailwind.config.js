/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
    "./public/index.html"
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: 'hsl(262, 80%, 60%)',
          dark: 'hsl(262, 80%, 45%)',
          light: 'hsl(262, 80%, 70%)',
        },
        accent: {
          DEFAULT: 'hsl(200, 100%, 60%)',
          neon: 'hsl(280, 100%, 70%)',
        },
        background: {
          DEFAULT: 'hsl(245, 32%, 10%)',
          glass: 'hsla(245, 32%, 10%, 0.7)',
        },
        foreground: {
          DEFAULT: 'hsl(0, 0%, 98%)',
          muted: 'hsl(245, 10%, 60%)',
        },
      },
      fontFamily: {
        sans: ['Segoe UI', 'Roboto', 'Arial', 'sans-serif'],
      },
      boxShadow: {
        glass: '0 8px 32px 0 rgba(31, 38, 135, 0.18)',
        neon: '0 0 8px 2px hsl(280, 100%, 70%)',
      },
      backgroundImage: {
        'hero-gradient': 'linear-gradient(120deg, hsl(262, 80%, 60%) 0%, hsl(200, 100%, 60%) 100%)',
        'glass': 'linear-gradient(120deg, hsla(262, 80%, 60%, 0.7) 0%, hsla(200, 100%, 60%, 0.7) 100%)',
      },
      borderRadius: {
        glass: '1.5rem',
      },
    },
  },
  plugins: [],
}

