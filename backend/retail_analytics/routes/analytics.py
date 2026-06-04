from flask import Blueprint, jsonify
from ..data_science.traffic_analytics import get_peak_hours

analytics_bp = Blueprint("analytics", __name__)

@analytics_bp.route("/analytics/peak-hours", methods=["GET"])
def peak_hours():
    result = get_peak_hours()
    return jsonify(result), 200