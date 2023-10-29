import aiosqlite


async def start_db():
    async with aiosqlite.connect('base.db') as db:
        cur = await db.cursor()
        await cur.execute(
            """CREATE TABLE IF NOT EXISTS Log(
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            ID_Telegram INT,
            Messages TEXT
        )""")


async def add_to_db(user_id, text):
    async with aiosqlite.connect('base.db') as db:
        cur = await db.cursor()

        await cur.execute("INSERT INTO Log (ID_Telegram, Messages) VALUES (?, ?)", (user_id, text))
        await db.commit()

        await cur.execute("SELECT COUNT(*) FROM Log WHERE ID_Telegram = ?", (user_id,))
        message_count = await cur.fetchone()
        message_count = message_count[0] if message_count else 0

        if message_count > 5:
            await cur.execute(
                "DELETE FROM Log WHERE ID_Telegram = ? AND ID IN (SELECT ID FROM Notes WHERE ID_Telegram = ? ORDER BY ID ASC LIMIT 1)",
                (user_id, user_id)
            )
            await db.commit()


async def get_from_db(user_id):
    async with aiosqlite.connect('base.db') as db:
        cur = await db.cursor()

        await cur.execute(
            "SELECT Messages FROM Log WHERE ID_Telegram = ? ORDER BY ID DESC LIMIT 5",
            (user_id,)
        )
        messages = await cur.fetchall()
        return [message[0] for message in messages]
