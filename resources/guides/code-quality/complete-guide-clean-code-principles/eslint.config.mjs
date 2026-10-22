// ESLint flat config enforcing the guide's principles mechanically.
// Run: npx eslint before/ after/ --config eslint.config.mjs
export default [
  {
    rules: {
      // small, focused functions
      'max-lines-per-function': ['warn', { max: 40, skipBlankLines: true }],
      'complexity': ['warn', 8],
      'max-depth': ['warn', 3],
      // few parameters
      'max-params': ['warn', 3],
      // no magic numbers in conditions
      'no-magic-numbers': ['warn', { ignore: [0, 1], ignoreArrayIndexes: true }],
      // naming basics
      'camelcase': 'warn',
      // error handling honesty
      'no-throw-literal': 'error',
    },
  },
];
