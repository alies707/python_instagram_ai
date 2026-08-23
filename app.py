import os
from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv
from services.instagram import InstagramClient, InstagramAPIError

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "change-this-secret")


def get_client():
    return InstagramClient(
        access_token=os.getenv("INSTAGRAM_ACCESS_TOKEN", ""),
        api_version=os.getenv("META_GRAPH_API_VERSION", "v25.0"),
    )


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    try:
        client = get_client()
        account = client.get_account()
        media = client.get_media(limit=12)
        insights = client.get_account_insights()
        return render_template(
            "dashboard.html", account=account, media=media, insights=insights
        )
    except InstagramAPIError as exc:
        flash(str(exc), "error")
        return redirect(url_for("index"))


@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        client = get_client()
        media_id = request.form.get("media_id", "").strip()
        result = client.analyze_media(media_id)
        return render_template("analysis.html", result=result)
    except InstagramAPIError as exc:
        flash(str(exc), "error")
        return redirect(url_for("dashboard"))


if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG", "true").lower() == "true")
