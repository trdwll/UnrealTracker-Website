module.exports = {
  purge: [],
  darkMode: 'class', // or 'media' or 'class'
  theme: {
    extend: {
      minWidth: {
        '2': '2rem',
      },
      maxWidth: {
        '2': '2rem',
      },
    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
  purge: {
    enabled: true, //true for production build
    preserveHtmlElements: false,
    content: [
      '../templates/**/*.html',
    ],
    options: {
      safelist: [],
      keyframes: true,
      fontFace: true,
    }
  },
}