# Signals – what the agent can check, and where

A menu for 15:10: each signal is one module, one owner, one PR. First build the four marked **MVP**, then add
others only if the score on the labelled set goes up (`AGENTS.md`, rule 6).

The brief groups signals into Looks, Substance and Risk (p. 2). Most need no vision model: they are HTTP calls
and text. Every signal returns facts **with the URL it got them from**; the LLM judges from those facts, it does
not collect them (`AGENTS.md`, rules 2 and 3).

## Free sources tested on 25 Nov (no key needed)

One request each, against a well-known domain – not against any product of the challenge.

| Source | Request | Gives | Test result |
|---|---|---|---|
| RDAP | `https://rdap.org/domain/<domain>` | domain registration date (`events`, `eventAction: registration`) | python.org → 1995-03-27 |
| Wayback Machine CDX | `https://web.archive.org/cdx/search/cdx?url=<domain>&limit=1&output=json` | first archived snapshot | python.org → 1997-05-01 |
| crt.sh | `https://crt.sh/?q=<domain>&output=json` | TLS certificates; oldest `not_before` | python.org → 2011-10-10 (slow, can time out) |
| Have I Been Pwned | `https://haveibeenpwned.com/api/v3/breaches?domain=<domain>` (send a `User-Agent`) | known breaches for the domain | adobe.com → breach 2013-10-04 |

Rate limits and terms of use: not verified. Be a polite visitor (brief, p. 3): cache every response in
`out/cache/`, one request per source and product.

## Signals

| Kind | Signal | How | Source of the link | MVP |
|---|---|---|---|---|
| Looks | copyright year | regex on the footer text | the vendor page | **yes** |
| Looks | dead links in help/docs | HTTP status of linked help pages (max. 20, HEAD then GET) | each checked URL | **yes** |
| Looks | design age, screenshots that don't match the product | page screenshot (headless Chrome/Playwright) → a vision-capable LLM via API | the vendor page | later |
| Substance | domain age vs. "since 20xx" on the site | RDAP + Wayback CDX, compared with the claim | rdap.org / web.archive.org | **yes** (both) |
| Substance | product still alive | dates in changelog, release notes, blog, `sitemap.xml` `lastmod`, status page | those pages | later |
| Substance | customers confirm | search (Tavily) for customer sites that name the vendor; the vendor's own logo wall does not count | the customer's page | later |
| Substance | company exists | imprint → company name and register number → company register | register entry (API: not verified) | later |
| Substance | claims check out | features in docs or a partner marketplace (e.g. app store listings) | docs / marketplace page | later |
| Risk | breaches | Have I Been Pwned by domain; search for "<company> breach" | haveibeenpwned.com / press article | later |
| Risk | lawsuits, frozen after acquisition, founders' history | search, only sources the vendor did not write | press article | later |
| Any | HTTPS history | crt.sh oldest certificate | crt.sh | later |

## Rules for every signal module

- Input: the product URL (and the cache). Output: a list of facts, each `{"claim", "url", "quote", "checked_at"}`.
- A source that times out or fails gives **no fact**, never a guessed one; the verdict can then say what it could
  not check.
- Timeout on every request (house rule, Norma `py-scal-requests-no-timeout`). Use the shared fetch helper.
- No network in tests: a fixture per source in `tests/fixtures/` (made-up `.example` domains).
- Search snippets and model knowledge never become a fact (README, "How evidence is weighed").
