from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class User:
    id: str
    email: str
    password_hash: str
    tier: str #'free' or 'paid'
    created_at: datetime


@dataclass
class Search:
    id: str
    user_id: str
    query: str
    sources: list
    timestamp: datetime


@dataclass
class Listing:
    listing_id: str
    source: str
    title: str
    sold_price: float
    currency: str
    sold_date: datetime
    condition: str
    url: str
    thumbnail: str
    category: str
    id: Optional[str] = None


@dataclass
class PriceHistory:
    id:str
    listing_id: str
    price: float
    timestamp: datetime


@dataclass
class Favorite:
    id: str
    user_id: str
    listing_id: str
    favorited_at: datetime
    no_longer_available: Optional[datetime] = None


@dataclass
class Subscription:
    id: str
    user_id: str
    stripe_id: str
    status: str
    created_at: datetime
    cancelled_at: Optional[datetime] = None


@dataclass
class SearchResult:
    query: str
    listings: list
    average_price: float
    high_price: float
    low_price: float
    total_results: int
    sources: list
    cached: bool = False