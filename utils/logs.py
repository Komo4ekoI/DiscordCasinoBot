import disnake
from dotenv import load_dotenv, find_dotenv
import os
import time

load_dotenv(find_dotenv())

logs_channel_id = int(os.getenv("log_channel_id"))


async def change_balance_log(
    balance_before: int,
    balance_after: int,
    count: int,
    session_name: str,
    inter: disnake.ApplicationCommandInteraction,
    target_user: disnake.Member,
):
    channel = await inter.bot.fetch_channel(logs_channel_id)
    await channel.send(
        embed=disnake.Embed(
            title="ТРАНЗАКЦИЯ",
            description=f"{inter.user.mention} изменил баланс {target_user.mention} на `{count}` фишек!\n\n"
            f"**Сессия** `{session_name}`\n"
            f"**Баланс до операции:** `{balance_before}`\n"
            f"**Баланс после операции:** `{balance_after}`\n"
            f"**Время проведения операции:** <t:{int(time.time())}:f>",
            color=disnake.Color.yellow(),
        )
    )


async def replenish_balance_log(
    balance_before: int,
    balance_after: int,
    count: int,
    session_name: str,
    inter: disnake.ApplicationCommandInteraction,
    target_user: disnake.Member,
):
    channel = await inter.bot.fetch_channel(logs_channel_id)
    await channel.send(
        embed=disnake.Embed(
            title="ТРАНЗАКЦИЯ",
            description=f"{inter.user.mention} пополнил счёт {target_user.mention} на `{count}` фишек!\n\n"
            f"**Сессия** `{session_name}`\n"
            f"**Баланс до операции:** `{balance_before}`\n"
            f"**Баланс после операции:** `{balance_after}`\n"
            f"**Время проведения операции:** <t:{int(time.time())}:f>",
            color=disnake.Color.green(),
        )
    )


async def withdraw_balance_log(
    balance_before: int,
    balance_after: int,
    count: int,
    session_name: str,
    inter: disnake.ApplicationCommandInteraction,
    target_user: disnake.Member,
):
    channel = await inter.bot.fetch_channel(logs_channel_id)
    await channel.send(
        embed=disnake.Embed(
            title="ТРАНЗАКЦИЯ",
            description=f"{inter.user.mention} снял `{count}` фишек со счёта {target_user.mention}!\n\n"
            f"**Сессия** `{session_name}`\n"
            f"**Баланс до операции:** `{balance_before}`\n"
            f"**Баланс после операции:** `{balance_after}`\n"
            f"**Время проведения операции:** <t:{int(time.time())}:f>",
            color=disnake.Color.dark_gold(),
        )
    )
