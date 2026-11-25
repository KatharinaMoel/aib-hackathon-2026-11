# 3 - AI-generated sites and software vendor due diligence

Research notes for the "is this SaaS product real, alive and trustworthy?" agent.
Researched 2026-11-25. Every source below was opened on that day unless it says "not verified".
Page numbers: "PDF p." means the page index in the PDF file, not the printed page number.

**Bottom line for the agent**

1. **Do not use AI-text detector scores as evidence.** Four independent sources (below) show high or
   uncontrolled false-positive rates, easy evasion by paraphrasing, and one major vendor (OpenAI)
   withdrew its own detector for low accuracy. A "this text looks AI-written" score cannot be
   checked by a user, so it fails the brief's "checkable link for every reason" rule anyway.
2. **Use concrete, checkable artefacts instead**: leftover chatbot phrases, unfilled template
   placeholders, bounced contact domains, missing registry entries, claimed certificates that do
   not appear in the issuer's register, no vulnerability-disclosure channel, a changelog with no
   history in web archives.
3. **Absence is weak evidence.** Both procurement guides warn against excluding a supplier on one
   missing signal (no credit rating, low turnover, no certification) - this protects small and
   young vendors from false alarms.

---

## Part A - AI-generated websites and AI-text detection

### A1. Liang, Yuksekgonul, Mao, Wu, Zou (Stanford) - detector bias against non-native writers

- **Title:** "GPT detectors are biased against non-native English writers"
- **Who / why credible:** Stanford group led by James Zou (Associate Professor of Biomedical Data
  Science, Stanford, courtesy appointment in Computer Science; per his own site
  <https://www.james-zou.com/>, opened). Widely cited study of off-the-shelf detectors.
- **Year / venue:** arXiv 2023 (v3, July 2023). The arXiv PDF says "The published version of this
  study can be accessed at: www.cell.com/patterns/fulltext/S2666-3899(23)00130-7" (journal
  *Patterns*). The cell.com page returned HTTP 403 to my fetch, so the journal record itself is
  **not verified**; the arXiv version is.
- **Link (verified):** <https://arxiv.org/abs/2304.02819> (PDF: <https://arxiv.org/pdf/2304.02819>)
- **Key numbers (Results section, first subsection, PDF p.2):** seven widely used detectors, 91
  human-written TOEFL essays and 88 US 8th-grade essays. Near-perfect on the US essays, but
  "average false positive rate: 61.22%" on the TOEFL essays; 18 of 91 (19.78%) flagged by all seven
  detectors; 89 of 91 (97.80%) flagged by at least one. Simple prompting also bypassed detectors.
  Authors "caution against their use in evaluative or educational settings".

### A2. Weber-Wulff et al. - test of 14 detection tools

- **Title:** "Testing of Detection Tools for AI-Generated Text"
- **Authors:** Debora Weber-Wulff, Alla Anohina-Naumeca, Sonja Bjelobaba, Tomáš Foltýnek,
  Jean Guerrero-Dib, Olumide Popoola, Petr Šigut, Lorna Waddington (academic-integrity researchers;
  Weber-Wulff, HTW Berlin, is a long-standing plagiarism-software tester - affiliation from my
  background knowledge, not re-checked).
- **Year / venue:** 2023; arXiv lists journal ref *Int J Educ Integr* 19, 26 (2023),
  DOI 10.1007/s40979-023-00146-z. The Springer page redirected to a login, so I verified the
  arXiv version only.
- **Link (verified):** <https://arxiv.org/abs/2306.15666>
- **Key numbers (arXiv v2 PDF, Sect. 6 Discussion, ~PDF p.28; Sect. 7 Conclusion):** 14 tools
  (incl. Turnitin and PlagiarismCheck); "all scored below 80% of accuracy and only 5 over 70%";
  false positives ranged "from 0% (Turnitin) to 50% (GPT Zero)"; false negatives from 8% to 100%;
  paraphrasing and machine translation make evasion easy; tools give a score "without any
  possibility of verification or evidence". Conclusion: "unsuitability for use as evidence".

### A3. Sadasivan, Kumar, Balasubramanian, Wang, Feizi (University of Maryland) - theoretical limits

- **Title:** "Can AI-Generated Text be Reliably Detected?"
- **Year / venue:** arXiv 2023 (v4 January 2025); arXiv page states "Published in Transactions on
  Machine Learning Research (TMLR)".
