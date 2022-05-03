from flask import Flask, render_template, redirect, request
import app as nighttimeAPI

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
        global caregiver
        caregiver = str(request.form.get("caregiver"))

        if request.form.get("pause"):
            nighttimeAPI.pauseMusic()

        if request.form.get("play"):
            nighttimeAPI.unpauseMusic()

        volLevel = request.form.get("volume")
        if volLevel:
            nighttimeAPI.adjustVolume(volLevel)

        text = request.form["text"]
        if text:
            nighttimeAPI.messages.append(text)

        if request.form.get("delete"):
            nighttimeAPI.messages.pop()

        if request.form.get("guidedBreathing"):
            nighttimeAPI.pauseBreathing()
        else:
            nighttimeAPI.resumeBreathing()

        if request.form.get("messages"):
            nighttimeAPI.pauseMessages()
        else:
            nighttimeAPI.resumeMessages()
    
    return render_template("setup.html")

@app.route("/templates/analytics")
def analytics_template():
    file = open(caregiver + ".txt", "r")
    dataFile = file.read()
    if (len(data) == 5):
        data = dataFile.split()
        return render_template("analytics.html", wakeups=data[0], avgWakeupTime=data[1], avgAwakeTime=data[2], stressLevels=data[3], workload=data[4])
    else:
        return render_template("analytics.html", wakeups=None, avgWakeupTime=None, avgAwakeTime=None, stressLevels=None, workload=None)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True, threaded=True)