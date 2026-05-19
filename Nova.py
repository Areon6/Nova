
import  asyncio
import aiosqlite
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.utils.keyboard import InlineKeyboardBuilder
import os
API_TOKEN = os.getenv("API_TOKEN")

bot = Bot(token= API_TOKEN)
dp = Dispatcher()


async def init_db():
    async with aiosqlite.connect("products.db") as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS products (
                name TEXT PRIMARY KEY,
                calories_per_100g REAL
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS food_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                name TEXT,
                weight REAL,
                calories REAL,
                date TEXT
            )
        """)
        await db.commit()
    
@dp.message(Command("start"))
async def start(message: types.Message):
    async with aiosqlite.connect("products.db") as db:
        async with db.execute("SELECT name, calories_per_100g FROM products") as cursor:
            rows = await cursor.fetchall()
    
    if not rows:
        await message.answer("Список пуст.")
        return
    
    text = "📜 Доступные продукты:\n"
    for row in rows:
        text += f"• {row[0]} — {row[1]} ккал/100г\n"
    
    await message.answer(text)
@dp.message(Command("history"))
async def history(message: types.Message):
    async with aiosqlite.connect('products.db') as db:
        async with db.execute('''SELECT name, weight, calories, date FROM food_log 
                                WHERE user_id = ? 
                                ORDER BY date DESC 
                                LIMIT 50''', (message.from_user.id,)) as cursor:
            row = await cursor.fetchall()
            text = "История:\n"
            for row in row:
                text += f"{row[3][8:10]}.{row[3][5:7]} — {row[0]} {row[1]}г — {row[2]} ккал\n"
        await message.answer(text)
        return  
@dp.message(Command("profile"))
async def profile(message: types.Message):
    data = message.text.lower().split()
    if len(data) <= 2:
        await message.answer("Введите в правильном формате")
    else:    
        hight = float(data[1])
        hight_m = hight / 100
        weight = float(data[2])
        imt = round(weight / (hight_m * hight_m), 1)
        if imt < 18.5:
            category = "Дефицит массы тела"
            calories = 2800
        elif imt < 25:
            category = "Норма"
            calories = 2500
        elif imt < 30:
            category = "Избыточный вес"
            calories = 2000
        else:
            category = "Ожирение"
            calories = 1800
        await message.answer(f"ИМТ: {imt}\nСтатус: {category}\nРекомендуемый калораж: {calories} ккал/день")

@dp.message(Command("eat"))
async def eat(message: types.Message):
    data = message.text.lower().split()
    if len(data) >= 3:
        name = data[1]
        weight = float(data[2])
    
        async with aiosqlite.connect('products.db') as bd:
            async with bd.execute("SELECT calories_per_100g FROM products WHERE name = ?", (name,)) as cursor:
                row = await cursor.fetchone()
                if row == None:
                    await message.answer(f"Продукт не найден")
                else:
                    calories_per_100g = row[0]
                    total = (calories_per_100g * weight) / 100
                    
                    # ЗАПИСЬ В ЛОГ
                    await bd.execute(
                        "INSERT INTO food_log (user_id, name, weight, calories, date) VALUES (?, ?, ?, ?, CURRENT_DATE)",
                        (message.from_user.id, name, weight, total)
                    )
                    await bd.commit()
                    
                    await message.answer(f"Записал: {name}, {total:.2f} ккал. Приятного аппетита.")
                    
    else:
        await message.answer("Введите в правильном формате")
    
    
    
    
@dp.message(Command("add"))
async def addproduct(message: types.Message):
    data = message.text.lower().split()
    
    # Нужно минимум 3 части: /add, Название, Калории
    if len(data) < 3:
        await message.answer("Напиши в формате: /add Рис 200")
        return
        
    new_name = data[1]
    try:
        new_cal = float(data[2])
    except ValueError:
        await message.answer("Калории должны быть числом!")
        return

    # Проверяем наличие по ключу 'name' внутри списка словарей
    try:
        # Добавляем в ТАКОМ ЖЕ формате, как остальные продукты
        async with aiosqlite.connect("products.db") as db:
            await db.execute("INSERT OR IGNORE INTO products (name, calories_per_100g) VALUES (?, ?)",
        (new_name, new_cal))
            await db.commit()
            await message.answer(f'Продукт {new_name} добавлен!')
    except Exception as e:
        await message.answer("Продукт уже добавлен")

@dp.message(Command("list"))
async def show_list(message: types.Message):
    async with aiosqlite.connect("products.db") as db:
        async with db.execute("SELECT name, calories_per_100g FROM products") as cursor:
            rows = await cursor.fetchall()
    
    if not rows:
        await message.answer("Список пуст.")
        return
    
    text = "📜 Доступные продукты:\n"
    for row in rows:
        text += f"• {row[0]} — {row[1]} ккал/100г\n"
    
    await message.answer(text)
@dp.message(Command("delete"))




async def delete_product(message: types.Message):
    data = message.text.split()
    if len(data) < 2:
        await message.answer("Введите в правильном формате")
        return
    name = data[1]
    async with aiosqlite.connect("products.db") as db:
        await db.execute("DELETE FROM products WHERE name = ?", (name,))
        await db.commit()
    await message.answer(f'{name} удалён из списка')    
@dp.message(Command("today"))
async def today_colories(message: types.Message):
    async with aiosqlite.connect("products.db") as db:
        async with db.execute("SELECT SUM(calories) FROM food_log WHERE user_id = ? AND date = CURRENT_DATE", (message.from_user.id,)) as cursor : 
            row = await cursor.fetchone()
        await message.answer(f"За сегодня {row[0]} колллорий") 

@dp.message()
async def par(message: types.Message):
    if message.text.startswith("/"):
        return

    data = message.text.split()
    if len(data) < 2:
        await message.answer("Напиши в формате: Рис 200")
        return
    
    name = data[0]
    weight = float(data[1])
    
    async with aiosqlite.connect("products.db") as db:
        async with db.execute("SELECT calories_per_100g FROM products WHERE name = ?", (name,)) as cursor:
            
            row = await cursor.fetchone()
            if row is None:
                await message.answer("блабла")
                
            else:
                calories_per_100g = row[0]
                result = calories_per_100g * weight / 100
                await message.answer(f"В {weight} граммах {name} - {result} коллорий")

            
  
async def main():
    await init_db()
    await dp.start_polling(bot)

asyncio.run(main())
    
