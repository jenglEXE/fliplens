import requests
from backend.config import REVERB_KEY
from backend.integrations.base import normalize_listing

BASE_URL = 'https://api.reverb.com/api'
HEADERS = {
    'Authorization': f'Bearer {REVERB_KEY}',
    'Accept': 'application/hal+json',
    'Content-Type': 'application/hal+json',
    'Accept-Version': '3.0',
    'User-Agent': 'FlipLens/0.1'
}


def search(query: str, filters: dict = {}) -> list:
    if not REVERB_KEY:
        return []
    
    params = {
        'query': query,
        'per_page': 50,
        'page': 1
    }

    if filters.get('condition'):
        params['condition'] = filters['condition']

    try:
        response = requests.get(
            f'{BASE_URL}/listings/sold',
            headers=HEADERS,
            params=params
        )
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f'Reverb search error: {e}')
        return []
    
    listings = []
    for item in data.get('listings', []):
        try:
            price = item.get('price', {}).get('amount', 0)
            currency = item.get('price', {}).get('currency', 'USD')
            thumbnail = ''
            photos = item.get('photos', [])
            if photos:
                thumbnail = photos[0].get('_links', {}).get('thumbnail', {}).get('href', '')
            listing = normalize_listing(
                listing_id=item.get('id'),
                source='reverb',
                title=item.get('title', 'Unknown'),
                sold_price=price,
                currency=currency,
                sold_date=item.get('sold_at', ''),
                condition=item.get('condition', {}).get('display_name', 'Unknown'),
                url=item.get('_links', {}).get('web', {}).get('href', ''),
                thumbnail=thumbnail,
                category='Instruments'
            )
            listings.append(listing)
        except Exception as e:
            print(f'Reverb listing parse error: {e}')
            continue
    
    return listings