import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  // GitHub Pages usually serves from a subpath (the repo name)
  base: process.env.BASE_URL || '/',
})
