import requests
from datetime import datetime
from backend.config import JUSTTCG_KEY
from backend.integrations.base import normalize_listing

BASE_URL = 'https://api.justtcg.com/v1'
HEADERS = {
    'X-API-Key': JUSTTCG_KEY,
    'User-Agent': 'FlipLens/0.1'
}


def search(query: str, filters: dict = {}) -> list:
    if not JUSTTCG_KEY:
        return []
    
    params = {
        'q': query,
        'limit': 20,
        'priceHistoryDuration': '30d',
        'game': 'pokemon' # TODO: make dynamic based on query or search all games
    }

    if filters.get('condition'):
        params['condition'] = filters['condition']
    
    try:
        response = requests.get(
            f'{BASE_URL}/cards',
            headers=HEADERS,
            params=params
        )
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f'JustTCG search error: {e}')
        return []
    
    listings = []
    for item in data.get('data', []):
        try:
            for variant in item.get('variants', []):
                price = variant.get('price', 0)
                last_updated = variant.get('lastUpdated', 0)
                sold_date = datetime.utcfromtimestamp(last_updated).isoformat() if last_updated else ''
                listing = normalize_listing(
                    listing_id=variant.get('id'),
                    source='justtcg',
                    title=item.get('name', 'Unknown'),
                    sold_price=price,
                    currency='USD',
                    sold_date=sold_date,
                    condition=variant.get('condition', 'Unknown'),
                    url=item.get('url', ''),
                    thumbnail=item.get('image', ''),
                    category='Trading Cards'
                )
                listings.append(listing)
        except Exception as e:
            print(f'JustTCG listing parse error: {e}')
            continue

    return listings