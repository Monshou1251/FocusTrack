from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool

from alembic import context

# Import your settings and Base model
from app.core.config import settings
from app.db.base import Base  # Your SQLAlchemy models should be imported here

# Load Alembic configuration
config = context.config

config.set_main_option(
    "sqlalchemy.url", settings.DATABASE_URL.replace("asyncpg", "psycopg2")
)

# Configure logging
if config.config_file_name:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata  # Ensure migrations recognize your models


def run_migrations_online():
    """Run migrations in 'online' mode with a synchronous engine."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,  # Detect column type changes
        )

        with context.begin_transaction():
            context.run_migrations()


run_migrations_online()
