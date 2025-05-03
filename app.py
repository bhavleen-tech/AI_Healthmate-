from flask import Flask, render_template
from routes.travel_health import travel_health_bp

app = Flask(__name__)
app.register_blueprint(travel_health_bp)

# ✅ Travel Health page
@app.route("/travel-health")
def travel_health_page():
    return render_template("travel_health.html")

# ✅ Homepage route
@app.route("/")
def home():
    return render_template("index.html")

# ✅ Custom 404 error handler
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

if __name__ == '__main__':
    app.run(host='127.0.0.3', port=2000, debug=True)
