from fastapi import APIRouter, HTTPException, Query
from backend.cache import get_cached, set_cached
from backend.models import SearchResult
from backend.integrations import discogs, reverb, etsy, justtcg
import statistics

router = APIRouter()


def calculate_stats(listings: list) -> dict:
    prices = [l.sold_price for l in listings if l.sold_price > 0]
    if not prices:
        return {'average': 0, 'high': 0, 'low': 0}
    return {
        'average': round(statistics.mean(prices), 2),
        'high': max(prices),
        'low': min(prices)
    }


@router.get('/')
def search(
    q: str = Query(..., description='Search query'),
    condition: str = Query(None),
    min_price: float = Query(None),
    max_price: float = Query(None),
    sources: str = Query(None, description='Comma separated list of sources')
):
    if not q.strip():
        raise HTTPException(status_code=400, detail='Search query cannot be empty')

    filters = {}
    if condition:
        filters['condition'] = condition
    if min_price is not None:
        filters['min_price'] = min_price
    if max_price is not None:
        filters['max_price'] = max_price

    cached = get_cached(q, filters)
    if cached:
        cached.cached = True
        return cached

    active_sources = sources.split(',') if sources else ['discogs', 'reverb', 'etsy', 'justtcg']

    all_listings = []
    if 'discogs' in active_sources:
        all_listings += discogs.search(q, filters)
    if 'reverb' in active_sources:
        all_listings += reverb.search(q, filters)
    if 'etsy' in active_sources:
        all_listings += etsy.search(q, filters)
    if 'justtcg' in active_sources:
        all_listings += justtcg.search(q, filters)

    if min_price is not None:
        all_listings = [l for l in all_listings if l.sold_price >= min_price]
    if max_price is not None:
        all_listings = [l for l in all_listings if l.sold_price <= max_price]

    all_listings.sort(key=lambda l: l.sold_date.replace(tzinfo=None), reverse=True)

    stats = calculate_stats(all_listings)
    sources_used = list(set(l.source for l in all_listings))

    result = SearchResult(
        query=q,
        listings=all_listings,
        average_price=stats['average'],
        high_price=stats['high'],
        low_price=stats['low'],
        total_results=len(all_listings),
        sources=sources_used,
        cached=False
    )

    set_cached(q, filters, result)
    return result


@router.get('/history')
def history():
    return {'message': 'Search history coming soon'}