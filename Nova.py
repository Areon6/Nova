# def color():
#     result = 0
#     sum = 0
    
    

#     while True:
#         produkt2 = input("Введите название продукта2")
#         if produkt2 == ".":
#             break
#         weight = int(input("Введите вес"))
        
#         if produkt2.lower() == 'чечевица':
#             result = weight * 1.16
#         elif produkt2.lower() == 'рис':
#             result = weight * 1.26
#         elif produkt2.lower() == 'яйцо сырое'or produkt2 == "яс" :
#             result = weight * 1.15
#         elif produkt2.lower() == 'яйцо варённое'or produkt2 == 'яв':
#             result = weight * 1.43
#         elif produkt2.lower() == 'банан':
#             result = weight * 0.94
#         elif produkt2.lower() == "масло":
#             result = weight * 8.97
#         elif produkt2.lower() == "жаренная картошка" or produkt2.lower() == "жк":
#             result = weight * 2.0
#         elif produkt2.lower() == 'яйцо жаренное' or produkt2.lower() == "яж":
#             result = weight * 1.96
#         elif produkt2.lower() == 'лепёшка' :
#             result = weight * 2.44
#         else: 
#             print("продукт не найден")
#             continue
        
#         sum += result
#         continue
    
#     return round(sum, 1)
# print(color())

# async def calcolor():
#     total = 0 

#     while True:
#         name = input("Введите Продукт (или точку для выхода): ").lower()
#         if name == '.':  break
        
#         if name in allproduct:
            
#             try:
#                 weight = float(input("Весс в граммах: "))
#                 total += weight * allproduct[name]
#             except ValueError:
#                 print("Ошибка! Введите число")
#         if name not in allproduct:              
#             print("Такого продукта нет в базе. Хотели бы вы внести его?")
#             a = input("Введите да или нет")
#             if a == "да":
#                 try:
#                     new_product = float(input("Соклько колллорий в этом продукте? :"))
#                 except:
#                     print("Вы ввели неверное значение")
#                 allproduct.update({name : new_product})
#                 continue
            
        
        
#     return round(total, 2)






# import asyncio
# from aiogram import Bot, Dispatcher, types
# from aiogram.filters import Command

# # 1. Вставь сюда свой токен
# API_TOKEN = '8070009245:AAFyYwBmhNEnox-q4FGgbSwN7LJ8aGmdYis'

# bot = Bot(token=API_TOKEN)
# dp = Dispatcher()

# allproduct = {
#     'чечевица': 1.16,
#     'рис': 1.26,
#     "яйцо сырое" : 1.15,
#     "яйцо жаренное" : 1.96,
#     "яйцо варенное" : 1.43,
#     'банан' : 0.94,
#     'масло' : 8.97,
#     'жаренная картошка' : 2.0,
#     'лепёшка' : 2.44,
#     'гречка' : 1.0,
#     'манная каша' : 1.10,
#     'ойгурт' : 1.20,
# }

# # Обработчик команды /start
# @dp.message(Command("start"))
# async def cmd_start(message: types.Message):
#     await message.answer("Привет! Пришли мне назв/add Творог 80ание продукта и вес через пробел.\nНапример: рис 200")
# @dp.message(Command("end"))
# async def end(message: types.Message):
#     await message.answer("Всё иди нахуй уже")
# # Основная логика обработки сообщений
# @dp.message() 
# async def calculate_calories(message: types.Message):
#     try:
#         # Разделяем сообщение на название и вес
#         # Пример: "рис 200" -> name="рис", weight="200"
#         data = message.text.lower().split()
        
#         if len(data) < 2:
#             await message.answer("Пожалуйста, введи продукт и вес через пробел.")
#             return

#         name = data[0]
#         weight = float(data[1])

#         if name in allproduct:
#             calories = round(weight * allproduct[name], 2)
#             await message.answer(f"В {weight}г продукта '{name}' содержится {calories} ккал.")
#         else:
#             await message.answer(f"Продукта '{name}' нет в базе. Добавь его (скоро научимся это делать через бота!)")
            
#     except ValueError:
#         await message.answer("Ошибка! Вес должен быть числом.")

    
# async def main():
#     # Запуск процесса опроса серверов Telegram
#     await dp.start_polling(bot)

