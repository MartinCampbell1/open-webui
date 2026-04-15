#!/usr/bin/env python3
"""Create or refresh a local Open WebUI audit user in the SQLite database."""

from __future__ import annotations

import argparse
import sqlite3
import sys
import time
import uuid
from pathlib import Path

import bcrypt


DEFAULT_DB_PATH = Path("backend/open_webui/data/webui.db")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create or refresh a local audit user for Open WebUI."
    )
    parser.add_argument(
        "--db",
        type=Path,
        default=DEFAULT_DB_PATH,
        help=f"Path to webui.db (default: {DEFAULT_DB_PATH})",
    )
    parser.add_argument(
        "--email",
        default="test@example.com",
        help="Audit user email (default: test@example.com)",
    )
    parser.add_argument(
        "--password",
        default="test",
        help="Audit user password (default: test)",
    )
    parser.add_argument(
        "--name",
        default="Audit Test",
        help='Display name (default: "Audit Test")',
    )
    parser.add_argument(
        "--role",
        default="admin",
        choices=("admin", "user", "pending"),
        help="Role to assign (default: admin)",
    )
    return parser.parse_args()


def require_tables(conn: sqlite3.Connection) -> None:
    cur = conn.cursor()
    for table in ("auth", "user"):
        cur.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
            (table,),
        )
        if cur.fetchone() is None:
            raise RuntimeError(
                f"Required table '{table}' was not found. "
                "Make sure this is a valid Open WebUI SQLite database."
            )


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(rounds=12)).decode(
        "utf-8"
    )


def upsert_user(
    conn: sqlite3.Connection,
    *,
    email: str,
    password: str,
    name: str,
    role: str,
) -> dict[str, object]:
    cur = conn.cursor()
    now = int(time.time())
    email = email.strip().lower()
    password_hash = hash_password(password)

    cur.execute("SELECT id FROM auth WHERE email=?", (email,))
    row = cur.fetchone()

    if row:
        user_id = row[0]
        cur.execute(
            "UPDATE auth SET password=?, active=1 WHERE id=?",
            (password_hash, user_id),
        )
        cur.execute(
            "UPDATE user SET name=?, email=?, role=?, updated_at=?, last_active_at=? WHERE id=?",
            (name, email, role, now, now, user_id),
        )
        action = "updated"
    else:
        user_id = str(uuid.uuid4())
        cur.execute(
            "INSERT INTO auth (id, email, password, active) VALUES (?, ?, ?, 1)",
            (user_id, email, password_hash),
        )
        cur.execute(
            """
            INSERT INTO user (
                id,
                name,
                email,
                role,
                profile_image_url,
                created_at,
                updated_at,
                last_active_at,
                username,
                bio,
                gender,
                date_of_birth,
                profile_banner_image_url,
                timezone,
                presence_state,
                status_emoji,
                status_message,
                status_expires_at,
                oauth,
                info,
                settings,
                scim
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user_id,
                name,
                email,
                role,
                "",
                now,
                now,
                now,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
            ),
        )
        action = "created"

    conn.commit()
    return {
        "action": action,
        "id": user_id,
        "email": email,
        "name": name,
        "role": role,
    }


def main() -> int:
    args = parse_args()
    db_path = args.db.expanduser().resolve()

    if not db_path.exists():
        print(
            f"Database not found: {db_path}\n"
            "Start Open WebUI once or point --db to an existing webui.db.",
            file=sys.stderr,
        )
        return 1

    conn = sqlite3.connect(db_path)
    try:
        require_tables(conn)
        result = upsert_user(
            conn,
            email=args.email,
            password=args.password,
            name=args.name,
            role=args.role,
        )
    except Exception as exc:
        print(f"Failed to create audit user: {exc}", file=sys.stderr)
        return 1
    finally:
        conn.close()

    print(
        f"{result['action']} audit user\n"
        f"db={db_path}\n"
        f"email={result['email']}\n"
        f"name={result['name']}\n"
        f"role={result['role']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
