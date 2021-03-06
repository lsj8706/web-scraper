from flask import Flask, render_template, request, redirect, send_file
from scrapper import get_jobs
from exporter import save_to_file
app = Flask("Super")

db = {}


@app.route('/')
def hello_world():
    return render_template("home.html")


@app.route('/report')
def report():
    word = request.args.get('word')
    if word:
        word = word.lower()
        existingJobs = db.get(word)
        if existingJobs:
            jobs = existingJobs
        else:
            jobs = get_jobs(word)
            db[word] = jobs
    else:
        return redirect("/")
    return render_template("report.html", searchingBy=word, resultsNumber=len(jobs), jobs=jobs)


# db에 있는 jobs들은 다운로드 할수 있도록 하는 루트
@app.route('/export')
def export():
    try:
        word = request.args.get('word')
        if not word:
            raise Exception()
        word = word.lower()
        jobs = db.get(word)
        if not jobs:
            raise Exception()
        save_to_file(jobs)
        return send_file("jobs.csv", mimetype="application/x-csv", attachment_filename="Jobs_search.csv", as_attachment=True)
    except:
        return redirect('/')


# @app.route("/<username>")
# def potato(username):
    # return f"hello {username} how are you doing!"
app.run(host="0.0.0.0")
