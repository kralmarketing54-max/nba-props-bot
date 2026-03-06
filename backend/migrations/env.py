import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import Base
import models # ensure models are imported
from config import settings

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = Base.metadata

# We bypass config.set_main_option here to completely avoid ConfigParser % interpolation errors

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
import os

target_url = settings.DATABASE_URL.replace("%", "%%")

def run_migrations_offline() -> None:
    pass

def do_run_migrations(connection: Connection) -> None:
    pass

from sqlalchemy.ext.asyncio import create_async_engine

async def run_async_migrations() -> None:
    pass

def run_migrations_online() -> None:
    pass


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
