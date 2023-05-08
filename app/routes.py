from flask import Blueprint, jsonify, abort, make_response, request
import requests
from app.models.task import Task
from app import db
from datetime import datetime
import os


tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    try:
        new_task = Task.from_dict(request_body)
    except KeyError:
        return {"details": "Invalid data"}, 400

    db.session.add(new_task)
    db.session.commit()

    return make_response({"task": new_task.to_dict()}, 201)


def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"message": f"Task {task_id} invalid"}, 400))

    task = Task.query.get(task_id)

    if not task:
        abort(make_response({"message": f"Task {task_id} not found"}, 404))

    return task


@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    sort_method = request.args.get("sort")

    if sort_method == "desc":
        tasks = Task.query.order_by(Task.title.desc()).all()
    elif sort_method == "asc":
        tasks = Task.query.order_by(Task.title.asc()).all()
    else:
        tasks = Task.query.all()

    return jsonify([task.to_dict() for task in tasks])


@tasks_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = validate_task(task_id)

    return make_response({"task": task.to_dict()}, 200)


@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_one_task(task_id):
    task = validate_task(task_id)

    request_body = request.get_json()

    for column, data in request_body.items():
        if column == "title":
            task.title = request_body["title"]
        elif column == "description":
            task.description = request_body["description"]
        elif column == "is_complete":
            task.is_complete == request_body["is_complete"]

    db.session.commit()

    return make_response({"task": task.to_dict()}, 200)


@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response(
        {"details": f'Task {task_id} "{task.title}" successfully deleted'},
        200,
    )


@tasks_bp.route("/<task_id>/<mark_completeness>", methods=["PATCH"])
def mark_complete(task_id, mark_completeness):
    task = validate_task(task_id)

    if mark_completeness == "mark_complete":
        task.completed_at = datetime.now()
    elif mark_completeness == "mark_incomplete":
        task.completed_at = None

    db.session.commit()

    print(task.title)
    response = requests.post(
        "https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer " + os.environ.get("SLACKBOT_TOKEN")},
        json={
            "channel": "task-notifications",
            "text": f"Someone just completed the task {task.title}",
        },
    )

    return make_response({"task": task.to_dict()}, 200)
