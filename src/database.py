# PostgreSQL database lifecycle and connection management

import os
import subprocess
import time

import psycopg


DATABASE_NAME = "app_note_rag"
DATABASE_USER = "app_user"
DATABASE_PASSWORD = "app_password"
DATABASE_HOST = "localhost"
DATABASE_PORT = 5432

DRIVE_ROOT = "/content/drive/MyDrive/app_note_rag"
BACKUP_DIRECTORY = os.path.join(DRIVE_ROOT, "db_backups")
BACKUP_PATH = os.path.join(BACKUP_DIRECTORY, "app_note_rag_backup.sql")

EXPECTED_TABLES = {
    "users",
    "notes",
    "summaries",
    "chunks",
}

DATABASE_CONFIG = {
    "host": DATABASE_HOST,
    "port": DATABASE_PORT,
    "dbname": DATABASE_NAME,
    "user": DATABASE_USER,
    "password": DATABASE_PASSWORD,
}


def _run_command(command):
    result = subprocess.run(
        command,
        shell=True,
        text=True,
        capture_output=True,
    )

    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip())

    return result.stdout.strip()


def _mount_drive():
    from google.colab import drive

    if not os.path.exists("/content/drive/MyDrive"):
        drive.mount("/content/drive")


def _install_postgresql():
    _run_command(
        "apt-get update -qq && "
        "apt-get install -y -qq postgresql postgresql-contrib"
    )


def _install_pgvector():
    _run_command(
        "apt-get update -qq && "
        "apt-get install -y -qq postgresql-16-pgvector"
    )


def _is_postgresql_running():
    result = subprocess.run(
        "service postgresql status",
        shell=True,
        text=True,
        capture_output=True,
    )

    return result.returncode == 0


def _start_postgresql():
    if not _is_postgresql_running():
        _run_command("service postgresql start")
        time.sleep(2)


def _ensure_database_user():
    role_exists = _run_command(
        f"sudo -u postgres psql -tAc "
        f"\"SELECT 1 FROM pg_roles WHERE rolname='{DATABASE_USER}';\""
    )

    if role_exists != "1":
        _run_command(
            f"sudo -u postgres psql -c "
            f"\"CREATE USER {DATABASE_USER} WITH PASSWORD '{DATABASE_PASSWORD}';\""
        )
    else:
        _run_command(
            f"sudo -u postgres psql -c "
            f"\"ALTER USER {DATABASE_USER} WITH PASSWORD '{DATABASE_PASSWORD}';\""
        )


def _database_exists():
    result = _run_command(
        f"sudo -u postgres psql -tAc "
        f"\"SELECT 1 FROM pg_database WHERE datname='{DATABASE_NAME}';\""
    )

    return result == "1"


def _ensure_database():
    if not _database_exists():
        _run_command(
            f"sudo -u postgres psql -c "
            f"\"CREATE DATABASE {DATABASE_NAME} OWNER {DATABASE_USER};\""
        )


def _ensure_pgvector():
    _run_command(
        f"sudo -u postgres psql {DATABASE_NAME} -c "
        "\"CREATE EXTENSION IF NOT EXISTS vector;\""
    )


def _get_tables():
    result = _run_command(
        f"sudo -u postgres psql {DATABASE_NAME} -tAc "
        f"\"SELECT table_name "
        f"FROM information_schema.tables "
        f"WHERE table_schema='public';\""
    )

    return {
        table.strip()
        for table in result.splitlines()
        if table.strip()
    }


def _database_is_complete():
    return EXPECTED_TABLES.issubset(_get_tables())


def _reset_database():
    _run_command(
        f"sudo -u postgres psql -d postgres -c "
        f"\"DROP DATABASE IF EXISTS {DATABASE_NAME};\""
    )

    _run_command(
        f"sudo -u postgres psql -d postgres -c "
        f"\"CREATE DATABASE {DATABASE_NAME} OWNER {DATABASE_USER};\""
    )

    _ensure_pgvector()


def _restore_backup():
    if not os.path.exists(BACKUP_PATH):
        return False

    if _database_is_complete():
        return False

    _reset_database()

    _run_command(
        f"sudo -u postgres psql {DATABASE_NAME} < '{BACKUP_PATH}'"
    )

    return True


def init_database():
    _mount_drive()
    os.makedirs(BACKUP_DIRECTORY, exist_ok=True)

    _install_postgresql()
    _install_pgvector()
    _start_postgresql()

    _ensure_database_user()
    _ensure_database()
    _ensure_pgvector()

    restored = _restore_backup()

    if restored:
        print("✅ PostgreSQL initialized and database restored.")
    else:
        print("✅ PostgreSQL initialized.")


def get_connection():
    return psycopg.connect(**DATABASE_CONFIG)


def backup_database():
    _mount_drive()
    os.makedirs(BACKUP_DIRECTORY, exist_ok=True)

    _run_command(
        f"sudo -u postgres pg_dump {DATABASE_NAME} > '{BACKUP_PATH}'"
    )

    print(f"✅ Database backup saved to: {BACKUP_PATH}")
