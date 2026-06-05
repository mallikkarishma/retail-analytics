import os
from datetime import datetime
from .config import Config


def write_audit_report(aisle_id: str, dwell_time_sec: float,
                       suspicious_frames: int, total_frames: int):
    """
    Writes an entry to a Markdown audit report
    when an aisle exceeds the maximum capacity threshold.
    """

    if dwell_time_sec < Config.AISLE_MAX_CAPACITY:
        return None

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report_date = datetime.now().strftime("%Y-%m-%d")
    report_path = os.path.join(Config.REPORTS_DIR, f"audit_{report_date}.md")

    # Create report file if it doesn't exist
    if not os.path.exists(report_path):
        with open(report_path, "w") as f:
            f.write(f"# Retail Audit Report — {report_date}\n\n")
            f.write("| Time | Aisle | Dwell Time | Suspicious Frames | Status |\n")
            f.write("|------|-------|------------|-------------------|--------|\n")

    # Append audit entry
    with open(report_path, "a") as f:
        f.write(f"| {timestamp} | {aisle_id} | {dwell_time_sec}s "
                f"| {suspicious_frames}/{total_frames} | 🚨 EXCEEDED THRESHOLD |\n")

    return report_path