# TechieHacker AI intelligence hub

Original static website with animated neural field (resolution scales up to 3840×2160), responsive design, light/dark mode, searchable category pages, article URLs and sitemap. No movies. News is intentionally empty until the first successful run; no fabricated current stories.

## Preview locally
Install Python 3.10+; run `python scripts/build.py`, then `python -m http.server 8080 --directory dist`. Open http://localhost:8080. No API key or external Python packages needed for the build. Google Fonts are optional network requests; system fonts fall back.

## GitHub Pages deployment
1. Create or back up a repository, default branch `main`. Upload the source files including hidden `.github/workflows/publish.yml` (git recommended). Do not upload only dist if you want automation.
2. Settings > Pages > Source > GitHub Actions. Ensure Actions is enabled, and repository/organization policies permit the workflow to write contents and deploy Pages. Branch protection may require adjusting the workflow or a PR-based process.
3. Settings > Secrets and variables > Actions > New repository secret: `OPENAI_API_KEY` (obtain from https://platform.openai.com/api-keys, separate billing). Optional repository variable `OPENAI_MODEL` defaults to gpt-4o-mini. Never add keys to HTML or git.
4. Actions > TechieHacker newsroom and deployment > Run workflow (main). Inspect logs for feed and generation failures and confirm the site. Scheduled runs every 3 hours, minute 17 UTC, up to 3 briefs per run (24/day). GitHub may delay/disable scheduled runs on inactive public repositories. Pushes build/deploy without API calls.
5. In Pages settings, configure custom domain `www.techiehacker.com`, verify domain ownership, then in Hostinger authoritative DNS set CNAME `www` to YOUR-USERNAME.github.io (replace any conflicting www record only after testing; leave mail and unrelated records alone). Enable HTTPS when available. Existing Netlify may remain until cutover. Apex domain redirect is optional and requires its own configuration.

## Editorial and operational limitations
Feed endpoints may change; this package does not scrape article bodies. Only dated excerpts within seven days with at least 100 characters are processed. Exact normalized URL deduplication, schema/length checks, source links and disclosure are included; these are not independent fact checking. Review published stories regularly; edit/remove items in news.json and push. For stricter editorial control, disable schedule or use PR approval. Respect feed terms and copyright. No third-party article imagery is copied. Research and learning resources are curated links, not automatically updated. No analytics, tracking or paid subscriptions are configured. API usage is capped by calls per run, not a monetary guarantee. Monitor billing. Workflow runs may succeed with no new stories; check logs. No live deployment or paid API requests were executed during creation.
