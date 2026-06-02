import httpx
from datetime import datetime, timezone

def get_free_games(country="IN") -> list[dict]:
    url = "https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions"
    params = {
        "locale": "en-US",
        "country": country,
        "allowCountries": country
    }
    
    with httpx.Client(timeout=15.0) as client:
        response = client.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
    elements = data.get("data", {}).get("Catalog", {}).get("searchStore", {}).get("elements", [])
    free_games = []
    
    now = datetime.now(timezone.utc)
    
    for el in elements:
        title = el.get("title")
        offer_id = el.get("id")
        namespace = el.get("namespace")
        slug = el.get("productSlug") or el.get("urlSlug")
        
        promotions = el.get("promotions")
        if not promotions or not isinstance(promotions, dict):
            continue
            
        active_promos = promotions.get("promotionalOffers")
        if not active_promos:
            continue
            
        for promo_wrapper in active_promos:
            offers = promo_wrapper.get("promotionalOffers", [])
            for offer in offers:
                discount_setting = offer.get("discountSetting", {})
                if discount_setting.get("discountPercentage") == 0:
                    start_date_str = offer.get("startDate")
                    end_date_str = offer.get("endDate")
                    
                    try:
                        start_date = datetime.fromisoformat(start_date_str.replace("Z", "+00:00")) if start_date_str else None
                        end_date = datetime.fromisoformat(end_date_str.replace("Z", "+00:00")) if end_date_str else None
                        
                        if start_date and end_date and start_date <= now <= end_date:
                            free_games.append({
                                "title": title,
                                "offer_id": offer_id,
                                "namespace": namespace,
                                "slug": slug,
                                "url": f"https://store.epicgames.com/en-US/p/{slug}"
                            })
                    except Exception as e:
                        print(f"Error parsing dates for {title}: {e}")
                        
    # Deduplicate by offer_id just in case
    seen = set()
    unique_games = []
    for game in free_games:
        if game["offer_id"] not in seen:
            seen.add(game["offer_id"])
            unique_games.append(game)
            
    return unique_games
