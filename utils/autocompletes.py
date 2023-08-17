from utils import database
import disnake


async def sessions_autocompleter(
    inter: disnake.ApplicationCommandInteraction, value: str
) -> list:
    sessions = []
    found = False
    sessions_list = await database.get_sessions_list()
    for session in sessions_list:
        if value in session:
            found = True
            sessions.append(session)
    if found:
        return sessions[:25]
    else:
        return ["По вашему запросу ничего не найдено!"]