- **Link (verified):** <https://arxiv.org/abs/2303.11156>
- **Key findings (abstract):** recursive paraphrasing "can significantly reduce detection rates"
  across detector types including watermarks; watermarks can be spoofed so human text is labelled
  AI-generated; the best possible detector's AUROC is bounded by how close AI text is to human text,
  so detection gets harder as models improve. (Abstract only read; no page-level numbers taken.)

### A4. OpenAI - withdrawn AI text classifier

- **Title:** "New AI classifier for indicating AI-written text", OpenAI, 31 January 2023.
- **Link (verified):** <https://openai.com/index/new-ai-classifier-for-indicating-ai-written-text/>
- **Key numbers:** on OpenAI's own English challenge set, 26% true positive rate, 9% false
  positive rate. Update on the page: "As of July 20, 2023, the AI classifier is no longer available
  due to its low rate of accuracy." A vendor's own self-assessment, but it is a strong signal that
  even the model maker could not build a usable detector.

### A5. NewsGuard - tracking AI content-farm news sites (recognised tracker)

- **Who / why credible:** NewsGuard Technologies rates news-site reliability and runs a public
  tracker of AI-generated news sites. It is a commercial company; its criteria are its own, not an
  independent standard.
- **Report 1 (verified):** McKenzie Sadeghi and Lorenzo Arvanitis, "Rise of the Newsbots:
  AI-Generated News Websites Proliferating Online", NewsGuard, 1 May 2023 (updated 1 and 5 May 2023).
  <https://www.newsguardtech.com/special-reports/newsbots-ai-generated-news-websites-proliferating/>
  - 49 sites in seven languages; **all 49** had at least one article with chatbot error text, e.g.
    "as an AI language model", "I cannot complete this prompt"; one article said "I am not capable
    of producing 1500 words...".
  - Bylines "Admin" / "Editor" or none; fake author profiles whose photos failed a reverse image search.
  - About page left unfilled: "This website was founded in [date] by [Your Name]" (built with a free
    About-Us generator); Terms and Privacy pages from a disclaimer generator.
  - Of 29 sites with contact info, 8 had **invalid email addresses**, 17 did not reply, 2 confirmed
    AI use.
- **Tracker (verified):** "Tracking AI-enabled Misinformation: 3,749 AI Content Farm sites (and
  Counting)...", last updated 23 June 2026 per the page.
  <https://www.newsguardtech.com/special-reports/ai-tracking-center/>
  Four criteria, all required: substantial AI-produced content; published without significant
  human oversight; presented so a reader would assume human writers; no clear AI disclosure.
  NewsGuard identifies sites by human review of these tells, **not** by detector scores alone
  (my reading of the method description; their full rating methodology was not opened).
  The count changes often - check the live page.

### A6. Hanley and Durumeric (Stanford) - measuring machine-generated news articles

- **Title:** "Machine-Made Media: Monitoring the Mobilization of Machine-Generated Articles on
  Misinformation and Mainstream News Websites"; Hans W. A. Hanley, Zakir Durumeric; arXiv 2023
  (rev. March 2024), comment field says "Accepted to ICWSM 2024" (proceedings not opened).
- **Link (verified):** <https://arxiv.org/abs/2305.09820>
- **Key numbers (abstract):** 15.46 million articles from 3,074 sites; Jan 2022 to May 2023 the
  relative share of synthetic articles rose about 57.3% on mainstream and about 474% on
  misinformation sites, driven by smaller, less popular sites. Note: this study itself uses a
  trained detector at **aggregate** level - fine for trends over millions of articles, not for a
  verdict on one site.

---

## Part B - Software vendor due diligence in procurement

### B1. CISA (with FBI branding) - Secure by Demand Guide

- **Title:** "Secure by Demand Guide: How Software Customers Can Drive a Secure Technology Ecosystem"
- **Organisation / year:** US Cybersecurity and Infrastructure Security Agency; PDF footer reads
  "As of August 2024" and carries CISA and FBI social handles (FBI co-branding seen, formal
  co-authorship not stated in the extracted text).
- **Links (verified):** page <https://www.cisa.gov/resources-tools/resources/secure-demand-guide>,
  PDF <https://www.cisa.gov/sites/default/files/2024-08/SecureByDemandGuide_080624_508c.pdf>
- **Why useful:** a free list of questions buyers should ask software makers before, during and
  after procurement. It says buyers' due diligence "often focus[es] on the enterprise security
  measures ... such as ... compliance standards" and adds product-security questions:
  - Vulnerability Disclosure and Reporting section: published vulnerability disclosure policy that
    authorises public testing; CVE records with correct CWE and CPE fields ("valuable even for SaaS").
  - Software supply chain: machine-readable SBOM including open-source dependencies.
  - Evidence of intrusions: security logs kept "for at least six months at no additional charge".
  - Authentication: SSO and MFA at no extra cost; no default passwords; easy patching / auto-update.

