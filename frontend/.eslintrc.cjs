/* eslint-env node */
require('@rushstack/eslint-patch/modern-module-resolution')

module.exports = {
  root: true,
  env: {
    browser: true,
    node: true,
    es2021: true
  },
  parser: 'vue-eslint-parser',
  parserOptions: {
    parser: '@typescript-eslint/parser',
    ecmaVersion: 'latest',
    sourceType: 'module',
    ecmaFeatures: {
      jsx: true
    }
  },
  extends: [
    'eslint:recommended',
    'plugin:vue/vue3-recommended',
    'plugin:@typescript-eslint/recommended',
    '@vue/eslint-config-typescript',
    '@vue/eslint-config-prettier'
  ],
  plugins: ['vue', '@typescript-eslint'],
  rules: {
    // Правила на твой вкус:
    'vue/multi-word-component-names': 'off',
    '@typescript-eslint/no-unused-vars': ['warn'],
    'no-unused-vars': 'off',
    'no-console': 'warn',
    'no-debugger': 'warn'
  }
}
