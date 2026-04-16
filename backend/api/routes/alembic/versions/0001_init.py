"""init"""

from alembic import op
import sqlalchemy as sa


revision = "0001_init"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Версионирование БД
    op.create_table(
        "request_logs",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("task_id", sa.String(length=64), nullable=False, unique=True, index=True),
        sa.Column("prompt", sa.Text(), nullable=False),
        sa.Column("creativity", sa.Float(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="queued"),
        sa.Column("result", sa.Text(), nullable=True),
        sa.Column("error", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("NOW()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("NOW()"), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("request_logs")
