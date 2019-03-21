"""empty message

Revision ID: 46a23623cd75
Revises: 
Create Date: 2019-03-20 10:30:22.229526

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '46a23623cd75'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('items')
    op.drop_table('users')
    op.drop_table('categories')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('categories',
                    sa.Column('id', mysql.INTEGER(display_width=11),
                              autoincrement=True,
                              nullable=False),
                    sa.Column('name',
                              mysql.VARCHAR(length=500),
                              nullable=True),
                    sa.PrimaryKeyConstraint('id'),
                    mysql_default_charset=u'latin1',
                    mysql_engine=u'InnoDB'
                    )
    op.create_table('users',
                    sa.Column('id', mysql.INTEGER(display_width=11),
                              autoincrement=True,
                              nullable=False),
                    sa.Column('username',
                              mysql.VARCHAR(length=500),
                              nullable=True),
                    sa.Column('password',
                              mysql.VARCHAR(length=500),
                              nullable=True),
                    sa.PrimaryKeyConstraint('id'),
                    mysql_default_charset=u'latin1',
                    mysql_engine=u'InnoDB'
                    )
    op.create_table('items',
                    sa.Column('id',
                              mysql.INTEGER(display_width=11),
                              autoincrement=True,
                              nullable=False),
                    sa.Column('title',
                              mysql.VARCHAR(length=500),
                              nullable=True),
                    sa.Column('description',
                              mysql.VARCHAR(length=5000),
                              nullable=True),
                    sa.Column('cat_id',
                              mysql.INTEGER(display_width=11),
                              autoincrement=False,
                              nullable=True),
                    sa.Column('user_id',
                              mysql.INTEGER(display_width=11),
                              autoincrement=False,
                              nullable=True),
                    sa.ForeignKeyConstraint(['cat_id'], [u'categories.id'],
                                            name=u'items_ibfk_1',
                                            ondelete=u'CASCADE'),
                    sa.ForeignKeyConstraint(['user_id'], [u'users.id'],
                                            name=u'items_ibfk_2',
                                            ondelete=u'CASCADE'),
                    sa.PrimaryKeyConstraint('id'),
                    mysql_default_charset=u'latin1',
                    mysql_engine=u'InnoDB'
                    )
    # ### end Alembic commands ###