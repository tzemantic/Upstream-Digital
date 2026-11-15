# Upstream Digital website

Static redesign of getupstreamdigital.com.

- `site/`: reimagined version (main)
- `archive/faithful-rebuild/`: responsive rebuild of the current design

Run: `cd site && python3 -m http.server 8000`, then open http://localhost:8000.
See `CLAUDE.md` for design tokens, content rules and open items.

## Deploying

Hosted on Netlify, connected to the GitHub repo. Every push to `main` publishes `site/` (settings and redirects in `netlify.toml`).
The contact form uses Netlify Forms (form name `contact`); set the notification email under Netlify > Forms.
Local testing can't submit the form; that only works on Netlify.
