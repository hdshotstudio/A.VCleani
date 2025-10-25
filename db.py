import aiosqlite

DB_NAME = "bookings.db"

CREATE_BOOKINGS = """
CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    username TEXT,
    service TEXT,
    date TEXT,
    address TEXT,
    phone TEXT,
    status TEXT DEFAULT 'pending'
)
"""

async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(CREATE_BOOKINGS)
        await db.commit()

async def add_booking(b):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            "INSERT INTO bookings (user_id, username, service, date, address, phone) VALUES (?, ?, ?, ?, ?, ?)",
            (b["user_id"], b["username"], b["service"], b["date"], b["address"], b["phone"])
        )
        await db.commit()
        return cursor.lastrowid

async def get_booking(bid):
    async with aiosqlite.connect(DB_NAME) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("SELECT * FROM bookings WHERE id = ?", (bid,))
        row = await cursor.fetchone()
        return dict(row) if row else None

async def list_bookings():
    async with aiosqlite.connect(DB_NAME) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("SELECT * FROM bookings ORDER BY id DESC")
        rows = await cursor.fetchall()
        return [dict(r) for r in rows]

async def user_bookings(uid):
    async with aiosqlite.connect(DB_NAME) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("SELECT * FROM bookings WHERE user_id = ? ORDER BY id DESC", (uid,))
        rows = await cursor.fetchall()
        return [dict(r) for r in rows]

async def update_status(bid, status):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("UPDATE bookings SET status = ? WHERE id = ?", (status, bid))
        await db.commit()