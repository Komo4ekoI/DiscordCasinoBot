import disnake
from disnake.ext import commands
from utils import database, checks


class CloseSession(commands.Cog):
    def __init__(self, bot: disnake.ext.commands.Bot):
        self.bot = bot

    @commands.slash_command(
        guild_only=True,
        name="закрыть-активную-сессию",
        description="Закрыть активную сессию",
    )
    async def close_session(self, inter: disnake.ApplicationCommandInteraction):
        if not await checks.is_admin(inter=inter):
            return await inter.response.send_message(
                embed=disnake.Embed(
                    title="ОШИБКА",
                    description="Вы должны быть администратором для использования данной команды!",
                    color=disnake.Color.red(),
                ),
                ephemeral=True,
            )
        current_session = await database.get_current_session_name()
        if current_session is None:
            return await inter.response.send_message(
                embed=disnake.Embed(
                    title="ОШИБКА",
                    description="Активной сессии не существует!",
                    color=disnake.Color.red(),
                ),
                ephemeral=True,
            )
        await database.close_current_session()
        return await inter.response.send_message(
            embed=disnake.Embed(
                title="УСПЕХ",
                description=f"Сессия `{current_session}` закрыта!",
                color=disnake.Color.orange(),
            ),
            ephemeral=True,
        )


def setup(bot: commands.Bot):
    bot.add_cog(CloseSession(bot))
    print(f">{__name__} is launched")
