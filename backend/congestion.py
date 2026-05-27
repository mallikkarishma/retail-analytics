from .database import get_all_records

def get_congestion_level(dwell_time_sec, is_suspicious):
    if is_suspicious and dwell_time_sec >= 15:
        return "RED"
    elif is_suspicious and dwell_time_sec >= 10:
        return "YELLOW"
    else:
        return "GREEN"

def get_top_congested_aisles():
    records = get_all_records()

    # Get latest record per aisle
    latest = {}
    for record in records:
        aisle_id = record["aisle_id"]
        if aisle_id not in latest:
            latest[aisle_id] = record

    # Calculate congestion for each aisle
    congestion_data = []
    for aisle_id, record in latest.items():
        level = get_congestion_level(
            record["dwell_time_sec"],
            record["is_suspicious"]
        )
        congestion_data.append({
            "aisle_id"        : aisle_id,
            "dwell_time_sec"  : record["dwell_time_sec"],
            "suspicious_frames": record["suspicious_frames"],
            "is_suspicious"   : record["is_suspicious"],
            "congestion_level": level
        })

    # Sort by dwell time descending
    congestion_data.sort(key=lambda x: x["dwell_time_sec"], reverse=True)

    # Return top 3
    return congestion_data[:3]