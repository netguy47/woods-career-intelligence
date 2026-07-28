import math
import re
import json
import datetime
from typing import Dict, List, Any, Tuple, Optional

# Origin: Florissant, MO
ORIGIN_LAT = 38.7992
ORIGIN_LON = -90.3243
MAX_RADIUS_MILES = 35.0

# St. Louis Metro Geocoding Table (Lat, Lon)
STL_GEO_TABLE = {
    "florissant": (38.7992, -90.3243),
    "hazelwood": (38.7714, -90.3709),
    "ferguson": (38.7442, -90.3054),
    "spanish lake": (38.7984, -90.2721),
    "st. louis": (38.6270, -90.1994),
    "saint louis": (38.6270, -90.1994),
    "st louis": (38.6270, -90.1994),
    "clayton": (38.6426, -90.3237),
    "chesterfield": (38.6631, -90.5771),
    "creve coeur": (38.6645, -90.4357),
    "maryland heights": (38.7131, -90.4298),
    "st. charles": (38.7881, -90.4974),
    "saint charles": (38.7881, -90.4974),
    "st charles": (38.7881, -90.4974),
    "st. peters": (38.7676, -90.6279),
    "o'fallon": (38.8106, -90.6998),
    "wentzville": (38.8114, -90.8529),
    "kirkwood": (38.5834, -90.4068),
    "webster groves": (38.5925, -90.3554),
    "ballwin": (38.5945, -90.5482),
    "manchester": (38.5887, -90.5098),
    "edwardsville": (38.8114, -89.9532),
    "alton": (38.8906, -90.1843),
    "granite city": (38.7014, -90.1487),
    "belleville": (38.5201, -89.9840),
    "collinsville": (38.6703, -89.9845),
    "sauget": (38.5912, -90.1679),
    "cottleville": (38.7556, -90.6554),
    "lake st. louis": (38.7878, -90.7854),
    "arnold": (38.4328, -90.3776),
    "fenton": (38.5273, -90.4362),
    "eureka": (38.5026, -90.6404),
    "wildwood": (38.5828, -90.6629),
    "bridgeton": (38.7753, -90.4218),
    "overland": (38.6948, -90.3640),
    "berkeley": (38.7534, -90.3323)
}

