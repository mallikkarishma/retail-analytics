from flask import Blueprint, jsonify
from ..congestion import get_top_congested_aisles

congestion_bp = Blueprint("congestion", __name__)

@congestion_bp.route("/congestion", methods=["GET"])
def get_congestion():
    top_aisles = get_top_congested_aisles()
    return jsonify(top_aisles), 200