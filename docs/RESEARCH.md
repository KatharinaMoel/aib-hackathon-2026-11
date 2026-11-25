# What research says about spotting fake sites

<!-- One-page summary of three literature reviews (25 Nov 2026), turned into rules for our agent.
Details, all numbers with page/section, and every source link: docs/research/1–3. See docs/FILES.md. -->

**Read this with one caveat:** the studies looked at fake online shops, phishing, news and health sites –
not at B2B software vendors. Using them for vendors is our own inference. Every source below was opened and
checked by a research agent on 25 Nov 2026; a sample of five was re-checked against arXiv and Crossref.

## The 10 rules we take from it

| # | Rule for our agent | Evidence (short) | Source |
|---|---|---|---|
| 1 | **Leave the site first.** Check what others say about the vendor before reading its own pages in depth. | Professional fact-checkers left a site after 26 s on average and all 10 picked the reliable source; historians and students read the site itself and were often fooled (60 % of students chose the lobby site). | Wineburg & McGrew 2017 → [2-credibility](research/2-credibility.md) |
| 2 | **Looks are a weak signal**, in both directions. A polished site is cheap; a dated site can be solid. | Lay users mentioned "design look" in 46.1 % of credibility comments; experts far less (finance 16.4 % vs 54.6 %, health 7.6 % vs 41.8 %). | Fogg et al. 2002; Stanford et al. 2002 |
| 3 | **What the vendor says about itself is neutral** until an outside source confirms it (logos, "since 2008", About page, address). Trace each claim to the original. | Fact-checkers took About pages, .org domains and addresses "with a grain of salt"; checklists "focus on a website's most easily manipulated features". | Wineburg & McGrew 2017; Caulfield, SIFT |
| 4 | **Domain age counts, but only as a prior.** Young domain + "since 2010" claim = strong mismatch. A young start-up alone is not hollow. | Fraud shops averaged 2 years, legitimate 13; under 1 year = 4.5× odds of counterfeit. Hidden WHOIS owner data is normal and is *not* a signal. | Beyond Phish (S&P 2023); Lemons (WWW 2015); Caulfield → [1-fraud-sites](research/1-fraud-sites.md) |
| 5 | **Check the social and outgoing links.** Real vendors link out (docs, GitHub, status page, partners) and their social links lead to matching profiles. | 81.5 % of fraud shops had no social link and 16.8 % a broken or wrong one (legitimate: 33.9 % none); legitimate sites had 1.91× more outgoing links. | Beyond Phish (S&P 2023) |
| 6 | **Look for copied or template content** (About, team, customer texts found on other sites). | Scam sites run in campaigns that reuse templates and text, often copying "About us" from real shops. | ScamMagnifier (NDSS 2025); Drew & Moore 2014 |
| 7 | **Look for the tells of generated sites:** leftover chatbot phrases, `[Your Name]`-style placeholders, "Admin" authors, contact addresses that cannot receive mail (no MX record). | All 49 AI content-farm sites had leftover chatbot phrases; 8 of 27 contact emails were invalid. | NewsGuard 2023 → [3-ai-and-vendors](research/3-ai-and-vendors.md) |
| 8 | **Never use an AI-text detector score as evidence.** | Detectors flagged non-native essays as AI at 61 % on average; none of 14 tools reached 80 % accuracy; OpenAI withdrew its own classifier. A score also has no link to check. | Liang et al. 2023; Weber-Wulff et al. 2023 |
| 9 | **"Not blocklisted" means nothing.** | Google Safe Browsing caught 0.46 % of fraud shops. | Beyond Phish (S&P 2023) |
| 10 | **Don't doubt everything.** Commit to a call when the evidence supports it; one past incident (breach, outage) does not cancel a solid record; missing certificates or a low turnover alone never make a vendor hollow. | "Our problem is not gullibility, but rather the gullibility of cynics"; UK procurement guidance: never exclude a supplier on financial data alone. | Caulfield 2018; UK EFS guidance 2026; ENISA 2023 |

## How this changes our plan

- **Order of work:** outside checks first (search for the vendor on other domains, register, archive), the
  vendor's own pages second. This matches the Stackgini brief: "signals that still mean something take time
  or need someone else".
- **New cheap signals** for `docs/SIGNALS.md`: social links resolve to matching profiles; number of outgoing
  links; chatbot leftovers and placeholders; MX record of the contact domain; `/.well-known/security.txt`.
- **Judge rules 2, 3 and 4** in `docs/SIGNALS.md` already follow rules 2, 3 and 10 above.

## No verified source for

TLS certificates, a missing imprint or legal page, and reviews as fraud signals – none of the papers we opened
measured them. Use them only as weak hints, and say so.

## The experts behind it

| Topic | Experts / groups | Details |
|---|---|---|
| Fraudulent websites | Adam Doupé (Arizona State Univ.), Tyler Moore (Univ. of Tulsa), Lieven Desmet's group (KU Leuven) | [research/1-fraud-sites.md](research/1-fraud-sites.md) |
| How people and experts judge credibility | B.J. Fogg (Stanford Web Credibility Project), Sam Wineburg & Sarah McGrew (Stanford, now Digital Inquiry Group), Mike Caulfield (SIFT) | [research/2-credibility.md](research/2-credibility.md) |
| AI-generated sites, vendor checks | Liang/Zou (Stanford), Weber-Wulff et al., NewsGuard, Hanley & Durumeric; CISA, ENISA, UK Government | [research/3-ai-and-vendors.md](research/3-ai-and-vendors.md) |
