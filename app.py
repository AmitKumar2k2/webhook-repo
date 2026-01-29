from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from datetime import datetime
import json
import os
import logging
import pytz
from bson import ObjectId

# Logging 
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s: %(message)s'
)
logger = logging.getLogger(__name__)

# App 
app = Flask(__name__)

#MongoDB 
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(MONGO_URI)

db = client["github_webhooks"]
collection = db["events"]

# JSON Encoder
class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super().default(obj)

app.json_encoder = JSONEncoder

# Routes
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        logger.info("Webhook received")

        event_type = request.headers.get("X-GitHub-Event")
        logger.info(f"Event type: {event_type}")

        payload = request.get_json(silent=True)

        if not payload:
            return jsonify({"error": "No payload received"}), 400

        event_data = None

        if event_type == "push":
            event_data = process_push_event(payload)

        elif (
            event_type == "pull_request"
            and payload.get("action") == "closed"
            and payload.get("pull_request", {}).get("merged")
        ):
            event_data = process_merge_event(payload)

        elif event_type == "pull_request":
            event_data = process_pull_request_event(payload)

        if event_data:
            result = collection.insert_one(event_data)
            logger.info(f"Event stored: {result.inserted_id}")
            return jsonify({"status": "success"}), 200

        return jsonify({"status": "ignored"}), 200

    except Exception as e:
        logger.error(f"Webhook error: {e}")
        return jsonify({"error": str(e)}), 500


# Event Processors
def process_push_event(payload):
    try:
        return {
            "action": "push",
            "author": payload["head_commit"]["author"]["name"],
            "to_branch": payload["ref"].split("/")[-1],
            "from_branch": None,
            "timestamp": datetime.utcnow(),
            "request_id": payload["head_commit"]["id"],
        }
    except Exception as e:
        logger.error(f"Push event error: {e}")
        return None


def process_pull_request_event(payload):
    if payload.get("action") != "opened":
        return None

    try:
        pr = payload["pull_request"]
        return {
            "action": "pull_request",
            "author": pr["user"]["login"],
            "from_branch": pr["head"]["ref"],
            "to_branch": pr["base"]["ref"],
            "timestamp": datetime.utcnow(),
            "request_id": str(pr["id"]),
        }
    except Exception as e:
        logger.error(f"PR event error: {e}")
        return None


def process_merge_event(payload):
    try:
        pr = payload["pull_request"]
        return {
            "action": "merge",
            "author": pr["merged_by"]["login"],
            "from_branch": pr["head"]["ref"],
            "to_branch": pr["base"]["ref"],
            "timestamp": datetime.utcnow(),
            "request_id": str(pr["id"]),
        }
    except Exception as e:
        logger.error(f"Merge event error: {e}")
        return None


# API
@app.route("/api/events")
def get_events():
    try:
        events = list(
            collection.find()
            .sort("timestamp", -1)
            .limit(10)
        )

        for event in events:
            event["_id"] = str(event["_id"])

            if event.get("timestamp"):
                utc = event["timestamp"]
                if utc.tzinfo is None:
                    utc = pytz.utc.localize(utc)

                event["timestamp"] = (
                    utc.astimezone(pytz.timezone("Asia/Kolkata"))
                    .isoformat()
                )

        return jsonify(events)

    except Exception as e:
        logger.error(f"Fetch events error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    })


# Run
if __name__ == "__main__":
    collection.create_index([("timestamp", -1)])
    app.run(host="0.0.0.0", port=5000, debug=True)
