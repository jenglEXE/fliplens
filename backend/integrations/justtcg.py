import requests
from backend.config import JUSTTCG_KEY
from backend.integrations.base import normalize_listing

BASE_URL = 'https://api.justtcg.com/v1'
HEADERS = {
    'Authorization': f'Bearer {JUSTTCG_KEY}',
    'User-Agent': 'FlipLens/0.1'
}


def search(query: str, filters: dict = {}) -> list:
    if not JUSTTCG_KEY:
        return []
    
    params = {
        'q': query,
        'limit': 20,
        'priceHistoryDuration': '30d'
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
    for item in data.get('cards', []):
        try:
            price = item.get('marketPrice') or item.get('price', 0)
            listing = normalize_listing(
                listing_id=item.get('id'),
                source='justtcg',
                title=item.get('name', 'Unknown'),
                sold_price=price,
                currency='USD',
                sold_date=item.get('updatedAt', ''),
                condition=item.get('condition', 'Unknown'),
                url=item.get('url', ''),
                thumbnail=item.get('imageUrl', ''),
                category='Trading Cards'
            )
            listings.append(listing)
        except Exception as e:
            print(f'JustTCG listing parse error: {e}')
            continue

    return listings