from flask import Blueprint, jsonify, abort, make_response, request
from app.models.task import Task
from app import db

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