### B2. ENISA - Good Practices for Supply Chain Cybersecurity

- **Authors / org / date:** Maria Papaphilippou, Konstantinos Moulinos, Marianthi Theocharidou;
  European Union Agency for Cybersecurity (ENISA), June 2023 (web page dated 13 June 2023).
- **Links (verified):** <https://www.enisa.europa.eu/publications/good-practices-for-supply-chain-cybersecurity>,
  PDF <https://www.enisa.europa.eu/sites/default/files/publications/Good%20Practices%20for%20Supply%20Chain%20Cybersecurity.pdf>
- **Key numbers (survey of EU NIS-regulated organisations):**
  - Executive summary, PDF p.4 and Sect. 2 (Fig. 6), PDF p.12: "61 % require security certification
    from suppliers, 43% use security rating services and 37% demonstrate due diligence or risk
    assessments. Only 9 %" do not evaluate their supply chain.
  - PDF p.13: "security certifications might be expensive, especially for smaller providers".
  - PDF p.5 (citing ENISA's 2021 threat landscape): in 66 % of supply chain attacks analysed,
    suppliers "did not know, or were not transparent about, how they were compromised".
  - Sect. 3 tables point to ISO/IEC 27001:2022 and ISO/IEC 27002:2022 (5.19-5.23, supplier
    relationships) as reference standards.

### B3. UK Government - Assessing and Monitoring the Economic and Financial Standing of Bidders and Suppliers (2026)

- **Organisation:** UK Government commercial function; published in "The Sourcing and
  Consultancy Playbooks" collection on GOV.UK (collection page lists the Government Commercial
  Agency / Government Commercial Function; the note refers to the Cabinet Office Markets, Sourcing
  & Suppliers team). The PDF has no author line in the extracted text.
- **Version:** the PDF served on 2026-11-25 is titled "... – 2026" (file metadata: created
  February 2026; collection page says the note was replaced on 13 January 2026).
- **Links (verified):** collection page
  <https://www.gov.uk/government/publications/the-sourcing-and-consultancy-playbooks/assessing-and-monitoring-the-economic-and-financial-standing-of-suppliers-guidance-note-html>,
  PDF <https://assets.publishing.service.gov.uk/media/648c3d4f5f7bb7000c7fac06/EFS_Guidance_Note.pdf>
- **Key points:**
  - Sect. 2.4.7 (printed p.11): do not eliminate a bidder for "the lack of a credit rating ...
    alone; other financial ratios and/or metrics should also be considered".
  - Sect. 2.4.8 (printed p.11): credit scores (Dun & Bradstreet, Experian, Company Watch) depend on
    "backwards-looking published financial information which can be out of date"; use them "to
    corroborate other analysis", not as the sole measure.
  - Annex, Metric 1 Turnover Ratio (printed p.33): do not exclude "solely on the basis of the
    Turnover Ratio"; avoid "unfair barriers to smaller ... suppliers". Eight metrics in total
    (operating margin, net debt/EBITDA, quick ratio, net asset value, etc.).
  - Lists Companies House as a reference resource.

### Not verified (named for completeness, not opened in this session)

- NIST SP 800-161 Rev. 1 (Cybersecurity Supply Chain Risk Management) - not opened.
- RFC 9116 (security.txt) - known standard, not opened here; verify before citing.
- IAF CertSearch (ISO certificate lookup) and Companies House public API - not opened here;
  check coverage and terms before building on them.

---

## Signal table

