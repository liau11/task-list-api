from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    tasks = db.relationship("Task", back_populates="goal", lazy=True)

    def to_dict(self):
        goal_as_dict = {
            "id": self.goal_id,
            "title": self.title,
        }

        return goal_as_dict

    def to_dict_with_tasks(self):
        goal_as_dict = self.to_dict()
        goal_as_dict["tasks"] = [task.to_dict_with_goal_id() for task in self.tasks]

        return goal_as_dict

    def to_dict_with_tasks_and_goal(self):
        goal_as_dict = self.to_dict_with_tasks()
        goal_as_dict["goal_id"] = self.goal_id

        return goal_as_dict

    @classmethod
    def from_dict(cls, goal_data):
        new_goal = Goal(title=goal_data["title"])
        return new_goal
