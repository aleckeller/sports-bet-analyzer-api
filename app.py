from flask import Flask, request
from rq import Queue
from rq.job import Job
from worker import conn

import processor

app = Flask(__name__)
q = Queue(connection=conn)

@app.route('/')
def index():
    return "<h1>Revenge Game Generator!</h1>"

@app.route("/results/<job_id>", methods=["GET"])
def get_results(job_id):
    job = Job.fetch(job_id, connection=conn)
    status_code = 202
    response = {}
    if job.is_finished:
        result = job.result
        if result.get("error"):
            status_code = result["error"].get("code")
        else:
            status_code = 200
        response = result
    return response, status_code

@app.route("/games/", methods=["POST"])
def games_handler():
    json_body = request.get_json()
    job = q.enqueue(processor.process_games, json_body, False)
    response = {
        "id": job.get_id()
    }
    return response

@app.route("/revenge-games/", methods=["POST"])
def revenge_games_handler():
    json_body = request.get_json()
    job = q.enqueue(processor.process_games, json_body, True)
    response = {
        "id": job.get_id()
    }
    return response

if __name__ == '__main__':
    app.run(threaded=True, port=5000)