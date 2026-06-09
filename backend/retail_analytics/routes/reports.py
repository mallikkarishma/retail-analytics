import os
from flask import Blueprint, jsonify
from ..config import Config
from ..data_science.vlm_report import generate_executive_report

reports_bp = Blueprint("reports", __name__)

@reports_bp.route("/reports/executive", methods=["GET"])
def executive_report():
    result = generate_executive_report()
    return jsonify(result), 200

@reports_bp.route("/reports/list", methods=["GET"])
def list_reports():
    files = os.listdir(Config.REPORTS_DIR)
    md_files = [f for f in files if f.endswith(".md")]
    md_files.sort(reverse=True)

    reports = []
    for f in md_files:
        path = os.path.join(Config.REPORTS_DIR, f)
        with open(path, "r") as file:
            content = file.read()
        reports.append({
            "filename": f,
            "content" : content
        })

    return jsonify(reports), 200