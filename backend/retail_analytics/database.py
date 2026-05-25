import sqlite3
import os
from .config import Config

def get_connection():
    conn = sqlite3.connect(Config.DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS aisle_dwell_times (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            aisle_id        TEXT    NOT NULL,
            video_file      TEXT    NOT NULL,
            total_frames    INTEGER NOT NULL,
            suspicious_frames INTEGER NOT NULL,
            is_suspicious   INTEGER NOT NULL,
            dwell_time_sec  REAL    NOT NULL,
            recorded_at     TEXT    DEFAULT (datetime('now'))
        )
    ''')

    conn.commit()
    conn.close()

def insert_dwell_record(aisle_id, video_file, total_frames, 
                        suspicious_frames, is_suspicious, dwell_time_sec):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO aisle_dwell_times 
        (aisle_id, video_file, total_frames, suspicious_frames, is_suspicious, dwell_time_sec)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (aisle_id, video_file, total_frames, suspicious_frames, 
          int(is_suspicious), dwell_time_sec))

    conn.commit()
    conn.close()

def get_all_records():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM aisle_dwell_times ORDER BY recorded_at DESC')
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows