import pandas as pd
from flask import Blueprint, request, jsonify
from .recommender_bot import Recommender

bp = Blueprint("recommender_app", __name__, url_prefix="/")

@bp.route("/", methods=["GET"])
def home():
    return """Home"""

@bp.route("/train", methods=["GET"])
def train():
    df = pd.read_csv("train_data.csv")

    global reco
    reco = Recommender(df)
    reco.train()

    return """Model trained."""

@bp.route("/list", methods=["GET"])
def list():
    names_list = pd.read_csv("train_data.csv")["name_original"].values

    return jsonify({"names": names_list.tolist()})

@bp.route("/reco", methods=["GET"])
def get_results():
    train()
    requested_url = request.args.get("url")
    recommendations = reco.recommend(requested_url)

    return jsonify({"recommendations": recommendations.tolist()})
