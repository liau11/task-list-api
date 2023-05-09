from flask import Blueprint, jsonify, abort, make_response, request
import requests
from app.models.goal import Goal
from app import db


goals_bp = Blueprint("goals", __name__, url_prefix="/goals")


@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()

    try:
        new_goal = Goal.from_dict(request_body)
    except KeyError:
        return {"details": "Invalid data"}, 400

    db.session.add(new_goal)
    db.session.commit()

    return make_response({"goal": new_goal.to_dict()}, 201)


@goals_bp.route("", methods=["GET"])
def read_all_goals():
    sort_method = request.args.get("sort")

    if sort_method == "desc":
        goals = Goal.query.order_by(Goal.title.desc()).all()
    elif sort_method == "asc":
        goals = Goal.query.order_by(Goal.title.asc()).all()
    else:
        goals = Goal.query.all()

    return jsonify([goal.to_dict() for goal in goals])
