const colors = require('tailwindcss/colors');

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./src/**/*.{html,js,jsx,ts,tsx}'],
  theme: {
    extend: {
      spacing: {
        '5px': '5px',
        '15px': '15px',
        '9px': '9px',
        '25px': '25px',
        '31.25px': '31.25px',
        '18.75px': '18.75px',
      },
      lineHeight: {
        '25px': '25px',
      },
      fontSize: {
        '25px': '25px',
      },
    },
    colors: {
      black: colors.black,
      white: colors.white,
      'robin-egg-blue': '#12C9CC',
      'fluorescent-blue': '#26EFE9',
      waterspout: '#A8F9F6',
      'midnight-blue': '#000048',
      'dark-teal': '#11C7CC',
      'medium-teal': '#29EEE9',
      'light-teal': '#A8F9F6',
      'lightest-teal': '#C9FBFA',
      'disabled-teal': '#26EFE9',
      'link-blue': '#2F78C4',
    },
    fontFamily: {
      gellix: ['Gellix', 'sans-serif'],
    },
  },
  plugins: [],
};
