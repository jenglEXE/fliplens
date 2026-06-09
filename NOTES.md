# FlipLens — Project Notes

## Vision
A flipper's price research tool. Search any item by text or photo and 
instantly see a scatterplot of real sold prices across multiple 
marketplaces, with average, high, and low clearly marked. No AI verdict. 
No scan limits on paid tier. Just clean, honest data to inform your 
own decision.

---

## Core Principles
- Never sell user data. Ever.
- No AI making decisions for users — raw data only.
- Scraping is a temporary bootstrap phase. Move to legitimate API access
  as soon as possible.
- Display only. We send traffic back to source platforms, we don't 
  hoard their data.
- Transparent privacy policy — visible and plain English, not buried in
  fine print.

---

## Tech Stack
- **Backend:** FastAPI (Python)
- **Database:** Supabase (PostgreSQL)
- **Cache:** In-memory Python dictionary (upgrade to Redis when needed)
- **Data fetching:** Official APIs only (no scraping until necessary)
- **Desktop client:** PyQt6
- **Mobile app:** React Native (Phase 3)
- **Payments:** Stripe
- **Hosting:** Railway or Render (free tier to start)

---

## Data Sources
Priority order:
1. Discogs — music, vinyl, CDs (free, instant access, 60 req/min)
2. Reverb — musical instruments and gear (free, apply, flexible limits)
3. Etsy — vintage, antiques, handmade (free, apply, 10,000 req/day)
4. JustTCG — trading cards: Pokemon, MTG, Yu-Gi-Oh (free, instant, 
   20 results/call)
5. eBay — general marketplace (pursuing via Partner Network)

Note: As additional legitimate API access becomes available, sources 
will be added. Scraping is a last resort and temporary by design.

---

## API Application Status
- [ ] Discogs — apply immediately, instant approval
- [ ] Reverb — apply immediately, flexible approval
- [ ] Etsy — apply immediately, standard approval
- [ ] JustTCG — apply immediately, instant approval
- [ ] eBay Partner Network — apply once landing page is live
- [ ] eBay Developer API — apply once product has real users

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
Affiliate model aligns our interests with source platforms — we send
them high value repeat buyers and get compensated for it through their
own official programs.

---

## Competitive Positioning
- FlipTip AI — closest competitor. AI verdict, scan limits, 
  $9.99-$39.99/mo.
- Our differentiators:
  - No AI — raw data, the user decides
  - No scan limits on paid tier
  - Scatterplot visualization of full price distribution
  - Cross-marketplace aggregation (Discogs, Reverb, Etsy, JustTCG, eBay)
  - $5/month subscription (vs $9.99-$39.99/month for competitors)
  - Transparent data sourcing
  - No data selling ever
  - Desktop + mobile

---

## Legal Stance
- All current data sources use legitimate, official APIs
- No scraping at launch
- Display only — we do not resell or redistribute data
- We send traffic back to source platforms
- If eBay scraping becomes necessary as a temporary measure:
  - hiQ v. LinkedIn (9th Circuit, 2022) protects publicly available data
  - ToS gray area acknowledged — move to API access ASAP
  - At small scale, legal risk is essentially zero

---

## Long Game
1. Launch with Discogs, Reverb, Etsy, and JustTCG
2. Build user base — flippers across music, instruments, vintage, cards
3. Apply to eBay Partner Network with working product
4. Pitch eBay: "Our users are professional resellers — your most 
   valuable customers. We send you high volume repeat buyers."
5. Secure eBay API access
6. Add more data sources as partnerships become available
7. Explore proprietary marketplace layer once sufficient leverage exists

---

## Build Order
1. Landing page — needed for Partner Network applications
2. Backend — FastAPI, Supabase, in-memory cache, API integrations,
   user auth, Stripe
3. Desktop client — PyQt6, talks to backend, personal use and testing
4. Mobile app — React Native, the real product (Phase 3)
5. eBay Partner Network — apply once landing page is live

---

## Pre-Launch Checklist
- [ ] Set up proxy IP rotation for production server (if scraping needed)
- [ ] Write plain English privacy policy
- [ ] Apply for eBay Partner Network
- [ ] Apply for eBay developer API access with pitch
- [ ] Set up error monitoring
- [ ] Load testing before going public
- [ ] Set up domain name

---

## Polish Items
- Fix arrows for font size in settings
- Fix stop fetching button color visual feedback
- Implement NoScroll functions in search tab
- If applicable, implement pull-down menu for categories
- Fix buying format names if compatible with eBay API
- Put rounded white square inside free shipping and returns accepted
  checkboxes when ticked
- Change color of weekends in calendar popup for end date

---

## Future Features
- Photo search / image recognition for item identification
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
- Dropped eBay API initial attempt (denied, reapplying with product)
- Dropped Amazon (PA API requires affiliate sales quota, 
  SP-API $1,400/yr)
- Dropped Poshmark (no public API)
- Dropped Playwright/scraping at launch — unnecessary with legitimate 
  APIs available
- Dropped Redis in favor of in-memory Python cache — simpler, free, 
  sufficient for early scale
- Dropped SQLite in favor of Supabase (PostgreSQL) — hosted databases 
  persist across server deploys, file system storage does not
- Chose Discogs, Reverb, Etsy, JustTCG as launch data sources —
  legitimate APIs, strong flipper category coverage, zero legal risk
- Chose in-memory cache over Redis — free, zero setup, upgradeable later
- Deferred proxy IP rotation — only needed if scraping becomes necessary
- Deferred mobile app to Phase 3 — backend first
- No AI features by design — this is a differentiator, not a limitation
- Dropped direct listing creation on external platforms — requires API
  access we don't have. Replaced with listing draft generator that
  user posts manually.


- Request to your API
- Check cache
    - In chache: return
    - Check database
        - In database: return
        - Search ebay (BeautifulSoup)
            - Set cache
            - Set database
            - return


Think about shape of data