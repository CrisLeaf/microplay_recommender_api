import pandas as pd
from flask import Flask, request, jsonify
from recommendations import Recommender


app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return """Home"""

@app.route("/train", methods=["GET"])
def train():
    df = pd.read_csv("train_data.csv")

    global reco
    reco = Recommender(df)
    reco.train()

    return """Model trained."""

@app.route("/reco", methods=["GET"])
def get_results():
    train() #
    requested_url = request.args.get("url")
    recommendations = reco.recommend(requested_url)

    return jsonify({"recommendations": recommendations.tolist()})

if __name__ == "__main__":
    app.run(debug=True)
