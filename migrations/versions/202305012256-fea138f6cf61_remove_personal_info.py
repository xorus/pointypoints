"""remove personal info

Revision ID: fea138f6cf61
Revises: d0af3fd39346
Create Date: 2023-05-01 22:56:57.102871

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fea138f6cf61'
down_revision = 'd0af3fd39346'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    # op.alter_column('users', 'display_name',
    #            existing_type=sa.VARCHAR(),
    #            nullable=True)
    # ### end Alembic commands ###
    op.execute('''create table users_dg_tmp
                (
                    id                CHAR(32) not null
                        primary key,
                    display_name      VARCHAR,
                    profile_image_url VARCHAR,
                    date              DATETIME not null,
                    twitch_id         VARCHAR  not null,
                    token             VARCHAR  not null
                );
                ''')
    op.execute('''insert into users_dg_tmp(id, display_name, profile_image_url, date, twitch_id, token)
                select id, display_name, profile_image_url, date, twitch_id, token
                from users;
                ''')
    op.execute('drop table users;')
    op.execute('alter table users_dg_tmp rename to users;')
    op.execute('create index ix_users_date    on users (date);')
    op.execute('create index ix_users_id on users (id)')
    op.execute('create index ix_users_token on users (token)')


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    # op.alter_column('users', 'display_name',
    #            existing_type=sa.VARCHAR(),
    #            nullable=False)
    # ### end Alembic commands ###
    op.execute('''create table users_dg_tmp
                (
                    id                CHAR(32) not null
                        primary key,
                    display_name      VARCHAR not null,
                    profile_image_url VARCHAR,
                    date              DATETIME not null,
                    twitch_id         VARCHAR  not null,
                    token             VARCHAR  not null
                );
                ''')
    op.execute('''insert into users_dg_tmp(id, display_name, profile_image_url, date, twitch_id, token)
                select id, display_name, profile_image_url, date, twitch_id, token
                from users;
                ''')
    op.execute('drop table users;')
    op.execute('alter table users_dg_tmp rename to users;')
    op.execute('create index ix_users_date    on users (date);')
    op.execute('create index ix_users_id on users (id)')
    op.execute('create index ix_users_token on users (token)')