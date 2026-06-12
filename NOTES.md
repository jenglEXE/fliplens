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
   - Personal access token obtained ✅
   - Uses /database/search endpoint — returns catalog metadata, not
     marketplace pricing. sold_price is 0 for all results. Pricing
     fix deferred — need to investigate marketplace endpoint.
   - URLs fixed — now return full https://www.discogs.com/... links
2. Reverb — musical instruments and gear (free, personal token)
   - Personal access token obtained ✅
   - Switched from /listings/sold to /listings (active listings) —
     /listings/sold is seller-only, not a public search endpoint.
   - Returns active listing prices, not sold history. Noted as known
     limitation. sold_date uses created_at as fallback.
   - Accept-Version: 3.0 header required
3. Etsy — vintage, antiques, handmade
   - API key obtained, pending approval ✅
   - Returns 403 Forbidden until approval granted — expected behavior
   - Rate limit: 5 QPS, 5,000 QPD
4. JustTCG — trading cards: Pokemon, MTG, Yu-Gi-Oh
   - Active and working ✅
   - Auth uses X-API-Key header (not Bearer token)
   - Response structure: data[] → variants[] → price field
   - One listing created per variant (condition-specific pricing)
   - game param currently hardcoded to 'pokemon' — TODO: make dynamic
   - lastUpdated is Unix timestamp — converted to ISO datetime
5. eBay — general marketplace (pursuing via Partner Network)

---

## Known Issues / Parked
- Discogs sold_price always 0 — /database/search doesn't return 
  marketplace pricing. Need to investigate correct endpoint.
- Reverb returns active listings not sold history — known limitation,
  documented in code.
- JustTCG game param hardcoded to 'pokemon' — needs to be made
  dynamic based on query or search all games.
- Discogs thumbnails empty — not returned by /database/search.
- Server must be started from VS Code integrated terminal (venv 
  activates automatically). Run from fliplens root:
  python -m uvicorn backend.main:app --reload

---

## API Application Status
- [x] Discogs — personal access token obtained
- [x] Reverb — personal access token obtained
- [x] Etsy — key obtained, pending approval
- [x] JustTCG — active and working
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

## Current Build Status
### Backend (in progress)
- [x] config.py — environment variables, API keys, rate limit constants
- [x] cache.py — in-memory cache with normalize_key, get, set, 
      clear_expired, cache_size
- [x] database.py — Supabase singleton client via get_db()
- [x] models.py — dataclasses: User, Search, Listing, PriceHistory, 
      Favorite, Subscription, SearchResult
- [x] main.py — FastAPI app, CORS middleware, router registration, 
      background cache cleanup task
- [x] routers/search.py — GET /search/ with aggregation, stats, 
      caching, filtering, source selection. Fixed offset-naive vs
      offset-aware datetime sort bug.
- [x] routers/users.py — register, login, /me endpoint. JWT auth
      with bcrypt password hashing. Supabase schema set up.
- [x] routers/subscriptions.py — placeholder
- [x] integrations/base.py — normalize_listing() shared function
- [x] integrations/discogs.py — working, no pricing data yet
- [x] integrations/reverb.py — working, active listings only
- [x] integrations/etsy.py — 403 pending approval
- [x] integrations/justtcg.py — working, real prices, per-variant

### Still to build
- [ ] routers/subscriptions.py — Stripe integration
- [ ] routers/search.py — search history endpoint
- [ ] Landing page
- [ ] Desktop client (PyQt6)
- [ ] Mobile app (React Native) — Phase 3

---

## Pre-Launch Checklist
- [ ] Set up proxy IP rotation for production server (if scraping needed)
- [ ] Write plain English privacy policy
- [ ] Apply for eBay Partner Network
- [ ] Apply for eBay developer API access with pitch
- [ ] Set up error monitoring
- [ ] Load testing before going public
- [ ] Set up domain name
- [ ] Legal — Terms of Service, Privacy Policy, consider LLC formation

---

## Polish Items (Desktop Client)
- Fix arrows for font size in settings
- Fix stop fetching button color visual feedback
- Implement NoScroll functions in search tab
- If applicable, implement pull-down menu for categories
- Fix buying format names if compatible with eBay API
- Put rounded white square inside free shipping and returns 
  accepted checkboxes when ticked
- Change color of weekends in calendar popup for end date

---

## Future Features
- Photo search / image recognition for item identification
- Saved search profiles
- Native bug reporting
- Hamburger menu (deferred from initial build)
- Profit calculator
- Inventory tracking
- Listing draft generator
- "List on eBay" affiliate button
- Reverb pagination — currently fetches page 1 only
- Reverb HAL+JSON links — currently hardcoding URLs
- Books integration — waiting on eBay API access
- Redis cache — replace in-memory cache when multiple server 
  instances are needed
- Search history — per user search history endpoint
- Sneakers (StockX/GOAT) — no legitimate API, deferred
- Luxury watches (Chrono24) — no legitimate API, deferred
- JustTCG game param — make dynamic based on query or search all games
- Discogs pricing — investigate marketplace endpoint for real prices

---

## Decisions Log
- Dropped Chrome extension approach in favor of Python backend
- Dropped Facebook Marketplace (no public API, high ban risk)
- Dropped Craigslist (ToS too aggressive, legal risk)
- Dropped eBay API initial attempt (denied, reapplying with product)
- Dropped Amazon (PA API requires affiliate sales quota, SP-API $1,400/yr)
- Dropped Poshmark (no public API)
- Dropped Playwright/scraping at launch
- Dropped BeautifulSoup — unnecessary without scraping
- Dropped Redis in favor of in-memory Python cache
- Dropped SQLite in favor of Supabase (PostgreSQL)
- Discogs endpoint changed from /marketplace/search to /database/search
- Reverb switched from /listings/sold to /listings (active listings)
- JustTCG auth changed from Bearer token to X-API-Key header
- JustTCG response key is 'data' not 'cards'
- JustTCG prices live inside variants[] array, one per condition
- search.py sort fixed — strip tzinfo before comparing datetimes
- bcrypt pinned to 4.0.1 — newer versions incompatible with passlib
- Supabase schema created — all 6 tables live
- users.py auth complete — register, login, /me all working