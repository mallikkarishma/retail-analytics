import pandas as pd
import sqlite3
from ..config import Config

def get_peak_hours():
    conn = sqlite3.connect(Config.DB_PATH)
    
    df = pd.read_sql_query("""
        SELECT * FROM aisle_dwell_times
    """, conn)
    conn.close()

    if df.empty:
        return {"error": "No data available yet"}

    # Convert recorded_at to datetime
    df["recorded_at"] = pd.to_datetime(df["recorded_at"])
    df["hour"] = df["recorded_at"].dt.hour

    # Count activity per hour
    hourly = df.groupby("hour").agg(
        total_records     = ("id", "count"),
        avg_dwell_time    = ("dwell_time_sec", "mean"),
        suspicious_count  = ("is_suspicious", "sum")
    ).reset_index()

    hourly["avg_dwell_time"] = hourly["avg_dwell_time"].round(2)

    # Find peak hour
    peak_hour = hourly.loc[hourly["total_records"].idxmax(), "hour"]

    return {
        "peak_hour"   : int(peak_hour),
        "peak_hour_label": f"{int(peak_hour):02d}:00 - {int(peak_hour)+1:02d}:00",
        "hourly_data" : hourly.to_dict(orient="records")
    }