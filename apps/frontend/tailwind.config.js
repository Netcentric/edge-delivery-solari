const colors = require('tailwindcss/colors')

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{html,js,jsx,ts,tsx}"],
  theme: {
    extend: {},
    colors: {
      black: colors.black,
      white: colors.white,
      "robin-egg-blue": "#12C9CC",
      "fluorescent-blue": "#26EFE9",
      "waterspout": "#A8F9F6",
      "midnight-blue": "#000048",
    }
  },
  plugins: [],
}

