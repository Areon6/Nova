# import asyncio
# from aiogram import Bot, Dispatcher, types
# from aiogram.filters import Command

# API_TOKEN = "8070009245:AAFyYwBmhNEnox-q4FGgbSwN7LJ8aGmdYis"

# bot = Bot(token= API_TOKEN)
# dp = Dispatcher

# allproduct = [
#     {"name": "Рис", "calories_per_100g": 130},
#     {"name": "Банан", "calories_per_100g": 89},
# ]
# async def par(message: types.Massages):
#     data =  message.text.split()
#     name = data[0]
#     weight = float(data[1])
#     for i in allproduct:
#         if i["name"].lower() == name.lower:
#             result = (i["weight"] / 100) * weight
#             await message.answer(result)
#             return
#     await message.answer("Продукт не найден")        
# @dp.message(Command("list"))
# async def show_list(message: types.Messages):
#     text = "Доступные продукты:\n"
#     for i in products:
#         text += f"— {i['name']} ({i['calories_per_100g']} ккал/100г)\n"
#     await message.answer(text)

# import asyncio

# async def main():
#     print("Hello")
#     await asyncio.sleep(10)
#     print("World")

# main()

# import asyncio
# import time

# async def say(time, word):
#     await asyncio.sleep(time)
#     print(word)

# async def main():
#     print(f"started at {time.strftime("%X")}")
    
#     await say(1,"any")
#     await say(2, "beny")
    
#     print(f'enden at {time.strftime("%X")}')
    
# asyncio.run(main())













# import  asyncio
# import aiosqlite
# from aiogram import Bot, Dispatcher, types
# from aiogram.filters import Command


# API_TOKEN = "8070009245:AAFyYwBmhNEnox-q4FGgbSwN7LJ8aGmdYis"
# bot = Bot(token = API_TOKEN)
# DB_Name = "calories.db"
# dp = Dispatcher()

# async def init_db():
#     async with aiosqlite.connect(DB_Name) as db: # Добавляем эту строку
#         await db.execute('''
#             CREATE TABLE IF NOT EXISTS products(
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 name TEXT UNIQUE NOT NULL,
#                 calories REAL NOT NULL
#             ) ''')
#         # ... остальной код таблиц ...
#         await db.commit()
        


# @dp.message(Command("add"))
# async def add_product(message: types.Message):
#     data = message.text.split()
#     if len(data) < 3:
#         await message.answer("Напиши в правильном формате")
        
#         return
    
#     name = data[1].lower()
#     try:
#         calories = float(data[2])
#     except ValueError:
#             await message.answer("Калории должны быть числом")
#             return
        

#     async with aiosqlite.connect(DB_Name) as db:
#         try:
#             await db.execute("INSERT INTO products (name, calories) VALUES (?, ?)", (name, calories))
#             await db.commit()
#             await message.answer(f"Продукт '{name}' (калорийность {calories} ккал/100г) успешно добавлен!")
#         except aiosqlite.IntegrityError:
#             await message.answer(f"Продукт '{name}' уже есть в базе данных.")
   
    



# @dp.message(Command("eat"))
# async def eat(message: types.Message):
#     data = message.text.split()
#     if len(data) < 3:
        
#         await message.answer("Напиши в правильном формате")
#         return
    
#     name = data[1].lower()
    
#     try:
#         weight = float(data[2])
#     except ValueError:
#         await message.answer('вес должен быть числом')
#         return
#     user_id = message.from_user.id
    
#     async with aiosqlite.connect(DB_Name) as db:
#         async with db.execute("SELECT calories FROM products WHERE name = ?", (name,)) as cursor:
#             result = await cursor.fetchone()
            
#         if result is None:
#             await message.answer("Продукт не найден")
#             return
#         calories_per_100g = result[0]
#         total_calories = (calories_per_100g * weight) / 100
#         await db.execute(
#             "INSERT INTO food_log (user_id, product_name, weight, calories) VALUES (?, ?, ?, ?)",
#             (user_id, name, weight, total_calories)
#         )
#         await db.commit()
        
#     await message.answer(f"Записал! {name}, {weight}г. Это вышло на {total_calories:.1f} ккал.")
    
# async def main():
#     await init_db()
#     await dp.start_polling(bot)
    

# asyncio.run(main())





hight = 180
hight_m = hight / 100
weight = 55
print(round(weight / (hight_m * hight_m), 1))