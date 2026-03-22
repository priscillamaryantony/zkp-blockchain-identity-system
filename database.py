import sqlite3

DB_NAME = "blockchain.db"


# 🧱 Create table
def init_db():
    with sqlite3.connect(DB_NAME, timeout=10) as conn:
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS blocks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            block_index INTEGER,
            timestamp TEXT,
            hash TEXT,
            previous_hash TEXT,
            proof TEXT,
            identity_hash TEXT,
            reason TEXT,
            user TEXT
        )
        """)

        conn.commit()


# ➕ Insert block
def insert_block(block):
    with sqlite3.connect(DB_NAME, timeout=10) as conn:
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO blocks (
            block_index,
            timestamp,
            hash,
            previous_hash,
            proof,
            identity_hash,
            reason,
            user
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            block.index,
            block.timestamp,
            block.hash,
            block.previous_hash,
            block.data.get("proof", ""),
            block.data.get("hash", ""),
            block.data.get("reason", ""),
            block.data.get("user", "")
        ))

        conn.commit()


# 📊 Fetch all blocks
def get_blocks():
    with sqlite3.connect(DB_NAME, timeout=10) as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM blocks ORDER BY block_index ASC")
        rows = cursor.fetchall()

    return rows