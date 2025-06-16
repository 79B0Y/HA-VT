import defaultTheme from 'tailwindcss/defaultTheme'

/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./App.vue",
    "./main.ts",
    "./router.ts",
    "./pages/**/*.{vue,ts,js,html}",
    "./utils/**/*.{ts,js}"
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ["Inter", ...defaultTheme.fontFamily.sans]
      }
    },
  },
  plugins: [],
}
