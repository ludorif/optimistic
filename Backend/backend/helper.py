#  Copyright (c) 2025 Ludovic Riffiod
from datetime import datetime, timezone

def get_utc_day():
    return datetime.now(timezone.utc).strftime('%Y-%m-%d')