| Signal or tell | Evidence (number, page/section) | How our agent could check it with free data | Risk of false alarm | Source |
|---|---|---|---|---|
| **AI-text detector score ("this page reads as AI-written")** | 61.22% average false positive rate on TOEFL essays (Results, PDF p.2); all 14 tools <80% accuracy, false positives 0-50% (Sect. 6); OpenAI classifier 26% TPR / 9% FPR, withdrawn 20 Jul 2023; paraphrasing defeats detectors | **Do not use as evidence.** At most log it internally; never show it as a reason. It also has no checkable link. | **High** - penalises plain or non-native writing; easy to evade | A1, A2, A3, A4 |
| Leftover chatbot phrases ("as an AI language model", "I cannot complete this prompt", "my knowledge cutoff") | All 49 sites in NewsGuard 2023 had at least one | Crawl the site (help center, blog, feature pages) and grep for a fixed phrase list; quote the page URL and the exact sentence | Low - but exclude pages that discuss AI or quote chatbots | A5 |
| Unfilled template placeholders ("[Your Name]", "[date]", "Lorem ipsum", "Company Name") | HistoryFact.in About page: "founded in [date] by [Your Name]" | Regex for bracketed placeholders and lorem ipsum on About, Imprint, Terms, Privacy, Careers; link the page | Low-medium - staging or unused pages exist on real sites | A5 |
| Legal pages from free generators | NewsGuard: About-Us and disclaimer generators | Detect generator footer strings or identical boilerplate; weak alone | **Medium-high** - many small real firms use generators | A5 |
| Generic or missing authors ("Admin", "Editor") on blog/help articles | NewsGuard 2023 | Read author fields / schema.org `author` on blog and help articles | Medium - many real help centers have no named authors | A5 |
| Team or author photos that are not authentic | NewsGuard: reverse image search showed fake profiles | No good free reverse-image API (my assessment); output a link for the user to run a reverse image search, plus check whether named people exist elsewhere (e.g. company registry officers) | Medium - stock photos on a team page are common on real sites | A5 |
| Contact email that cannot receive mail | 8 of 27 contacted sites had invalid addresses | DNS MX lookup on the contact domain (free, no email sent) | Low-medium - role addresses on another domain, catch-all setups | A5 |
| Content appears all at once on a young, small site | Synthetic articles rose ~474% on misinformation sites, mostly small sites (abstract) | Wayback Machine first-capture date vs. claimed founding year and article dates; sitemap `lastmod` spread. (Link from evidence to vendor sites is our inference.) | Medium - relaunches and site migrations look similar | A6 |
| Security certification claimed (ISO 27001, SOC 2) | 61% of surveyed EU organisations require supplier certification (PDF p.4, p.12) | Look for certificate number and issuing body on the trust page; check the certification body's public register where one exists; SOC 2 reports are private, so only presence of a trust page/report request flow can be checked | **High if absent** (certs expensive for small providers, PDF p.13); low if a claimed cert is missing from the issuer's register | B2 |
| No vulnerability-disclosure channel / security contact | CISA "Vulnerability Disclosure and Reporting" section | Fetch `/.well-known/security.txt` and a `/security` page; search CVE.org / NVD for the vendor name (free APIs) | Medium - many small honest vendors lack both; zero CVEs proves nothing on its own | B1 |
| Product security features claimed but not documented (SSO/MFA, logs, SBOM) | CISA: SSO/MFA at no extra cost; logs >= 6 months; SBOM | Check docs and pricing pages for these features; a feature page with no matching docs page is a mismatch to report | Medium - docs may sit behind login | B1 |
| Changelog / release notes with no real history | CISA asks about patching and updates (our extension to changelogs) | Compare changelog dates with Wayback captures of the changelog page; check the status page has a history of incidents | Medium - new products legitimately have short histories | B1 (indirect) |
| Company not in a registry, or registry details mismatch the site (name, address, age) | UK EFS lists Companies House as a resource; financial checks assume registered accounts | Query national registries (UK Companies House, German Handelsregister/Unternehmensregister, OpenCorporates free tier); compare legal name, address, incorporation date with the imprint | Low if not found anywhere with a clear legal name; medium for foreign or newly formed companies | B3 |
| Weak or missing financial data (no credit rating, small turnover) | EFS 2.4.7-2.4.8 (p.11), Annex Metric 1 (p.33): never exclude on this alone | Use only as context; filed accounts from registries; never a sole red flag | **High** - startups and small firms | B3 |
| Past breach and how the vendor handled it | 66% of supply-chain attacks: suppliers did not know or were not transparent (PDF p.5) | Search news and the vendor's own blog/status page for incident posts; check public breach lists (e.g. Have I Been Pwned breach list - not opened here) | Medium - no record may just mean no breach | B2 |

### Notes on limits

- All detector studies date from 2023-2025; tools have changed since. The direction (unreliable,
  biased, evadable) is consistent across independent groups, but exact rates may differ today.
- NewsGuard evidence is about news content farms, not SaaS vendor sites. Transferring the tells to
  vendor sites is our inference; it fits the brief's "help center nobody wrote" scenario but is not
  measured for SaaS.
- I am not certain about current coverage or terms of the free APIs named in the "how to check"
  column; verify each before building on it.
