from flask import Flask, request, jsonify
from src.task import count_dna
from celery.result import AsyncResult
from src.celery_app import celery

app = Flask(__name__)

@app.route("/process", methods=["POST"])
def process_file():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    filepath = f"/data/{file.filename}"
    file.save(filepath)

    task = count_dna.delay(filepath)

    return jsonify({
        "message": "Task submitted",
        "task_id": task.id
    })


@app.route("/result/<task_id>", methods=["GET"])
def get_result(task_id):
    result = AsyncResult(task_id, app=celery)

    if result.state == "PENDING":
        return jsonify({"status": "pending"})

    elif result.state == "STARTED":
        return jsonify({"status": "processing"})

    elif result.state == "SUCCESS":
        return jsonify({
            "status": "success",
            "result": result.result
        })

    elif result.state == "FAILURE":
        return jsonify({
            "status": "failed",
            "error": str(result.result)
        })

    return jsonify({"status": result.state})