# if __name__ == "__main__":
#     try:
#         asyncio.run(main())
#     except KeyboardInterrupt:
#         print("Бот выключен")





# import asyncio
# import aiosqlite
# from aiogram import Bot, Dispatcher, types, 
# from aiogram.filters import Command
# from aiogram.utils.keyboard import ReplyKeyboardBuilder
# from aiogram.utils.keyboard import InlineKeyboardBuilder

# API_TOKEN = '8070009245:AAFyYwBmhNEnox-q4FGgbSwN7LJ8aGmdYis'
# bot = Bot(token=API_TOKEN)
# dp = Dispatcher()

# # --- РАБОТА С БАЗОЙ ДАННЫХ ---
# async def init_db():
#     async with aiosqlite.connect("calories.db") as db:
#         # Создаем таблицу, если её нет
#         await db.execute("""
#             CREATE TABLE IF NOT EXISTS products (
#                 name TEXT PRIMARY KEY,
#                 calories REAL
#             )
#         """)
#         # Заполним базу начальными данными, если она пустая
#         cursor = await db.execute("SELECT COUNT(*) FROM products")
#         count = await cursor.fetchone()
#         if count[0] == 0:
#             initial_data = [
#                 ('Рис', 1.26), ('Банан', 0.94), ('Чечевица', 1.16), ('Гречка', 1.0)
#             ]
#             await db.executemany("INSERT INTO products VALUES (?, ?)", initial_data)
#         await db.commit()
# @dp.message(F.text == "🍎 Список продуктов")
# async def show_products(message: types.Message):
#     products = await get_products() # Берем из БД
#     builder = InlineKeyboardBuilder()
    
#     for name in products:
#         # callback_data — это то, что бот "услышит" при нажатии
#         builder.button(text=f"Удалить {name}", callback_data=f"del_{name}")
    
#     builder.adjust(1) # Кнопки в один столбец
#     await message.answer("Нажми на продукт, чтобы удалить его:", reply_markup=builder.as_markup())
# async def get_products():
#     async with aiosqlite.connect("calories.db") as db:
#         async with db.execute("SELECT name FROM products") as cursor:
#             rows = await cursor.fetchall()
#             return [row[0] for row in rows]

# # --- КЛАВИАТУРА ---
# def main_menu_kb():
#     builder = ReplyKeyboardBuilder()
#     builder.button(text="🍎 Список продуктов")
#     builder.button(text="📊 Посчитать калории")
#     builder.button(text="ℹ️ Помощь")
#     builder.adjust(2) # Делаем 2 кнопки в ряд
#     return builder.as_markup(resize_keyboard=True)

# # --- ХЭНДЛЕРЫ ---
# @dp.message(Command("start"))
# async def cmd_start(message: types.Message):
#     await message.answer("Добро пожаловать! Используй кнопки для навигации.", 
#                          reply_markup=main_menu_kb())

# @dp.message(F.text == "🍎 Список продуктов")
# async def show_products(message: types.Message):
#     products = await get_products()
#     text = "Доступные продукты:\n" + "\n".join(f"— {p}" for p in products)
#     await message.answer(text)

# @dp.message(F.text == "📊 Посчитать калории")
# async def calc_prompt(message: types.Message):
#     await message.answer("Пришли название и вес как раньше (например: Рис 200). Скоро мы сделаем это кнопками!")



# async def delete_product(name):
#     async with aiosqlite.connect("calories.db") as db:
#         # SQL-команда: УДАЛИТЬ ИЗ таблицы ГДЕ имя равно...
#         await db.execute("DELETE FROM products WHERE name = ?", (name,))
#         await db.commit()
# async def main():
#     await init_db() # Инициализируем БД перед запуском
#     await dp.start_polling(bot)

# if __name__ == "__main__":
#     asyncio.run(main())




import  asyncio
import aiosqlite
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.utils.keyboard import InlineKeyboardBuilder

API_TOKEN = "8070009245:AAFyYwBmhNEnox-q4FGgbSwN7LJ8aGmdYis"

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
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

    
    
    
    
    
    
    
    
