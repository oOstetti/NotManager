import sqlite3
from contextlib import contextmanager
from pathlib import Path


DATA_DIR = (
    Path.home()
    / "AppData"
    / "Local"
    / "GestorNotificacoes"
)

DATABASE_PATH = DATA_DIR / "notificacoes.db"


@contextmanager
def connect():
    """Abre a conexão, controla a transação e fecha ao terminar."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row

    try:
        with connection:
            yield connection
    finally:
        connection.close()


def initialize_database():
    with connect() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS notifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                identification TEXT NOT NULL,
                title TEXT NOT NULL,
                observation TEXT NOT NULL DEFAULT '',
                status TEXT NOT NULL DEFAULT 'em_andamento',
                created_at TEXT NOT NULL DEFAULT (
                    strftime('%Y-%m-%dT%H:%M:%SZ', 'now')
                )
            )
        """)


def create_notification(identification, title, observation):
    with connect() as connection:
        cursor = connection.execute(
            """
            INSERT INTO notifications (
                identification,
                title,
                observation
            )
            VALUES (?, ?, ?)
            """,
            (identification, title, observation),
        )

        return cursor.lastrowid


def list_notifications():
    with connect() as connection:
        return connection.execute("""
            SELECT
                id,
                identification,
                title,
                observation,
                status,
                created_at
            FROM notifications
            ORDER BY id DESC
        """).fetchall()


def get_notification(notification_id):
    with connect() as connection:
        return connection.execute(
            """
            SELECT
                id,
                identification,
                title,
                observation,
                status,
                created_at
            FROM notifications
            WHERE id = ?
            """,
            (notification_id,),
        ).fetchone()


def update_notification(
    notification_id,
    identification,
    title,
    observation,
):
    with connect() as connection:
        connection.execute(
            """
            UPDATE notifications
            SET
                identification = ?,
                title = ?,
                observation = ?
            WHERE id = ?
            """,
            (
                identification,
                title,
                observation,
                notification_id,
            ),
        )