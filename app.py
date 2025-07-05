from flask import Flask, request, jsonify, render_template
from flask_pymongo import PyMongo
from datetime import datetime
import pytz

app = Flask(__name__)

# MongoDB connection
app.config["MONGO_URI"] = "mongodb+srv://abhi:abhi1234@cluster01.p75v2nc.mongodb.net/github_events?retryWrites=true&w=majority&appName=Cluster01"
mongo = PyMongo(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    event = request.headers.get('X-GitHub-Event')
    timestamp = datetime.utcnow().replace(tzinfo=pytz.UTC)
    formatted_time = timestamp.strftime('%d %B %Y - %I:%M %p UTC')

    message = None

    if event == 'push':
        author = data['pusher']['name']
        to_branch = data['ref'].split('/')[-1]
        message = f'"{author}" pushed to "{to_branch}" on {formatted_time}'

    elif event == 'pull_request':
        action = data['action']
        author = data['pull_request']['user']['login']
        from_branch = data['pull_request']['head']['ref']
        to_branch = data['pull_request']['base']['ref']

        if action in ['opened', 'reopened']:
            message = f'"{author}" submitted a pull request from "{from_branch}" to "{to_branch}" on {formatted_time}'
        elif action == 'closed' and data['pull_request']['merged']:
            message = f'"{author}" merged branch "{from_branch}" to "{to_branch}" on {formatted_time}'

    if message:
        mongo.db.events.insert_one({
            "message": message,
            "timestamp": timestamp
        })

    return jsonify({'status': 'received'}), 200

@app.route('/events')
def events():
    data = mongo.db.events.find().sort("timestamp", -1).limit(10)
    output = []
    for e in data:
        output.append({
            "_id": str(e["_id"]),
            "message": e["message"]
        })
    return jsonify(output)

import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Render will set PORT
    app.run(host='0.0.0.0', port=port)

