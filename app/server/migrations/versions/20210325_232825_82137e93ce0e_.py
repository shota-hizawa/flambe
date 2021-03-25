"""empty message

Revision ID: 82137e93ce0e
Revises: 
Create Date: 2021-03-25 23:28:25.164987+09:00

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '82137e93ce0e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tasks',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('deleted', sa.BOOLEAN(), nullable=False, comment='論理削除フラグ'),
    sa.Column('created_at', mysql.DATETIME(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False, comment='登録日時'),
    sa.Column('updated_at', mysql.DATETIME(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False, comment='最終更新日時'),
    sa.Column('title', sa.String(length=255), nullable=False, comment='タイトル'),
    sa.Column('description', sa.String(length=255), nullable=True, comment='説明本文'),
    sa.Column('status', sa.Enum('TODO', 'DOING', 'DONE', name='status'), nullable=False, comment='ステータス'),
    sa.Column('priority', sa.Enum('HIGH', 'MEDIUM', 'LOW', name='priority'), nullable=False, comment='優先度'),
    sa.PrimaryKeyConstraint('id'),
    mysql_engine='InnoDB'
    )
    op.create_table('users',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('deleted', sa.BOOLEAN(), nullable=False, comment='論理削除フラグ'),
    sa.Column('created_at', mysql.DATETIME(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False, comment='登録日時'),
    sa.Column('updated_at', mysql.DATETIME(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False, comment='最終更新日時'),
    sa.Column('username', sa.String(length=255), nullable=False, comment='ユーザ名'),
    sa.Column('password_hash', sa.String(length=128), nullable=False, comment='パスワードのハッシュ値'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username'),
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    op.drop_table('tasks')
    # ### end Alembic commands ###
