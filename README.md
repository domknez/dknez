# domagoj-knez.dev

One-page personal site. Static: no build step, no framework, no dependencies.

```
index.html          the page
404.html
robots.txt          allows search engines and AI crawlers
sitemap.xml
llms.txt            plain-text brief for language models
CNAME               knez.dev
assets/
  styles.css
  main.js
  portrait.jpg
  og.png            1200x630 social preview card
files/
  Domagoj_Knez_CV.pdf   one-page CV, generated from tools/make-cv.py
tools/
  make-og.py        regenerates og.png (needs Pillow)
  make-cv.py        regenerates the CV PDF (needs reportlab)
  fonts/            Bricolage Grotesque, Space Grotesk, JetBrains Mono as TTF,
                    used by make-cv.py so the PDF matches the site
```

## Run locally

```sh
python3 -m http.server 8000   # then open http://localhost:8000
```

## Deploy to GitHub Pages

1. Push to a repo. For `https://<user>.github.io` name the repo `<user>.github.io`; any other name serves at `https://<user>.github.io/<repo>/`.
2. Settings -> Pages -> Source: *Deploy from a branch*, branch `main`, folder `/ (root)`.
3. `.nojekyll` is already here so Jekyll does not touch the files.

### Custom domain (knez.dev, registered at Namecheap)

`CNAME` already contains `knez.dev`. In Namecheap -> Domain List -> Manage -> *Advanced DNS*, using Namecheap BasicDNS:

| Type | Host | Value |
| --- | --- | --- |
| A | @ | 185.199.108.153 |
| A | @ | 185.199.109.153 |
| A | @ | 185.199.110.153 |
| A | @ | 185.199.111.153 |
| CNAME | www | `<user>.github.io.` |

Delete Namecheap's default *URL Redirect* / parking records first, or the A records will not take. Then GitHub -> Settings -> Pages -> Custom domain -> `knez.dev`, wait for the DNS check, and tick **Enforce HTTPS**.

`.dev` is on the HSTS preload list, so it is HTTPS-only by design — do not link to `http://` anywhere.

### After the domain resolves

- Google Search Console: add `knez.dev`, verify by DNS TXT, submit `https://knez.dev/sitemap.xml`
- Bing Webmaster Tools: import from Search Console in one click (this also feeds DuckDuckGo, which uses Bing's index)

## Before going live

- [x] `assets/portrait.jpg`
- [x] `assets/og.png` — regenerate with `tools/make-og.py` if the photo or the strapline changes

- [x] `files/Domagoj_Knez_CV.pdf`
- [ ] GitHub and LinkedIn URLs in the contact section (currently `github.com/domknez`, `linkedin.com/in/dknez`)
- [ ] Bump `lastmod` in `sitemap.xml` when you change the page

## SEO and AI search

- `robots.txt` allows every mainstream crawler and explicitly allows AI crawlers (GPTBot, OAI-SearchBot, ClaudeBot, PerplexityBot, Google-Extended, Applebot-Extended, CCBot and others) so the site can be indexed *and cited* by AI answers.
- `sitemap.xml` — one URL; bump `lastmod` when the content changes materially.
- `llms.txt` — a plain-text brief for language models at `/llms.txt`, following the llmstxt.org convention: stack, projects, education, availability, all as flat facts. Keep it in sync with the page.
- JSON-LD `@graph` in `index.html`: `WebSite`, `ProfilePage`, `Person` and `Organization` (CoreTech). This is what feeds knowledge panels and gives AI answers something unambiguous to quote. Validate at <https://validator.schema.org/>.
- All content is server-rendered HTML with real `h1`/`h2`/`h3` structure — no JavaScript needed to read the page, which is what most AI crawlers require.
- No email address in the markup, so it is also absent from structured data on purpose.

## Regenerating the CV

`tools/make-cv.py` draws the CV with ReportLab using the same fonts and Latte palette as the site, so the PDF and the page look like one thing. Text stays selectable and the fonts are embedded.

```sh
python3 -m venv .venv && .venv/bin/pip install reportlab pillow
.venv/bin/python tools/make-cv.py
```

It lays out in one flowing column and breaks to a second page automatically if the content grows; page numbers only appear when there is more than one page.

## Notes

- **Theme** follows the OS by default; the toggle sets an explicit choice in `localStorage`. The inline script in `<head>` applies it before first paint, so there is no flash.
- **Email** never appears as one string in the HTML. `main.js` assembles `mailto:` from `data-u` / `data-d` at runtime. Stops regex scrapers, not headless browsers. If the domain is behind Cloudflare, leave Scrape Shield -> *Email Address Obfuscation* on as well.
- **Fonts** come from Google Fonts. To go fully self-hosted, download Bricolage Grotesque, Space Grotesk and JetBrains Mono into `assets/fonts/` and swap the `<link>` for `@font-face` rules.
- **Colours** are Catppuccin Macchiato (dark) and Latte (light), defined once at the top of `styles.css`.
