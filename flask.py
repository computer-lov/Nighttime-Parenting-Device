from flask import Flask, render_template, redirect, request
import nighttimeParenting as np

app = Flask(__name__, static_folder='assets')

@app.route("/")
def home():
    return redirect("/templates/index")

@app.route("/templates/index")
def home_template():
    return render_template("index.html")

@app.route("/templates/input", methods=['POST', 'GET'])
def setup_template():
    if request.method=="POST":
        text = request.form['text']
    
    return render_template("setup.html")

@app.route("/templates/analytics")
def analytics_template():
    return render_template("analytics.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True, threaded=True)