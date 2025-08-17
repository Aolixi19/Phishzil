import js from '@eslint/js'
import globals from 'globals'
import reactHooks from 'eslint-plugin-react-hooks'
import reactRefresh from 'eslint-plugin-react-refresh'
import { defineConfig, globalIgnores } from 'eslint/config'

export default defineConfig([
  globalIgnores(['dist']),
  {
    // React-specific config
    files: ['**/*.{js,jsx}'],
    extends: [
      js.configs.recommended,
      reactHooks.configs['recommended-latest'],
      reactRefresh.configs.vite,
    ],
    languageOptions: {
      ecmaVersion: 2020,
      globals: globals.browser,
      parserOptions: {
        ecmaVersion: 'latest',
        ecmaFeatures: { jsx: true },
        sourceType: 'module',
      },
    },
    rules: {
      'no-unused-vars': ['error', { varsIgnorePattern: '^[A-Z_]' }],
    },
  },
  {
    // Node.js config files
    files: [
      'postcss.config.js',
      'tailwind.config.js',
      'vite.config.js',
      'eslint.config.js'
    ],
    languageOptions: {
      globals: {
        ...globals.node
      },
      parserOptions: {
        sourceType: 'script' // Use CommonJS for config files
      }
    },
    rules: {
      'no-undef': 'off' // Disable since we're using Node globals
    }
  }
])