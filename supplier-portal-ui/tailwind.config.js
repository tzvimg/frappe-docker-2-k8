/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
    "./node_modules/frappe-ui/src/**/*.{vue,js,ts}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Rubik', 'sans-serif'],
      },
    },
  },
  plugins: [
    require('tailwindcss-rtl'),
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
  ],
}
