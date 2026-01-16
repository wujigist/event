import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { copyFileSync, existsSync, mkdirSync } from 'fs'
import { resolve } from 'path'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    react(),
    {
      name: 'copy-redirects',
      closeBundle() {
        const redirectsPath = resolve(__dirname, 'public/_redirects')
        const distPath = resolve(__dirname, 'dist/_redirects')
        
        if (existsSync(redirectsPath)) {
          copyFileSync(redirectsPath, distPath)
          console.log('✅ Copied _redirects to dist/')
        }
      }
    }
  ],
})