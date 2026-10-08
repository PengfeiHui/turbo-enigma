"""add account field to users

Revision ID: add_account_field
Revises:
Create Date: 2024-10-08

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_account_field'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # 添加 account 字段（允许为 NULL，稍后填充数据）
    op.add_column('users', sa.Column('account', sa.String(length=11), nullable=True))

    # 为现有用户生成账号（使用 user_id + 随机数生成）
    # 注意：实际执行时需要根据具体情况调整
    op.execute("""
        UPDATE users
        SET account = LPAD(CAST((id + 10000000000) AS TEXT), 11, '0')
        WHERE account IS NULL
    """)

    # 设置 account 为非空
    op.alter_column('users', 'account', nullable=False)

    # 创建唯一索引
    op.create_index('ix_users_account', 'users', ['account'], unique=True)

    # 移除 username 的唯一约束（允许重复昵称）
    op.drop_index('ix_users_username', table_name='users')
    op.create_index('ix_users_username', 'users', ['username'], unique=False)


def downgrade():
    # 回滚操作
    op.drop_index('ix_users_account', table_name='users')
    op.drop_column('users', 'account')

    # 恢复 username 唯一约束
    op.drop_index('ix_users_username', table_name='users')
    op.create_index('ix_users_username', 'users', ['username'], unique=True)
