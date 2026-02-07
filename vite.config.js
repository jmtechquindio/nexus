import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  base: '/nexus/',
  plugins: [react()],
  build: {
    outDir: 'dist',
    emptyOutDir: true
  },
  publicDir: 'public'
})
