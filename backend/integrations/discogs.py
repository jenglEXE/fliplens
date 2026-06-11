import requests
from backend.config import DISCOGS_TOKEN
from backend.integrations.base import normalize_listing

BASE_URL = 'https://api.discogs.com'
HEADERS = {
    'Authorization': f'Discogs token={DISCOGS_TOKEN}',
    'User-Agent': 'FlipLens/0.1'
}


def search(query: str, filters:dict = {}) -> list:
    if not DISCOGS_TOKEN:
        return []
    
    params = {
        'q': query,
        'type': 'release',
        'per_page': 50,
        'page': 1
    }

    if filters.get('condition'):
        params['condition'] = filters['condition']
    
    try:
        response = requests.get(
            f'{BASE_URL}/marketplace/search',
            headers=HEADERS,
            params=params
        )
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f'Discogs search error: {e}')
        return []
    
    listings = []
    for item in data.get('results', []):
        try:
            listing = normalize_listing(
                listing_id=item.get('id'),
                source='discogs',
                title=item.get('title', 'Unknown'),
                sold_price=item.get('price', {}).get('value', 0),
                currency=item.get('price', {}).get('currency', 'USD'),
                sold_date=item.get('posted', ''),
                condition=item.get('condition', 'Unknown'),
                url=item.get('uri', ''),
                thumbnail=item.get('thumbnail', ''),
                category='Music'
            )
            listings.append(listing)
        except Exception as e:
            print(f'Discogs listing parse error: {e}')
            continue
    
    return listings
