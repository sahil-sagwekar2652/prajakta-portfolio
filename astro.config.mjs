import { defineConfig } from 'astro/config';

// Static output — hostable on Cloudflare Pages (build: `npm run build`, output: `dist`).
export default defineConfig({
  output: 'static',
});
