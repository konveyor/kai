"""Add collection tables for grouping mined solutions

Revision ID: b7e2f4a1c3d9
Revises: a535c5759c14
Create Date: 2026-03-30 00:00:00.000000

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "b7e2f4a1c3d9"
down_revision: Union[str, None] = "a535c5759c14"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "kai_collections",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("source_repo", sa.String(), nullable=True),
        sa.Column("migration_type", sa.String(), nullable=True),
        sa.Column("metadata", sa.JSON(), nullable=False, server_default="{}"),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )

    op.create_table(
        "kai_collection_solution_association",
        sa.Column(
            "collection_id",
            sa.Integer(),
            sa.ForeignKey("kai_collections.id", ondelete="CASCADE", onupdate="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "solution_id",
            sa.Integer(),
            sa.ForeignKey("kai_solutions.id", ondelete="CASCADE", onupdate="CASCADE"),
            nullable=False,
        ),
    )

    op.create_table(
        "kai_collection_incident_association",
        sa.Column(
            "collection_id",
            sa.Integer(),
            sa.ForeignKey("kai_collections.id", ondelete="CASCADE", onupdate="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "incident_id",
            sa.Integer(),
            sa.ForeignKey("kai_incidents.id", ondelete="CASCADE", onupdate="CASCADE"),
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_table("kai_collection_incident_association")
    op.drop_table("kai_collection_solution_association")
    op.drop_table("kai_collections")
