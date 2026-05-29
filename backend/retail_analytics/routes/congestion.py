from flask import Blueprint, jsonify, request
from ..congestion import get_top_congested_aisles

congestion_bp = Blueprint("congestion", __name__)

@congestion_bp.route("/congestion", methods=["GET"])
def get_congestion():
    session_id = request.args.get("session_id", None)
    top_aisles = get_top_congested_aisles(session_id)
    return jsonify(top_aisles), 200