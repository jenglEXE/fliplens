import requests
import time
from backend.config import ETSY_KEY
from backend.integrations.base import normalize_listing

BASE_URL = 'https://openapi.etsy.com/v3/application'
HEADERS = {
    'x-api-key': ETSY_KEY,
    'User-Agent': 'FlipLens/0.1'
}


def search(query: str, filters: dict = {}) -> list:
    if not ETSY_KEY:
        return []
    
    params = {
        'keywords': query,
        'limit': 50,
        'offset': 0,
        'sort_on': 'created',
        'sort_order': 'desc'
    }

    if filters.get('condition'):
        params['item_type'] = filters['condition']
    
    try:
        response = requests.get(
            f'{BASE_URL}/listings/active',
            headers=HEADERS,
            params=params
        )
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f'Etsy search error: {e}')
        return []
    
    listings = []
    for item in data.get('results', []):
        try:
            time.sleep(0.2)
            price = item.get('price', {}).get('amount', 0)
            divisor = item.get('price', {}).get('divisor', 100)
            currency = item.get('price', {}).get('currency_code', 'USD')
            actual_price = float(price) / float(divisor)

            images = item.get('images', [])
            thumbnail = images[0].get('url_170x135', '') if images else ''

            listing = normalize_listing(
                listing_id=item.get('listing_id'),
                source='etsy',
                title=item.get('title', 'Unknown'),
                sold_price=actual_price,
                currency=currency,
                sold_date=str(item.get('last_modified_tsz')),
                condition=item.get('item_type', 'Unknown'),
                url=item.get('url', ''),
                thumbnail=thumbnail,
                category=item.get('taxonomy_path', ['General'])[0] if item.get('taxonomy_path') else 'General'
            )
            listings.append(listing)
        except Exception as e:
            print(f'Etsy listing parse error: {e}')
            continue
    
    return listings