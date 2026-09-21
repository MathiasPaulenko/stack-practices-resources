// babel.config.js — transpilation targets matching the support matrix
module.exports = {
  presets: [
    ['@babel/preset-env', {
      targets: {
        chrome: '110',
        edge: '110',
        firefox: '115',
        safari: '16',
        samsung: '20',
      },
      useBuiltIns: 'usage',
      corejs: 3,
    }],
  ],
};
