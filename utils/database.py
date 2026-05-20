import sqlite3
import os

# =====================================
# DATABASE PATH
# =====================================

DB_PATH = os.getenv(
    "DB_PATH",
    "database/bot.db"
)

folder = os.path.dirname(
    DB_PATH
)

if folder:

    os.makedirs(
        folder,
        exist_ok=True
    )

print(
    "DATABASE:",
    DB_PATH
)

# =====================================
# CONNECT
# =====================================

conn = sqlite3.connect(
    DB_PATH,
    check_same_thread=False
)

cursor = conn.cursor()

# =====================================
# ADMINS
# =====================================

cursor.execute(
"""
CREATE TABLE IF NOT EXISTS admins(
    id INTEGER PRIMARY KEY
)
"""
)

# =====================================
# USERS
# =====================================

cursor.execute(
"""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY,
    fullname TEXT
)
"""
)

# =====================================
# LEADERBOARD
# =====================================

cursor.execute(
"""
CREATE TABLE IF NOT EXISTS leaderboard(
    user_id INTEGER PRIMARY KEY,
    fullname TEXT,
    correct INTEGER DEFAULT 0,
    total INTEGER DEFAULT 0
)
"""
)

conn.commit()

# =====================================
# ADMIN
# =====================================

def add_admin_db(uid):

    cursor.execute(
"""
INSERT OR IGNORE INTO admins(
id
)
VALUES(
?
)
""",
(uid,)
)

    conn.commit()


def del_admin_db(uid):

    cursor.execute(
"""
DELETE FROM admins
WHERE id=?
""",
(uid,)
)

    conn.commit()


def is_admin_db(uid):

    cursor.execute(
"""
SELECT id
FROM admins
WHERE id=?
""",
(uid,)
)

    return cursor.fetchone() is not None


def get_admins():

    cursor.execute(
"""
SELECT id
FROM admins
"""
    )

    return [
        x[0]
        for x in cursor.fetchall()
    ]

# =====================================
# USERS
# =====================================

def add_user_db(
        uid,
        fullname
):

    cursor.execute(
"""
INSERT OR IGNORE INTO users(
id,
fullname
)
VALUES(
?,
?
)
""",
(
uid,
fullname
)
)

    conn.commit()

def del_user_db(uid):

    # USER

    cursor.execute(
"""
DELETE FROM users
WHERE id=?
""",
(uid,)
)

    # REYTING

    cursor.execute(
"""
DELETE FROM leaderboard
WHERE user_id=?
""",
(uid,)
)

    conn.commit()


def is_user(uid):

    cursor.execute(
"""
SELECT id
FROM users
WHERE id=?
""",
(uid,)
)

    return cursor.fetchone() is not None


def get_users():

    cursor.execute(
"""
SELECT
id,
fullname
FROM users
ORDER BY id DESC
"""
    )

    return cursor.fetchall()

# =====================================
# LEADERBOARD
# =====================================

def save_result(
        uid,
        fullname,
        correct,
        total
):

    cursor.execute(
"""
SELECT
correct,
total
FROM leaderboard
WHERE user_id=?
""",
(uid,)
)

    old = cursor.fetchone()

    if old:

        correct += old[0]

        total += old[1]

        cursor.execute(
"""
UPDATE leaderboard
SET
fullname=?,
correct=?,
total=?
WHERE user_id=?
""",
(
fullname,
correct,
total,
uid
)
)

    else:

        cursor.execute(
"""
INSERT INTO leaderboard(
user_id,
fullname,
correct,
total
)
VALUES(
?,
?,
?,
?
)
""",
(
uid,
fullname,
correct,
total
)
)

    conn.commit()


def get_leaderboard():

    cursor.execute(
"""
SELECT
fullname,
correct,
total
FROM leaderboard
ORDER BY correct DESC
"""
    )

    return cursor.fetchall()


# =====================================
# TEST
# =====================================

if __name__ == "__main__":

    add_user_db(
        1,
        "TEST USER"
    )

    print(
        get_users()
    )