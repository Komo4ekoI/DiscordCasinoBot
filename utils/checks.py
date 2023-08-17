import disnake
from dotenv import find_dotenv, load_dotenv
import os

load_dotenv(find_dotenv())

admin_role_id = int(os.getenv("ADMIN_ROLE_ID"))
croupier_role_id = int(os.getenv("CROUPIER_ROLE_ID"))
cashier_role_id = int(os.getenv("CASHIER_ROLE_ID"))


async def is_admin(inter: disnake.ApplicationCommandInteraction) -> bool:
    role = inter.guild.get_role(admin_role_id)
    return True if role in inter.user.roles else False


async def is_cashier(inter: disnake.ApplicationCommandInteraction) -> bool:
    role = inter.guild.get_role(cashier_role_id)
    return True if role in inter.user.roles else False


async def is_croupier(inter: disnake.ApplicationCommandInteraction) -> bool:
    role = inter.guild.get_role(croupier_role_id)
    return True if role in inter.user.roles else False
