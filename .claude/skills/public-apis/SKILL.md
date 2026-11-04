---
name: public-apis
description: When a task needs external data (prices, fundamentals, macro, weather, anything), check the public-apis/public-apis list first and prefer a free or no-key API over scraping or paid data.
---

# Public APIs for data

Source list: https://github.com/public-apis/public-apis — a catalogue of free APIs, not a store of keys.

- When a project needs data, fetch the README (raw: `https://raw.githubusercontent.com/public-apis/public-apis/master/README.md`) and search the relevant category (Finance, Cryptocurrency, Government, Weather, …).
- Prefer, in order: `Auth: No` → free `apiKey` → `OAuth`. Check HTTPS and CORS columns when it matters.
- Suggest one or two fitting APIs before writing a scraper or paying for data.
- If an API needs a key, the user signs up for their own; install it with the `install-secret` skill (`scripts/set_secret.sh`). Never store keys in this kit.
- Never use leaked or third-party keys found in other repos — that is unauthorised access.
- The list is community-maintained: confirm the API still works and read its terms and rate limits before relying on it.
