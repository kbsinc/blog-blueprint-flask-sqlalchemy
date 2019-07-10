from __future__ import with_statement

import os
import sys
# Include the project's folder on the system path.
sys.path.append(os.getcwd())

from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config#, pool

from blogexample.app import create_app, db
#from a2t.extensions import db


app = create_app()


# Include the project's folder on the system path.
sys.path.append(os.getcwd())

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# Get the SQLAlchemy database URI.
config.set_main_option('sqlalchemy.url', app.config['SQLALCHEMY_DATABASE_URI'])

# Required for --autogenerate to work so that Alembic can attempt to find
# the difference between the current database and our models automatically.

target_metadata = db.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    context.configure(url=app.config['SQLALCHEMY_DATABASE_URI'],
                      target_metadata=target_metadata, literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.')

    with connectable.connect() as connection:
        context.configure(
            url=app.config['SQLALCHEMY_DATABASE_URI'],
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()