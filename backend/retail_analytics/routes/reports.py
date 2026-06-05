from flask import Blueprint, jsonify
from ..data_science.vlm_report import generate_executive_report

reports_bp = Blueprint("reports", __name__)

@reports_bp.route("/reports/executive", methods=["GET"])
def executive_report():
    result = generate_executive_report()
    return jsonify(result), 200