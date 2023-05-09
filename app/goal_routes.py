from flask import Blueprint, jsonify, abort, make_response, request
import requests
from app.models.goal import Goal
from app import db


goals_db = Blueprint("tasks", __name__, url_prefix="/goals")


@goals_db.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()

    try:
        new_goal = Goal.from_dict(request_body)
    except KeyError:
        return {"details": "Invalid data"}, 400

    db.session.add(new_goal)
    db.session.commit()

    return make_response({"goal": new_goal.to_dict()}, 201)