def haversine_miles(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 3958.8  # Earth radius in miles
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def normalize_string(text: str) -> str:
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    return ' '.join(text.split())

def parse_date(date_val: Any) -> Tuple[Optional[datetime.datetime], str]:
    if not date_val:
        return None, "unknown"
    
    # Numeric timestamp (ms or s)
    if isinstance(date_val, (int, float)) or (isinstance(date_val, str) and date_val.isdigit()):
        val = float(date_val)
        if val > 1e11:  # milliseconds
            val /= 1000.0
        try:
            dt = datetime.datetime.fromtimestamp(val, tz=datetime.timezone.utc)
            return dt, "valid"
        except Exception:
            return None, "unknown"

    if isinstance(date_val, str):
        try:
            # ISO format parsing
            dt = datetime.datetime.fromisoformat(date_val.replace('Z', '+00:00'))
            return dt, "valid"
        except Exception:
            pass

    return None, "unknown"

def validate_location(location_str: Optional[str], is_remote: bool) -> Tuple[str, Optional[float], bool]:
    """
    Returns: (location_status, distance_miles, review_required)
    """
    if is_remote:
        return "remote_exempt", 0.0, False

    if not location_str or not location_str.strip():
        return "location_incomplete", None, True

    norm_loc = location_str.lower().strip()
    
    if "remote" in norm_loc:
        return "remote_exempt", 0.0, False

    # Try matching municipality
    matched_coords = None
    for city, coords in STL_GEO_TABLE.items():
        if city in norm_loc:
            matched_coords = coords
            break

    if not matched_coords:
        return "municipality_not_found", None, True

    dist = haversine_miles(ORIGIN_LAT, ORIGIN_LON, matched_coords[0], matched_coords[1])
    dist = round(dist, 2)

    if dist <= MAX_RADIUS_MILES:
        return "distance_verified", dist, False
    else:
        return "distance_out_of_range", dist, True

def process_job_record(record: Dict[str, Any], now_dt: datetime.datetime, max_hours_old: int = 168) -> Dict[str, Any]:
    # Support both datePosted and date_posted
    raw_date = record.get("datePosted") or record.get("date_posted")
    parsed_dt, date_status = parse_date(raw_date)

    within_window = False
    age_hours = None
    review_req = False

    if date_status == "unknown":
        review_req = True
    else:
        age_delta = now_dt - parsed_dt
        age_hours = round(age_delta.total_seconds() / 3600.0, 1)
        if age_hours <= max_hours_old:
            within_window = True
        else:
            within_window = False
            review_req = True

    # Location validation
    loc_str = record.get("location")
    is_remote = bool(record.get("isRemote") or record.get("is_remote"))
    loc_status, dist_miles, loc_review = validate_location(loc_str, is_remote)

    if loc_review:
        review_req = True

    post_processing = {
        "date_status": date_status,
        "parsed_date_iso": parsed_dt.isoformat() if parsed_dt else None,
        "age_hours": age_hours,
        "within_7_days": within_window,
        "location_status": loc_status,
        "distance_miles": dist_miles,
        "review_required": review_req,
        "exclusion_reasons": []
    }

    if not within_window and date_status != "unknown":
        post_processing["exclusion_reasons"].append(f"Exceeded max hours ({age_hours}h > {max_hours_old}h)")
    if loc_status == "distance_out_of_range":
        post_processing["exclusion_reasons"].append(f"Distance out of range ({dist_miles}mi > {MAX_RADIUS_MILES}mi)")

    # Preserve raw source data and attach decisions
    updated_record = dict(record)
    updated_record["post_processing"] = post_processing
    return updated_record

def jaccard_similarity(str1: str, str2: str) -> float:
    set1 = set(normalize_string(str1).split())
    set2 = set(normalize_string(str2).split())
    if not set1 or not set2:
        return 0.0
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    return len(intersection) / len(union)

def layered_deduplicate(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    unique_jobs: List[Dict[str, Any]] = []

    for item in records:
        url_direct = item.get("jobUrlDirect") or item.get("job_url_direct") or item.get("jobUrl") or item.get("job_url") or ""
        norm_company = normalize_string(item.get("company", ""))
        norm_title = normalize_string(item.get("title", ""))
        norm_loc = normalize_string(item.get("location", ""))
        sec_key = f"{norm_company}|{norm_title}|{norm_loc}"
        desc = item.get("description", "") or ""
        desc_prefix = desc[:200]
        site = item.get("site") or "unknown"

        matched = False
        for existing in unique_jobs:
            ex_url = existing.get("jobUrlDirect") or existing.get("job_url_direct") or existing.get("jobUrl") or existing.get("job_url") or ""
            ex_company = normalize_string(existing.get("company", ""))
            ex_title = normalize_string(existing.get("title", ""))
            ex_loc = normalize_string(existing.get("location", ""))
            ex_sec_key = f"{ex_company}|{ex_title}|{ex_loc}"
            ex_desc_prefix = (existing.get("description") or "")[:200]

            # Primary: URL match
            if url_direct and ex_url and url_direct == ex_url:
                matched = True
            # Secondary: Composite key match
            elif sec_key and ex_sec_key and sec_key == ex_sec_key:
                matched = True
            # Tertiary: Semantic string similarity
            elif norm_title and ex_title and jaccard_similarity(norm_title, ex_title) >= 0.80:
                if jaccard_similarity(desc_prefix, ex_desc_prefix) >= 0.70:
                    matched = True

            if matched:
                if "found_on_sources" not in existing["post_processing"]:
                    existing["post_processing"]["found_on_sources"] = [existing.get("site", "unknown")]
                if site not in existing["post_processing"]["found_on_sources"]:
                    existing["post_processing"]["found_on_sources"].append(site)
                break

        if not matched:
            item_copy = dict(item)
            if "post_processing" not in item_copy:
                item_copy["post_processing"] = {}
            item_copy["post_processing"]["found_on_sources"] = [site]
            unique_jobs.append(item_copy)

    return unique_jobs
