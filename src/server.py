from flask import Flask, jsonify, request
from detect import predictor
from nsfw_score import nsfw_predictor


app = Flask(__name__)

@app.route("/detect", methods=["GET"])
def detect ():
    headline = request.args.get("headline", "")
    clickbaitiness = predictor.predict(headline)
    return jsonify({ "clickbaitiness": round(clickbaitiness * 100, 2) })

@app.route("/nsfw", methods=["GET"])
def nsfw_score ():
    headline = request.args.get("url", "")
    porniness = nsfw_predictor.predict(headline)
    return jsonify({ "porniness": round(porniness * 100, 2) })

if __name__ == "__main__":
    app.run()
