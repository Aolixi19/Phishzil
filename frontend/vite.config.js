import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';
import { fileURLToPath } from 'url';

// Proper path handling for Windows with spaces
const __dirname = path.dirname(fileURLToPath(import.meta.url));

export default defineConfig({
  plugins: [react()],
  css: {
    postcss: path.resolve(__dirname, 'postcss.config.cjs')
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
      // Add any other aliases you need
    }
  },
  server: {
    port: 5173,
    strictPort: true,
    hmr: {
      overlay: false,
      // Additional HMR config for Windows
      protocol: 'ws',
      host: 'localhost'
    },
    // Windows-specific optimizations
    watch: {
      usePolling: true,
      interval: 100
    }
  },
  // Build optimizations
  build: {
    chunkSizeWarningLimit: 1600,
    rollupOptions: {
      output: {
        manualChunks: {
          react: ['react', 'react-dom'],
          vendor: ['react-router-dom']
        }
      }
    }
  }
});