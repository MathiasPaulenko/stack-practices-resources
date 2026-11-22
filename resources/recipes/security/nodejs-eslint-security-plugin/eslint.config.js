import security from 'eslint-plugin-security';

export default [
  {
    plugins: { security },
    rules: {
      'security/detect-object-injection': 'off',
      'security/detect-non-literal-regexp': 'error',
      'security/detect-non-literal-fs-filename': 'warn',
      'security/detect-unsafe-regex': 'error',
      'security/detect-child-process': 'warn',
      'security/detect-buffer-noassert': 'error',
      'security/detect-pseudoRandomBytes': 'error',
      'security/detect-new-buffer': 'error',
      'security/detect-eval-with-expression': 'error',
      'security/detect-no-callsites': 'off',
    },
  },
  {
    // Relaxed rules for test code
    files: ['test/**/*.js'],
    rules: {
      'security/detect-child-process': 'off',
      'security/detect-non-literal-fs-filename': 'off',
    },
  },
];
