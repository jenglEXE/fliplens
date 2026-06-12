import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY', 'changeme')
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 1440 #24 hours

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')

DISCOGS_TOKEN = os.getenv('DISCOGS_TOKEN')
JUSTTCG_KEY = os.getenv('JUSTTCG_KEY')
REVERB_KEY = os.getenv('REVERB_KEY')
ETSY_KEY = os.getenv('ETSY_KEY')
EBAY_CLIENT_ID = os.getenv('EBAY_CLIENT_ID')
EBAY_CLIENT_SECRET = os.getenv('EBAY_CLIENT_SECRET')
ETSY_SECRET = os.getenv('ETSY_SECRET')

FREE_TIER_DAILY_LIMIT = 10

