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

@app.route('/addlink')
def addlinkpage():
    return render_template("addlink.html")

@app.route("/add-link", methods=["POST"])
def add_link():
    data = request.get_json()
    title = data["title"]
    description = data["description"]
    link = data["link"]
    with open("data.json", "r") as json_file:
        json_data = json.load(json_file)
    new_link = {"title": title, "description": description, "link": link}
    json_data.append(new_link)
    with open("data.json", "w") as json_file:
        json.dump(json_data, json_file)
    webhook_content = {
        "embeds": [{
            "color": 3066993,
            "fields": [{
                "name": "New Link Added",
                "value": f"Title: {title}\nDescription: {description}\nLink: {link}"
            }]
        }],
        "username": "Link Addition Bot"
    }
    result = requests.post(webhook, json=webhook_content)
    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    return "Link added successfully!"

@app.route('/report', methods=['POST'])
def report_link():
    data = json.loads(request.data)
    link_name = data["linkName"]
    link_description = data["linkDescription"]
    link_url = data["linkUrl"]

    # Send message to webhook
    webhook_content = {
        "embeds": [
            {
                "title": "Reported Link",
                "color": 16711680,
                "fields": [
                    {
                        "name": "Link Name",
                        "value": link_name
                    },
                    {
                        "name": "Link Description",
                        "value": link_description
                    },
                    {
                        "name": "Link URL",
                        "value": link_url
                    }
                ]
            }
        ],
        "username": "Report Bot"
    }
    result = requests.post(webhook, json=webhook_content)
    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    return jsonify({"message": "Link reported"}), 200

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