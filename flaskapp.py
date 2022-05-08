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
    if request.method=="POST":
        global caregiver
        caregiver = str(request.form.get("caregiver"))

        if request.form.get("pause"):
            nighttimeAPI.pauseMusic()
            return redirect("/templates/setup")

        if request.form.get("play"):
            nighttimeAPI.unpauseMusic()
            return redirect("/templates/setup")

        volLevel = request.form.get("volume")
        if volLevel:
            nighttimeAPI.adjustVolume(volLevel)
            return redirect("/templates/setup")

        text = request.form["add"]
        if text:
            nighttimeAPI.messages.append(text)
            return redirect("/templates/setup")

        if request.form.get("delete"):
            nighttimeAPI.messages.pop()
            return redirect("/templates/setup")

        if request.form.get("guidedBreathing"):
            nighttimeAPI.pauseBreathing()
            return redirect("/templates/setup")

        if not request.form.get("guidedBreathing"):
            nighttimeAPI.resumeBreathing()
            return redirect("/templates/setup")

        if request.form.get("messages"):
            nighttimeAPI.pauseMessages()
            return redirect("/templates/setup")

        if not request.form.get("messages"):
            nighttimeAPI.resumeMessages()
            return redirect("/templates/setup")

        return render_template("setup.html")

    else:
        return render_template("setup.html")

@app.route("/templates/analytics")
def analytics_template():
    data = [17, "01:37:43 AM", "14 minutes 21 seconds", "UP"]
    return render_template("analytics.html", wakeups=data[0], avgWakeupTime=data[1], avgAwakeTime=data[2], stressLevels=data[3])


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True, threaded=True)