# Recognising fraudulent, fake and scam websites: what research says

Research date: 2026-11-25. Every paper listed here was downloaded and read as a PDF (text extracted with `pdftotext`). Venue, year and DOI were checked against Crossref. Page and section references point to the PDF at the listed link. Citation counts come from OpenAlex and Crossref. They are approximate and change over time, so re-check them before quoting them.

Scope caveat: all three groups study **consumer-facing** fraud: fake shops, counterfeit stores, fake escrow and investment sites, and malicious domain registrations. None of them studies fake **B2B software vendors**. The transfer column in the table below is my judgement, not a finding of the papers.

---

## Expert 1: Adam Doupé and the ASU SEFCOM group (with Marzieh Bitaab and Adam Oest)

- **Who:** Adam Doupé, Professor at Arizona State University and Director of its Center for Cybersecurity and Trusted Foundations (checked on https://adamdoupe.com/). First author of both papers below: Marzieh Bitaab (ASU). Co-author Adam Oest was at PayPal, later Amazon, and is known for large-scale phishing measurement.
- **Why an expert:** the group wrote the two most recent top-venue papers specifically on fraudulent e-commerce websites, at IEEE S&P 2023 and NDSS 2025, both top-4 security venues. OpenAlex lists Doupé with about 130 works, about 4,700 citations and h-index about 35 (approximate, from openalex.org/A5050806439).

### Papers (opened and checked)
1. **Bitaab, Cho, Oest, Lyu, Wang, Abraham, Wang, Bao, Shoshitaishvili, Doupé. "Beyond Phish: Toward Detecting Fraudulent e-Commerce Websites at Scale." IEEE Symposium on Security and Privacy (S&P) 2023.** DOI 10.1109/SP46215.2023.10179461. Free PDF: https://sefcom.asu.edu/publications/beyondphish-oakland23.pdf . Code and data: github.com/mbitaab/beyondphish (the URL appears in the paper; I did not open the repo).
2. **Bitaab, Karimi, Lyu, Oest, Kuchhal, Saad, Ahn, Wang, Bao, Shoshitaishvili, Doupé. "ScamMagnifier: Piercing the Veil of Fraudulent Shopping Website Campaigns." NDSS 2025.** DOI 10.14722/ndss.2025.240763. Free PDF: https://ndss-symposium.org/wp-content/uploads/2025-763-paper.pdf

### Key findings
- **Dataset (Beyond Phish, Sec. VI-A, Table IV):** 6,127 fraudulent sites crowdsourced from Reddit /r/Scams, plus 12,330 legitimate e-commerce sites. Legitimate sites came partly from Palo Alto Networks and include newly registered but legitimate domains.
- **Blocklists miss almost all fraud shops (Abstract, Sec. V-B):** Google Safe Browsing detected 0.46% of the dataset. Within it, APWG flagged only 25 FCWs and GSB only 10. *Takeaway: "not on a blocklist" is near-worthless evidence of legitimacy.*
- **Classifier quality (Abstract, Table V, Table VII):** neural network: FPR 1.68%, detection 87.14% on the test set. In a 14-month live user study on 2,223 Reddit submissions: accuracy 98.38%, FPR 1.34%. On Palo Alto real-world data: FPR 2.46%, detection 94.88%. Phishing detectors fail on fraud shops: Cantina+ had 22.22% FPR and CheckPhish detected 18.87%. ROC AUC was 0.96.
- **Most important features (Sec. VI-E, Table VIII, DeepSHAP):** "Valid social media, cheap TLD, and the number of external links are among the most important." Domain age matters more for assigning the *fraudulent* label.
- **Price is no longer a reliable tell (Sec. IV-E):** older studies used steep discounts, but "most of the recent FCWs do not offer significant discounts."
- **ScamMagnifier (NDSS 2025):** crawled 1,155,237 shopping domains (May 2023 to June 2024), found 46,746 fraudulent ones, and ran 41,863 automated checkouts, which revealed 5,278 merchant IDs (Abstract).
  - Merchant ID at checkout is a stable, hard-to-change signal (Sec. I).
  - 54.55% of fraudulent sites are run by only 10 merchant IDs, and one merchant ID covers 974 domains (Sec. V-A). The fraud is campaign-based.
  - 97.73% are monetised within less than a year of domain registration, and 20.17% have transactions within 10 days of creation (Sec. V).
  - Platforms: 58.74% Shopify, 19.13% Wix, 18.69% Squarespace, 3.42% other (Sec. V-A).
  - Traffic sources: Facebook/Instagram ads 28.78%, Google 21.10%, Bing 9.38% (Sec. I).
  - Combining ScamMagnifier's checkout model with Beyond Phish raised detection from 59.30% to 76.74% at the same 0.49% FPR (Sec. VI). This also shows how much Beyond Phish alone misses on newer data.
- **Evasion (Beyond Phish Sec. VI-F):** content features cost the attacker nothing to change. An aged domain costs at least about $1,000 and can partly bypass the model (Fig. 8). Removing domain age from the model costs little ("negligible performance loss"). Changing the cheap-registrar, registration-period or private-WHOIS features gives bypass rates of only 1.21%, 1.20% and 2.39%. Adding a *valid* social link gives a 13% bypass rate in the best case for the attacker. ScamMagnifier documents sites that route the payment through a *second* domain so the payment processor never sees the real shop (Fig. 7, Sec. V).

---

## Expert 2: Tyler Moore (University of Tulsa, formerly Southern Methodist University)

- **Who:** Tyler Moore, Tandy Professor of Cyber Security and Information Assurance and Department Head of the School of Cyber Studies, University of Tulsa. He directs the Security Economics Lab and co-edits the *Journal of Cybersecurity* (checked on https://tylermoore.utulsa.edu/).
- **Why an expert:** about 15 years of measurement papers on online scams: counterfeit stores, fake escrow, high-yield investment programs (HYIP) and other Ponzi schemes, Bitcoin scams and tech-support scams (publication list at https://tylermoore.utulsa.edu/pub.html). OpenAlex lists "Tyler W. Moore" (Tulsa) with about 212 works, about 11,700 citations and h-index about 46. That profile may merge some records, so verify.

### Papers (opened and checked)
1. **Wadleigh, Drew, Moore. "The E-Commerce Market for 'Lemons': Identification and Analysis of Websites Selling Counterfeit Goods." WWW 2015 (Security and Privacy track), pp. 1188–1197.** DOI 10.1145/2736277.2741658. Free PDF: https://tylermoore.utulsa.edu/www15.pdf
2. **Drew, Moore. "Automatic Identification of Replicated Criminal Websites Using Combined Clustering." International Workshop on Cyber Crime (IWCC), IEEE S&P Workshops 2014.** DOI 10.1109/SPW.2014.26. Free PDF (author's pre-publication copy): https://tylermoore.utulsa.edu/iwcc14.pdf

### Key findings
- **Lemons, setup (Sec. 2–3):** 225 search queries across 25 brands, 6,979 distinct websites in January 2014, and 602 hand-labelled sites (234 counterfeit). The SVM reached 86.4% accuracy, 86.5% precision and 76.9% recall (Table 1).
- **Odds ratios from logistic regression (Table 2):**

  | Signal | Odds ratio | p-value | Significant? |
  |---|---|---|---|
  | Large iframe loading an external, non-top-1000 site | 204.3 | <0.0001 | yes |
  | Page replaced by a brand-enforcement takedown notice | 18.05 | 0.0005 | yes |
  | WHOIS registration under 1 year | 4.50 | 0.0001 | yes |
  | "replica" in the domain name | 4.23 | 0.0002 | yes |
  | Each additional currency offered | 1.27 | 0.0017 | yes |
  | Each additional distinct brand mentioned | 1.18 | <0.0001 | yes |
  | Each point of average % discount | 1.045 | <0.0001 | yes |
  | Webmail address (gmail, yahoo, hotmail) on the page | 2.0 | 0.17 | **no** |
  | Private or China WHOIS | 1.33 | 0.38 | **no** |
  | Duplicate prices | — | 0.45 | **no** |
  | Site in Alexa top 100K (protective) | 0.072 | <0.0001 | yes |
  | Homepage also mentions the brand (protective) | 0.496 | 0.0097 | yes |
- **Domain age (Sec. 4.3, Fig. 5):** sites under 1 year old were much more likely to be counterfeit, "despite the trend, there are a large number of exceptions." WHOIS creation date could only be extracted for 56.35% of domains.
- **Country (Sec. 4.3, Table 8):** fake sites had 17 times the odds of a WHOIS registration in China rather than the US, but only twice the odds of being *hosted* in China. Private or proxy WHOIS gave only 25% higher odds, just outside statistical significance.
- **Replicated sites (IWCC 2014, Sec. I and V):** scammers cheaply change name, domain and registration data, but "website structure (if coming from a kit) or the text on a page (if the criminal's English or writing composition skills are weak) are more costly to change." 1,216 fake-escrow sites formed 161 clusters plus only 7 singletons. 4,191 HYIP sites formed 864 clusters plus 530 singletons. Combining HTML-tag, sentence and file-structure similarity reached an adjusted Rand index of 0.952 against manual ground truth (Sec. IV).

---

## Expert 3: Lieven Desmet, Thomas Vissers, Jan Spooren and Wouter Joosen (imec-DistriNet, KU Leuven), with EURid (.eu registry)

- **Who:** Lieven Desmet, research manager at imec-DistriNet, KU Leuven. The affiliation is taken from the paper; OpenAlex shows the same.
- **Why an expert:** the group runs a long-term collaboration with the .eu registry on malicious domain registrations, published at RAID 2017, ACSAC 2019 and ACM DTRAP 2021. Their system was put into production at a real top-level-domain registry. OpenAlex lists Desmet with about 145 works, about 2,200 citations and h-index about 25 (approximate).

### Papers
1. **Desmet, Spooren, Vissers, Janssen, Joosen. "Premadoma: An Operational Solution to Prevent Malicious Domain Name Registrations in the .eu TLD." ACM Digital Threats: Research and Practice 2(1), 2021** (extended version of the ACSAC 2019 paper). DOI 10.1145/3419476. Free PDF (author version, KU Leuven repository): https://lirias.kuleuven.be/retrieve/78e2d7e8-2dfa-4aed-9af8-2bb0eddc8be9 . Opened and checked.
2. *Not verified (full text not opened, paywalled copies only):* Vissers et al., "Exploring the Ecosystem of Malicious Domain Registrations in the .eu TLD," RAID 2017, DOI 10.1007/978-3-319-66332-6_21. Its numbers below are quoted only *as cited inside Premadoma*.

### Key findings
- **Context:** the malicious registrations in this work are mainly spam, phishing, malware and botnet domains, not fake shops specifically (Sec. 1).
- **Campaigns (Premadoma Sec. 1, citing Vissers et al. 2017):**
  - About 80% of malicious .eu registration campaigns come from at most 20 actors.
  - Blocklisting takes up to 5 days for 73% of malicious registrations.
  - 19% of campaign domains never appear on any blocklist.
  - Only 2.53% of registrations were labelled malicious (Sec. 3).
- **Signals (Sec. 4, Table 1):**
  - Reputation of the "facilitators", meaning the share of past malicious registrations tied to the same registrar, e-mail provider, phone number or name server.
  - Similarity of the registrant's name, address, e-mail and phone to known bad registrations (Levenshtein distance).
  - Domain-name randomness and length, hour of registration, and an address-validity score.
  - Registrant fields and name-server domains carried the most information gain (Fig. 5).
- **Performance (Sec. 5):** 66.23% recall at 84.57% precision and 0.30% FPR over an 11-month test. Campaign-level results: 76.68% recall and 87.20% precision, with 17 of 20 campaigns well predicted.
- **Deployment:** the system went into production at the .eu registry in 2018 and was followed by a "remarkable decline in malicious domain registrations" (Sec. 6 and conclusion).
- **Evasion (Sec. 7.1):**
  - EP1, day-to-day variance: one campaign used 98 different registrant contacts and changed daily, and only 27% of its domains were ever blocklisted.
  - EP2, inactivity gaps longer than the training window.
  - EP3, registering extra domains to dilute reputation scores.

---

## Additional verified source (payment chokepoint, UCSD and ICSI group)
- **Levchenko, Pitsillidis, Chachra, Enright, Félegyházi, Grier, Halvorson, Kanich, Kreibich, Liu, McCoy, et al. "Click Trajectories: End-to-End Analysis of the Spam Value Chain." IEEE S&P 2011.** DOI 10.1109/SP.2011.24. Free PDF: https://cseweb.ucsd.edu/~savage/papers/Oakland11.pdf . I checked the title and the first-page author list; the list continues past McCoy.
- **Finding (Abstract and Sec. V):** "95% of spam-advertised pharmaceutical, replica and software products are monetized using merchant services from just a handful of banks." Just three banks served over 95%. This supports ScamMagnifier's point that payment is the hardest link for scammers to change.

---

## Signal table

Abbreviations: **BP** = Beyond Phish (S&P 2023); **SM** = ScamMagnifier (NDSS 2025); **LM** = Lemons (WWW 2015); **RC** = Replicated Criminal sites (IWCC 2014); **PD** = Premadoma (DTRAP 2021); **CT** = Click Trajectories (S&P 2011).

In the last column, "free data" means sources such as public RDAP/WHOIS, Tranco, Common Crawl, crt.sh and the Wayback Machine. These tool suggestions are mine and do not come from the papers.

| Signal | Finding + number | Source | Applies to software vendors? | Automatable in 7 h with free data? |
|---|---|---|---|---|
| Domain age | Fraud sites average 2 years old vs. 13 years for legitimate ones. Age under 1 year gives 4.5× odds of counterfeit. Many exceptions. 97.73% of fraud shops are monetised within less than 1 year of registration. | BP Sec. V-A; LM Table 2, Sec. 4.3; SM Sec. V | Yes, but young legitimate start-ups produce false positives. Use it only as a weak prior. | Yes. RDAP or WHOIS creation date. Note: LM got dates for only 56% of domains. |
| Registration period | "Most of the FCWs are only registered for 1 year." Bypass rate when changed: 1.20%. | BP Sec. V-A, VI-F | Partly; many legitimate firms also renew yearly. Weak. | Yes (RDAP expiry minus creation date). |
| Private / proxy WHOIS | About one third of fraud sites use it. Not significant in LM (odds 1.33, p=0.38; "+25% odds, just outside significance"). | BP Sec. V-A; LM Table 2, Sec. 4.3 | Weak. Privacy-redacted WHOIS is very common for legitimate firms (my note, not from the papers). | Yes, but low value. |
| Registrant / host country mismatch | 56.49% of fraud sites register outside US/CA/UK, of which 42.86% in Panama. Legitimate sites have 3× the odds of the same host and registrant country. China-registered gives 17× odds of counterfeit (2014 data). | BP Sec. V-A; LM Table 8 | Partly. Check against the company address claimed on the site. | Yes (RDAP country plus GeoIP of the IP), but often redacted. |
| Cheap registrar / cheap TLD | 28.21% of fraud sites use the 50 cheapest TLDs (under about $2, e.g. .xyz, .store). Cheap TLD is among the top-3 features. Registrar list in BP: Namecheap, GoDaddy, Porkbun, NameSilo, Danesco, Hostinger. | BP Sec. V-A, VI-E | TLD: yes. Registrar: weak, since legitimate SaaS firms use the same registrars. | Yes (static TLD list). |
| Social media links valid? | 81.47% of fraud sites have no social link and 16.80% have an invalid one (logo without a link, or a link to someone else's or a generic page). Only 33.85% of legitimate sites have none. Top-3 feature, adds 3% AUC. Faking a valid profile bypasses the model in 13% of cases. | BP Sec. V, VI-E, VI-F | **Yes, strongly.** Check that LinkedIn, X and GitHub links resolve to a real profile matching the company name. | Partly. Checking whether a link exists and points to a profile is easy. Account age and follower counts are blocked or rate-limited on major platforms (my note). |
| Few outgoing links ("closed world") | Legitimate sites have 1.91× more outgoing links. Top-3 feature. | BP Sec. V-A, VI-E | Yes (docs, GitHub, status page, integrations, customers). | Yes (parse HTML). |
| Script-tag count | 23 average for fraud vs. 13 for legitimate. | BP Sec. V-A | Unclear; modern SaaS sites are script-heavy. | Yes, low value. |
| Traffic rank | Alexa top 100K gives odds 0.072 (strongly protective). Used as a feature in BP. | LM Table 2; BP Sec. V-A | Yes, absence is weak evidence for niche B2B. | Yes, use the Tranco list. Alexa was shut down; that fact is from my knowledge, so verify it. |
| Blocklist status | Google Safe Browsing detects 0.46% of fraud shops. 19% of malicious campaign domains are never blocklisted. Blocklisting is slow: 73% take up to 5 days. | BP Abstract, V-B; PD Sec. 1 | Yes. "Not blocklisted" ≠ safe. | Yes (Safe Browsing API with a free key), but low recall. |
| Shared template / copied content | Scam sites are cloned in campaigns. Structure and text are costly to change: fake escrow formed 161 clusters from 1,216 sites. Fraud shops reuse stock images and copy text, including the "About us" page from real shops. 54.55% of fraud shops are run by 10 merchants. | RC Sec. I, V; SM Sec. V-A, discussion of shared content (Fig. 12–13) | **Yes.** Copied "About", team or customer text is a strong tell for fake vendors too (by analogy; not measured for SaaS). | Partly. Search exact sentences from the About page and compare against known sites. Clustering at scale does not fit 7 h. |
| Payment / merchant identity | Merchant ID is "a stable, difficult-to-bypass feature". 95% of spam-advertised goods were paid through 3 banks. Some fraud shops route payment via a second domain. | SM Sec. I, V; CT Abstract, Sec. V | Limited. B2B often sells by sales call or invoice, but a Stripe or Paddle checkout naming a different legal entity is checkable. | Mostly no. Needs a checkout run; where SM's automated checkout failed, the top cause (46.12%) was server-side credit-card-only payment. |
| Low or discounted prices | Old tell that has weakened: "most of the recent FCWs do not offer significant discounts." Average discount still significant in 2014 (odds 1.045 per % point). | BP Sec. IV-E; LM Table 2 | Rarely. Implausible pricing claims could be a weak tell. | Yes to scrape; low value. |
| Many currencies / brand stuffing | +27% odds per extra currency; +18% per extra brand mentioned. | LM Table 2 | Brand stuffing, yes: many unrelated product names or keyword-stuffed pages. | Yes. |
| Free webmail contact address | Hypothesised; not significant (odds 2.0, p=0.17). | LM Table 2 | Plausible but unproven by these papers. | Yes. |
| Hidden large iframe to an external site | Odds 204 of counterfeit; signals a hacked or redirecting site. | LM Table 2 | Yes, as a compromise indicator. | Yes. |
| Hyphens, digits, sub-domain depth in the name | Used as features. Fraud sites average 19.87 sub-domains vs. 8.86 (BP's numbers). | BP Sec. V-A | Weak. | Yes. |
| Registrant reputation / similarity | Registrant fields and name-server domains carry the most information gain. 66% recall at 85% precision before the domain is used. | PD Sec. 4–5, Fig. 5 | Only for registries with full registrant data. | **No.** Registrant data is private to registries. |
| Hosting platform | 58.74% of fraud shops run on Shopify, 19.13% on Wix, 18.69% on Squarespace. These are base rates among fraud shops, not a contrast with legitimate shops. | SM Sec. V-A | Weak. A "SaaS company" whose whole site is a website-builder template is a soft flag (my inference). | Yes (HTML fingerprints). |
| Ad-driven traffic, fast monetisation | 28.78% of victims arrive via Facebook/Instagram ads; 20.17% of shops have transactions within 10 days of registration. | SM Sec. I, V | Partly. Meta Ad Library lookup is possible. | Partly. |
| TLS certificate, imprint/legal page, reviews | **Not measured** in any paper opened here. | — | — | I do not have a verified source on these as signals. |

---

## What scammers neglect or get wrong (the "tells")

1. **Social proof that does not link anywhere.** Fraud sites add Facebook, X or Instagram *logos* without links, or with links to someone else's page. Maintaining real profiles is "costly, time-consuming" and risks exposure (BP Sec. V, VI-F; 79.08% of fraud sites have no social link).
2. **Closed world.** Few or no outbound links (BP Sec. V-A).
3. **Cheapest possible domain.** Cheap TLD, 1-year registration, budget registrar, very young domain (BP Sec. V-A). An aged domain would cost at least about $1,000 (BP Sec. VI-F).
4. **Copy-paste at scale.** Kit-based HTML structure, reused sentences (especially when "writing composition skills are weak"), stock or stolen product images, and an "About us" copied from a real shop (RC Sec. I; SM Fig. 12–13). LM targeted "lazy" owners who copy products but not prices, but duplicate prices were *not* significant (LM Sec. 3.1, Table 2).
5. **Same money pipe across many sites.** A few merchant IDs or banks serve most campaigns (SM Sec. V-A; CT Sec. V).
6. **Mismatched geography.** Registrant country differs from hosting country and from the claimed location (BP Sec. V-A; LM Table 8).
7. **Daily-changing but similar registrant details.** Advanced campaigns rotate registrant data, but a similar pattern remains (PD Sec. 7.1).

## Failure modes to keep in mind
- Labels come from crowds (Reddit) or blocklists. Both are incomplete and biased toward reported, consumer-facing scams (BP Sec. III–IV; PD subsection "Addressing dataset challenges").
- Signals drift. Prices stopped being a tell, and social logos appeared on fraud sites after 2018 (BP Sec. IV-E, V).
- All feature models trained on shops; none was evaluated on B2B software vendors. A young, legitimate start-up looks "fraudulent" on age, traffic rank and registrar features. Use these signals as weighted evidence with links, not as a verdict.
