import aiosqlite

from datetime import datetime

DB_PATH = 'undb.db'


# Проверка есть ли пользователь в базе
async def get_user(user_id: int):
    async with aiosqlite.connect(DB_PATH, timeout=10) as db:
        cursor = await db.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        return await cursor.fetchone()

# Добавить нового пользователя
async def add_user(user_id: int, name: str):
    async with aiosqlite.connect(DB_PATH, timeout=10) as db:
        now = datetime.now().isoformat()
        await db.execute(
            'INSERT INTO users (id, name, entry_time, last_seen, first_sticker) VALUES (?, ?, ?, ?, ?)',
            (user_id, name, now, now, True))
        await db.commit()

# Обновить время последнего действия
async def update_last_seen(user_id: int):
    async with aiosqlite.connect(DB_PATH, timeout=10) as db:
        await db.execute(
            'UPDATE users SET last_seen = ? WHERE id = ?',
            (datetime.now().isoformat(), user_id))
        await db.commit()

# Обновить время отправки последнего стикера
async def update_last_sticker_time(user_id: int):
    async with aiosqlite.connect(DB_PATH, timeout=10) as db:
        await db.execute('UPDATE users SET last_sticker_start_time = ? WHERE id = ?', (datetime.now().isoformat(), user_id))
        await db.commit()

# Проверка наличия артикула в таблице items
async def get_articles_looks(look_id: int):
    async with aiosqlite.connect(DB_PATH, timeout=10) as db:
        cursor = await db.execute("""
            SELECT items.name, items.articul FROM look_items 
            JOIN items ON look_items.item_id = items.id
            WHERE look_items.look_id = ?
            """, (look_id,))
        rows = await cursor.fetchall() # Получает все строки в виде списка
        return rows

async def check_articul_exists(articul: str) -> bool:
    async with aiosqlite.connect(DB_PATH, timeout=10) as db:
        cursor = await db.execute("SELECT 1 FROM items WHERE articul = ?", (articul,))
        row = await cursor.fetchone()
        return row is not None


# Получение фото для отправки по id
async def get_look_photo(look_id: int):
    async with aiosqlite.connect(DB_PATH, timeout=10) as db:
        cursor = await db.execute("""
            SELECT photo_url
            FROM looks
            WHERE id = ?""", (look_id,))
        row = await cursor.fetchone() #Получает одну (первую) строку результата
        return row[0] if row else None # если row не пустой - вернуть row[0], иначе none

# Получение образов, где есть артикулы
async def get_looks_for_articul(articuls: list[str]) -> list[int]:
    placeholders = ','.join(['?'] * len(articuls))  # ?, ?, ?, ...
    query = f"""
        SELECT look_items.look_id
        FROM look_items
        JOIN items ON look_items.item_id = items.id
        WHERE items.articul IN ({placeholders})
        GROUP BY look_items.look_id
        HAVING COUNT(DISTINCT items.articul) = ?
    """
    async with aiosqlite.connect(DB_PATH, timeout=10) as db:
        cursor = await db.execute(query, (*articuls, len(articuls)))
        rows = await cursor.fetchall()
        return [row[0] for row in rows]

async def get_category_photo(category: str, exclude_ids: list[int] = None) -> list[str]:
    exclude_ids = exclude_ids or []
    placeholders = ",".join("?" for _ in exclude_ids)

    async with aiosqlite.connect(DB_PATH, timeout=10) as db:
        if exclude_ids:
            query = f"""
                SELECT photo_url, id FROM looks
                WHERE category = ? AND id NOT IN ({placeholders})
                ORDER BY RANDOM()
                LIMIT 5
            """
            params = [category] + exclude_ids
        else:
            query = """
                SELECT photo_url, id FROM looks
                WHERE category = ?
                ORDER BY RANDOM()
                LIMIT 5
            """
            params = [category]

        cursor = await db.execute(query, params)
        rows = await cursor.fetchall()
        return rows

async def stats_count():
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("SELECT COUNT(id) FROM users")
        row = await cursor.fetchone()
        return row[0] if row else None

async def get_all_user_ids():
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("SELECT id FROM users")
        rows = await cursor.fetchall()
        return [row[0] for row in rows]











