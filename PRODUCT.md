# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

Astro, structured to be hostable on Cloudflare Pages (static output). Confirmed by the user on a greenfield project.

## Users

Primary: visitors getting to know Prajakta Patil as a person — readers of her travel/trek stories, her Instagram audience (@_.praju._._, 751 followers), and viewers of her photos. Secondary (later): people interested in her work as a founder.

## Product Purpose

Prajakta Patil's personal website. The personal part leads: her blogs, her photos, and her social links. A section about her as a founder comes later in the site, secondary to the personal focus. Success means a visitor leaves knowing who she is and can read her stories, browse her photos, and reach her socials.

## Positioning

An individual's personal home on the web. Prajakta Patil, in her own words: athlete, trekker, poet, traveller, tour guide, blog writer — and founder of Muhurta Yatra (Tours & Treks). Not a commercial travel service and not a pure professional portfolio: the personal identity carries the site; the founder identity is a section within it, not the frame.

## Operating Context

Existing public blog *YatraWithPrajakta* on Blogspot (https://yatrawithprajakta.blogspot.com) with 5 published posts, fully scraped into `blog_scrape/` (verbatim text + downloaded images). Personal photo collection in `photos/`. Social presence: Instagram @_.praju._._ (personal), Instagram @muhurtayatra (her venture, "Muhurta Yatra Tours & Treks"), LinkedIn /in/prajakta-patil-1b3368296/. Deploy target is Cloudflare Pages.

## Capabilities and Constraints

- Must present the 5 existing blog posts (Kalsubai trek guide, Gorakhgad trek guide, Nakhind trek, Tanzania wildlife safari, "Children's day vibe in 20s") migrated from `blog_scrape/`.
- Must showcase the personal photos from `photos/` (8 loose photos; `attachments.zip` holds the same set plus 5 more, 11 total unique shots).
- Must surface social links. Confirmed: Instagram https://www.instagram.com/_.praju._._/, LinkedIn https://www.linkedin.com/in/prajakta-patil-1b3368296/, Blogspot https://yatrawithprajakta.blogspot.com. **Open:** any further links (email, venture link) not yet provided.
- **Open:** founder section — confirmed as wanted but deferred; its content, company name, and details are not yet provided. Do not fabricate.
- **Open:** brand identity (see below) — unanswered during init.
- Process constraint: the user explicitly asked to be asked about the design language before any visual build begins. Honor this in new-work.

## Brand Commitments

Confirmed facts:
- Owner's name: **Prajakta Patil**. "Prajakta" (प्राजक्ता) is the Marathi/Sanskrit name of the parijat flower (Nyctanthes arbor-tristis, night-flowering jasmine) — white petals, saffron-orange stems, blooms at night, falls by dawn.
- `photos/logo.jpg` is the mark of her **venture**, *muhurta yatra* — tagline "journey at the auspicious time" — not of the personal site.
- Established Blogspot name: *YatraWithPrajakta*. Her venture's public handle: @muhurtayatra.

**Binding visual constraint (user-pinned, 2026-10-13):** the site's theme is warm, very minimally Indian-inspired, heavily based on the prajakta/parijat flower — colours from the flower and imagery of the flower used in the website.

**Open:** the site's formal title treatment (Prajakta's name vs a yatra wordmark) — personal-name-led implied by the pinned theme, not yet confirmed.

## Evidence on Hand

- `blog_scrape/scraped_data.json` and `scraped_data.md` — 5 posts, verbatim full text, publish dates, author "Prajakta"; 16 downloaded post images in `blog_scrape/images/`.
- `photos/` — 8 personal photos + `logo.jpg` + `attachments.zip` (11 photos, ~5 unique beyond the loose set).
- Instagram bio (fetched 2026-10-13): "Prajakta Patil — Founder @muhurtayatra; Athlete / Trekker / Poet / Traveller / Tour Guide / Blog writer; Be Kind | Be You |"; travel highlights incl. Manali, Kullu, Chandigarh, Ujjain, Ashtavinayak. LinkedIn page exists but blocks automated reads.
- No testimonials, press, metrics, or professional bio on hand — future work must not fabricate any.

## Product Principles

1. Personal first — the person, her stories, and her photos lead; professional content is a section, not the frame.
2. Real content only — use her actual posts and photos; never invent bio facts, achievements, or social proof.
3. Simple to host — static output deployable to Cloudflare Pages with no server dependencies.
4. Undecided stays undecided — open facts (brand name, socials, founder section) are recorded as open, not guessed.
