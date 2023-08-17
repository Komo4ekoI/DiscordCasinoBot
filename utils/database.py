from motor.motor_asyncio import AsyncIOMotorClient
import time
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())


client = AsyncIOMotorClient(os.getenv("DB_LINK"))
db = client["sessions"]
bot_info_db = client["bot_info_db"]

bot_info_collection = bot_info_db["bot_info"]


async def create_new_session(session_name: str) -> str:
    """Создаёт новую сессию в базе данных"""
    named_tuple = time.localtime()
    time_string = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)
    time_dig = time.time()

    final_name = time_string if session_name is None else session_name

    collection = db[f"{final_name}"]

    await collection.insert_one(
        {"session_name": final_name, "create_time": time_dig, "time": time_string}
    )

    if old_session_name := await get_current_session_name():
        await bot_info_collection.update_one(
            {"current_session": old_session_name},
            {"$set": {"current_session": final_name}},
        )
    else:
        await bot_info_collection.insert_one({"current_session": final_name})

    return final_name


async def get_sessions_list() -> list:
    """Получить название всех существующих сессий"""
    sessions_list = [collection for collection in await db.list_collection_names()]
    return sessions_list


async def delete_session(session_name: str) -> bool:
    """Удаляет указанную сессию. Возвращает bool значение, являлась ли сессия активной"""
    collection = db[f"{session_name}"]
    await collection.drop()
    current_session = await get_current_session_name()
    if current_session and session_name == current_session:
        await bot_info_collection.delete_one({"current_session": session_name})
        return True
    return False


async def get_current_session_name() -> str or bool:
    """Возвращает название активной сессии"""
    session_name = None
    result = await bot_info_collection.find({}, {"current_session": 1}).to_list(
        length=None
    )
    if result:
        for info in result:
            session_name = info.get("current_session", str)

    if session_name:
        return session_name

    return None


async def change_user_balance(discord_id: int, session_name: str, value: int) -> None:
    """Изменяет баланс на указанное значение относительно нынешнего баланса"""
    collection = db[session_name]
    current_balance = await get_user_balance(
        session_name=session_name, discord_id=discord_id
    )
    result = current_balance - abs(value) if value < 0 else current_balance + abs(value)
    await collection.update_one(
        {"discord_id": discord_id}, {"$set": {"balance": result}}
    )


async def check_session_member(session_name: str, discord_id: int) -> bool:
    """Возвращает значение, есть ли пользователь в указанной сессии"""
    collection = db[session_name]
    result = await collection.find_one({"discord_id": discord_id})
    return True if result else False


async def get_user_balance(session_name: str, discord_id: int) -> int or bool:
    """Возвращает текущий баланс пользователя в определённой сессии, или None если такого пользователя в сессии нет"""
    collection = db[session_name]
    user_data = await collection.find_one({"discord_id": discord_id}, {"balance": 1})
    if user_data:
        return user_data.get("balance", 1)
    return None


async def replenish_balance(discord_id: int, session_name: str, value: int) -> None:
    """Пополняет счёт игрока на указанное число"""
    collection = db[session_name]
    if (
        await get_user_balance(session_name=session_name, discord_id=discord_id)
        is not None
    ):
        current_topped_balance = await get_topped_balance(
            discord_id=discord_id, session_name=session_name
        )
        await collection.update_one(
            {"discord_id": discord_id},
            {"$set": {"topped_balance": current_topped_balance + value}},
        )
        await change_user_balance(
            discord_id=discord_id, session_name=session_name, value=value
        )
    else:
        await collection.insert_one(
            {
                "discord_id": discord_id,
                "topped_balance": value,
                "balance": value,
                "withdrawn_balance": 0,
            }
        )


async def get_topped_balance(discord_id: int, session_name: str) -> int or bool:
    """Возвращает число, на сколько пользователь пополнял счёт за сессию, или None если пользователя нет в сессии"""
    collection = db[session_name]
    user_data = await collection.find_one(
        {"discord_id": discord_id}, {"topped_balance": 1}
    )
    if user_data:
        return user_data.get("topped_balance", 1)
    return None


async def get_withdrawn_balance(discord_id: int, session_name: str) -> int or bool:
    """Возвращает число, сколько пользователь снял за сессию, или None если пользователя нет в сессии"""
    collection = db[session_name]
    user_data = await collection.find_one(
        {"discord_id": discord_id}, {"withdrawn_balance": 1}
    )
    if user_data:
        return user_data.get("withdrawn_balance", 1)
    return None


async def withdraw(discord_id: int, session_name: str, value: int) -> None:
    """Снимает средства с баланса и добавляет данные об снятии"""
    collection = db[session_name]
    current_withdrawn_balance = await get_withdrawn_balance(
        discord_id=discord_id, session_name=session_name
    )
    await collection.update_one(
        {"discord_id": discord_id},
        {"$set": {"withdrawn_balance": current_withdrawn_balance + value}},
    )
    await change_user_balance(
        discord_id=discord_id, session_name=session_name, value=-value
    )


async def close_current_session():
    """Закрывает активную сессию"""
    current_session = await get_current_session_name()
    await bot_info_collection.delete_one({"current_session": current_session})
