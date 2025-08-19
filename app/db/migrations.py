from sqlalchemy import text

def ensure_sqlite_columns(engine):
    """Ensure newly added columns exist in SQLite without full migrations.
    Adds users.first_name and users.last_name if missing.
    Safe to run on every startup.
    """
    with engine.begin() as conn:
        # Check existing columns on users table
        result = conn.execute(text("PRAGMA table_info('users')"))
        cols = {row[1] for row in result.fetchall()}  # row[1] is name

        if 'first_name' not in cols:
            conn.execute(text("ALTER TABLE users ADD COLUMN first_name TEXT"))
        if 'last_name' not in cols:
            conn.execute(text("ALTER TABLE users ADD COLUMN last_name TEXT"))

        # Extend here for other new columns in future
