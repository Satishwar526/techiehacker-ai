# TechieHacker V2 — upgrade instructions

This update preserves the existing custom domain, three archived articles in the supplied backup, and daily schedule (02:30 UTC / 08:00 IST). Use the small patch ZIP to avoid replacing your current news archive. Do not run a news workflow on a development branch: the existing workflow can deploy when manually triggered.

1. In the existing local repository, run `git status`. If clean, `git switch main` and `git pull --ff-only origin main`.
2. Create `git switch -c v2-development` (or switch to the existing branch). Copy the contents of the patch ZIP into the repository root, replacing the listed files. Do not replace `news.json` or the workflow.
3. Run `python3 scripts/build.py` and `python3 -m http.server 8080 --directory dist`. Open http://localhost:8080/ and test News, Lab and Search. Stop the server with Ctrl+C.
4. Run `git add scripts/build.py scripts/news.py site/style.css site/app.js V2-UPGRADE.md` and `git commit -m "Upgrade TechieHacker to V2"`. Push the branch: `git push -u origin v2-development`.
5. Open a pull request to main. Review and merge after testing. The push to main rebuilds and deploys without calling the news API. No DNS or secret changes required.
6. On main only, optionally manually run the newsroom once (up to three API generation attempts). Otherwise the daily schedule remains active.

The new source list has 19 configured endpoints, including research feeds; endpoints are runtime candidates, not verified live. The engine reports entry counts, eligible candidates, and safe API status/code diagnostics. It prioritizes source diversity, keeps the original seven-day window and three-attempt budget, and fails if all attempted generations error. Existing news stays intact on a failed build. Visuals are original procedural CSS/Canvas illustrations, not photos or prerecorded 4K video. Search covers published local content and curated entries, not the live web. Lab demonstrations are conceptual. No chatbot or newsletter service is included in this release.
