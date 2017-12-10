from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

import sys
import os.path

sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

from detect import predictor
from nsfw_score import nsfw_predictor
from fetch_youtube import fetcher


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/detect", methods=["GET"])
@cross_origin()
def detect ():
    headline = request.args.get("headline", "")
    clickbaitiness = predictor.predict(headline)
    return jsonify({ "clickbaitiness": round(clickbaitiness * 100, 2) })

@app.route("/nsfw", methods=["GET"])
@cross_origin()
def nsfw_score ():
    headline = request.args.get("url", "")
    porniness = nsfw_predictor.predict(headline)
    return jsonify({ "porniness": round(porniness * 100, 2) })

@app.route("/predictVid", methods=["GET"])
@cross_origin()
def predict_vid ():
    channelID = request.args.get("channelID", "")
    numWeeks = request.args.get("numWeeks","")
    clickbait = request.args.get('clickbait',"")
    porniness = request.args.get("porniness","")

    fetcher.get(channelID)
    y_pred = fetcher.predict(numWeeks,clickbait,porniness)
    return jsonify({ "views": round(y_pred,2) })

if __name__ == "__main__":
    app.run()
