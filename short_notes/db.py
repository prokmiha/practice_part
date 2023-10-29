import aiosqlite


async def start_db():
    async with aiosqlite.connect('base.db') as db:
        cur = await db.cursor()
        await cur.execute(
            """CREATE TABLE IF NOT EXISTS Notes(
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            ID_Telegram INT,
            Note_Name TEXT,
            Note_Text TEXT
        )""")


async def add_to_db(user_id, name, text):
    async with aiosqlite.connect('base.db') as db:
        cur = await db.cursor()
        await cur.execute("INSERT INTO Notes (ID_Telegram, Note_Name, Note_Text) VALUES (?, ?, ?)",
                          (user_id, name, text))
        await db.commit()


async def get_from_db(user_id):
    async with aiosqlite.connect('base.db') as db:
        cur = await db.cursor()
        await cur.execute("SELECT Note_Name, Note_Text FROM Notes WHERE ID_Telegram = ?", (user_id,))
        result = await cur.fetchall()

        if not result:
            return False
        else:
            notes_list = [{'Note_Name': note[0], 'Note_Text': note[1]} for note in result]
            return notes_list
