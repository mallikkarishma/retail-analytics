import requests
import json
import os
from datetime import datetime
from ..config import Config
from ..data_science.traffic_analytics import get_peak_hours


def generate_executive_report():
    # Get analytics data
    analytics = get_peak_hours()

    if "error" in analytics:
        return {"error": "No data available to generate report"}

    # Build summary for the AI
    summary = f"""
    Retail Store Daily Analytics Summary:
    
    - Peak Hour: {analytics['peak_hour_label']}
    - Hourly Breakdown:
    """

    for hour in analytics["hourly_data"]:
        summary += f"\n    - {hour['hour']:02d}:00 — {hour['total_records']} records, avg dwell: {hour['avg_dwell_time']}s, suspicious: {int(hour['suspicious_count'])}"

    # Call Groq API
    headers = {
        "Authorization": f"Bearer {Config.GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {
                "role": "system",
                "content": "You are a retail store analytics assistant. Generate a concise professional end-of-day business report in Markdown format."
            },
            {
                "role": "user",
                "content": f"Based on this data, generate an end-of-day retail store report:\n{summary}"
            }
        ],
        "max_tokens": 500
    }

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers=headers,
        json=payload
    )

    if response.status_code != 200:
        return {"error": f"Groq API error: {response.text}"}

    report_text = response.json()["choices"][0]["message"]["content"]

    # Save report to file
    report_date = datetime.now().strftime("%Y-%m-%d")
    report_path = os.path.join(Config.REPORTS_DIR, f"executive_report_{report_date}.md")

    with open(report_path, "w") as f:
        f.write(f"# Executive Report — {report_date}\n\n")
        f.write(report_text)

    return {
        "report_path": report_path,
        "report"     : report_text
    }