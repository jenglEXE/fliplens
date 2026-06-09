# FlipLens — Project Notes

## Vision
A flipper's price research tool. Search any item and instantly see a
scatterplot of real sold prices from eBay, with average, high, and low
clearly marked. No AI verdict. No scan limits on paid tier. Just clean,
honest data to inform your own decision.

---

## Core Principles
- Never sell user data. Ever.
- No AI making decisions for users — raw data only.
- Scraping is a temporary bootstrap phase. Move to legitimate API access
  as soon as possible.
- Display only. We send traffic back to eBay, we don't hoard their data.
- Transparent privacy policy — visible and plain English, not buried in
  fine print.

---

## Tech Stack
- **Backend:** FastAPI (Python)
- **Database:** SQLite to start, migrate to PostgreSQL when needed
- **Cache:** Redis (aggressive caching — same search within 60 minutes
  serves cached result)
- **Data fetching:** Playwright (programmatic browser, not a scraper)
- **Desktop client:** PyQt6
- **Mobile app:** React Native (future)
- **Payments:** Stripe
- **Hosting:** Railway or Render (free tier to start)

---

## Data Sources
Priority order:
1. eBay sold listings — primary, publicly visible, no login required
2. Mercari sold listings — secondary, backup
3. Additional sources as legitimate API access becomes available

---

## Business Model
- **Free tier:** Limited searches per day
- **Paid tier:** $5/month subscription, unlimited searches, full features
- **eBay Partner Network:** Affiliate commissions on clickthroughs,
  zero cost to users
- No data selling. No ads. No exceptions.

---

## Revenue Philosophy
We monetize through subscriptions and affiliate commissions only.
Affiliate model actually aligns our interests with eBay's — we send
them high value repeat buyers and get compensated for it through their
own official program.

---

## Competitive Positioning
- FlipTip AI — closest competitor. AI verdict, scan limits, $9.99-$39.99/mo.
- Our differentiators:
  - No AI — raw data, user decides
  - No scan limits on paid tier
  - Scatterplot visualization of full price distribution
  - $5/month subscription (vs $9.99-$39.99/month for competitors)
  - Transparent data sourcing
  - No data selling ever
  - Desktop + mobile

---

## Legal Stance
- eBay sold listings are publicly visible to any unauthenticated user
- hiQ v. LinkedIn (9th Circuit, 2022) protects access to publicly
  available data
- We display data only — we do not resell or redistribute it
- We send traffic back to eBay — we are not a competitive threat
- ToS gray area acknowledged — move to legitimate API access ASAP
- At current scale, legal risk is essentially zero

---

## Long Game
1. Build the tool, get real users
2. Apply to eBay developer program with a working product and real
   user base
3. Pitch: "Our users are professional resellers — eBay's most valuable
   customers. We send you high volume repeat buyers."
4. Secure legitimate API access
5. Add more data sources as partnerships become available
6. Explore building own marketplace layer once leverage exists

---

## Build Order
1. Backend — FastAPI, SQLite, Redis, Playwright eBay fetcher,
   user auth, Stripe
2. Desktop client — PyQt6, talks to backend, personal use and testing
3. Mobile app — React Native, the real product
4. eBay Partner Network — apply once product is working

---

## Pre-Launch Checklist
- [ ] Set up proxy IP rotation for production server
- [ ] Set up proper PostgreSQL database
- [ ] Write plain English privacy policy
- [ ] Apply for eBay Partner Network
- [ ] Apply for eBay developer API access with pitch
- [ ] Set up error monitoring
- [ ] Load testing before going public
- [ ] Set up domain name

---

## Polish Items



---

## Future Features
- Photo search / image recognition for item lookup
- Saved search profiles
- Native bug reporting
- Hamburger menu (deferred from initial build)
- Profit calculator
- Inventory tracking
- Listing draft generator — based on sold data, suggests title,
  description, price, and starting bid. User copies and posts manually
  to any platform. No API required.
- "List on eBay" affiliate button — links to eBay listing creation
  page via eBay Partner Network affiliate URL. Earns commission while
  giving user a direct path to post.

---

## Decisions Log
- Dropped Chrome extension approach in favor of Python backend
- Dropped Facebook Marketplace (no public API, high ban risk)
- Dropped Craigslist (ToS too aggressive, legal risk)
- Dropped eBay API (denied, reapply with working product)
- Dropped Amazon (PA API requires affiliate sales quota, SP-API $1400/yr)
- Dropped Poshmark (no public API)
- Chose eBay sold listings as primary source — publicly visible,
  most trusted price reference in secondhand market
- Chose SQLite over PostgreSQL for initial build — cheaper, simpler,
  easy to migrate later
- Deferred proxy IP rotation to pre-launch phase
- Deferred mobile app to Phase 3 — backend first
- No AI features by design — this is a differentiator, not a limitation
- Dropped direct listing creation on external platforms — requires API
  access we don't have. Replaced with listing draft generator that
  user posts manually.