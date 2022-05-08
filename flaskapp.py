import re
from flask import Flask, render_template, redirect, request
import app as nighttimeAPI

app = Flask(__name__, static_folder='assets')

@app.route("/")
def home():
    return redirect("/templates/index")

@app.route("/templates/index")
def home_template():
    return render_template("index.html")

@app.route("/templates/setup", methods=['POST', 'GET'])
def setup_template():
    # get messages to display
    displayMes = ""
    for mes in nighttimeAPI.messages:
        displayMes += (mes + "\n")

    global caregiver
    caregiver = str(request.form.get("caregiver"))

    if "pause" in request.method:
        nighttimeAPI.pauseMusic()
        return render_template("setup.html", messages=displayMes)

    if "play" in request.method:
        nighttimeAPI.unpauseMusic()
        return render_template("setup.html", messages=displayMes)

    if "volume" in request.method:
        nighttimeAPI.adjustVolume(request.form.get("volume"))
        return render_template("setup.html", messages=displayMes)

    if "add" in request.method:
        print("added")
        text = request.form["text"]
        nighttimeAPI.messages.append(text)
        return render_template("setup.html", messages=displayMes)

    if "delete" in request.method:
        nighttimeAPI.messages.pop()
        return render_template("setup.html", messages=displayMes)

    if "messages" in request.method:
        nighttimeAPI.pauseMessages()
        return render_template("setup.html", messages=displayMes)

    if not "messages" in request.method:
        nighttimeAPI.resumeMessages()
        return render_template("setup.html", messages=displayMes)

    return render_template("setup.html", messages=displayMes)

@app.route("/templates/analytics")
def analytics_template():
    data = [17, "01:37:43 AM", "14 minutes 21 seconds", "UP"]
    return render_template("analytics.html", wakeups=data[0], avgWakeupTime=data[1], avgAwakeTime=data[2], stressLevels=data[3])


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True, threaded=True)