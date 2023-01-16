import json
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

with open("config.json") as f:
    config = json.load(f)

webhook = config["webhook"]

@app.route('/')
def home():
    with open('data.json') as json_file:
        data = json.load(json_file)
    return render_template("index.html", websites=data)

@app.route('/contact')
def contactpage():
    return render_template("contact.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/contact', methods=['POST'])
def contact():
    data = json.loads(request.data)
    try:
        webhookcontent = {
            "embeds": [{
                "title": data["subject"],
                "description": data["message"],
                "fields": [
                    {
                        "name": "Username",
                        "value": data["username"]
                    },
                    {
                        "name": "Email",
                        "value": data["email"]
                    }
                ]
            }],
            "username": "Feedback Bot"
        }
        result = requests.post(webhook, json=webhookcontent)
        try:
            result.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print(err)
        return jsonify({"message": "Form submitted"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)