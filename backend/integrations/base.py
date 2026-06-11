from backend.models import Listing
from datetime import datetime


def normalize_listing(
        listing_id: str,
        source: str,
        title: str,
        sold_price: float,
        currency: str,
        sold_date: str,
        condition: str,
        url: str,
        thumbnail: str,
        category: str
) -> Listing:
    try:
        parsed_date = datetime.fromisoformat(sold_date)
    except Exception:
        parsed_date = datetime.now()

    return Listing(
        listing_id=str(listing_id),
        source=source,
        title=title,
        sold_price=float(sold_price) if sold_price else 0.0,
        currency=currency or 'USD',
        sold_date=parsed_date,
        condition=condition or 'Unknown',
        url=url or '',
        thumbnail=thumbnail or '',
        category=category or 'General'
    )