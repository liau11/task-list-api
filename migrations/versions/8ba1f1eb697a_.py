"""new columns, 

Revision ID: 8ba1f1eb697a
Revises: 
Create Date: 2023-05-04 22:10:32.824755

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "8ba1f1eb697a"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "goal",
        sa.Column("goal_id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("goal_id"),
    )
    op.create_table(
        "task",
        sa.Column("task_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=True),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("completed_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("task_id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("task")
    op.drop_table("goal")
    # ### end Alembic commands ###
