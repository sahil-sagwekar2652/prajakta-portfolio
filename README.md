# Prajakta Patil — personal website

Personal site of Prajakta Patil — athlete, trekker, poet, traveller, tour guide, writer,
and founder of Muhurta Yatra. Built with Astro, fully static, deployable to Cloudflare Pages.

## Run locally

Requires Node.js 18 or newer.

```sh
cd prajakta-personal-website
npm install        # first time only
npm run dev        # dev server at http://localhost:4321
```

Other commands:

```sh
npm run build      # static build -> dist/
npm run preview    # serve the production build at http://localhost:4321
```

## Deploy (Cloudflare Pages)

- Framework preset: **Astro** (or "None" — output is plain static files)
- Build command: `npm run build`
- Build output directory: `dist`

## Structure

- `src/pages/index.astro` — homepage (identity hero, blog cards, photo strip, venture teaser)
- `src/components/` — Nav, Hero, Stories, Gallery, Venture, Footer, Parijat (flower SVG), Arrow
- `src/data/posts.ts` — the 5 blog posts (cards link to the originals on Blogspot)
- `src/data/photos.ts` — gallery photographs
- `src/styles/global.css` — tokens, fonts, base styles
- `public/fonts/` — self-hosted Yatra One + Mukta (woff2)
- `public/images/` — her own photographs and blog images (optimized copies)

## Content & image provenance

- Blog text and images: scraped from her own blog, `yatrawithprajakta.blogspot.com`
  (raw scrape in `blog_scrape/`); cards link out to the original posts.
- Photographs in `public/images/`: the author's own photos (source archive in `photos/`).
- `public/images/muhurta-yatra.jpg`: the Muhurta Yatra venture logo.
- Parijat flower SVGs and favicon: authored in-repo as crisp vector geometry.
