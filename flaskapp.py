from flask import Flask, render_template, redirect, request
import app as nighttimeAPI

app = Flask(__name__, static_folder='assets')

# flask app functions
@app.route("/")
def home():
    return redirect("/templates/index")

@app.route("/templates/index")
def home_template():
    return render_template("index.html")

@app.route("/templates/setup", methods=['POST', 'GET'])
def setup_template():
    global caregiver
    global displayMes
    caregiver = str(request.form.get("caregiver"))

    if request.method == "POST":

        if "pause" in request.form:
            nighttimeAPI.pauseMusic()
            return render_template("setup.html")

        if "play" in request.form:
            nighttimeAPI.unpauseMusic()
            return render_template("setup.html")

        if "volume" in request.form:
            nighttimeAPI.adjustVolume(float(request.form.get("volume")))
            return render_template("setup.html")

        if "add" in request.form:
            text = request.form["text"]
            nighttimeAPI.addMessage(text)
            return render_template("setup.html")

        if "delete" in request.form:
            text = request.form["text"]
            nighttimeAPI.deleteMessage(text)
            return render_template("setup.html")

    else:

        if "messages" in request.form:
            nighttimeAPI.pauseMessages()
            return render_template("setup.html")

        if not "messages" in request.form:
            nighttimeAPI.resumeMessages()
            return render_template("setup.html")

    return render_template("setup.html")

@app.route("/templates/analytics")
def analytics_template():
    data = [17, "01:37:43 AM", "14 minutes 21 seconds", "UP"]
    return render_template("analytics.html", wakeups=data[0], avgWakeupTime=data[1], avgAwakeTime=data[2], stressLevels=data[3])


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True, threaded=True)