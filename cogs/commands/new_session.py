import disnake
from disnake.ext import commands
from utils import database, checks


class CreateNewSession(commands.Cog):
    def __init__(self, bot: disnake.ext.commands.Bot):
        self.bot = bot

    @commands.slash_command(
        guild_only=True, name="создать-новую-сессию", description="Создаёт новую сессию"
    )
    async def create_new_session(
        self,
        inter: disnake.ApplicationCommandInteraction,
        session_name: str = commands.Param(
            default=None,
            name="название",
            description="Название которое вы хотите дать сессии",
        ),
    ):
        if not await checks.is_admin(inter=inter):
            return await inter.response.send_message(
                embed=disnake.Embed(
                    title="ОШИБКА",
                    description="Вы должны быть администратором для использования данной команды!",
                    color=disnake.Color.red(),
                ),
                ephemeral=True,
            )
        session_list = await database.get_sessions_list()
        session_name = await database.create_new_session(session_name=session_name)
        if session_list and session_name in session_list:
            return await inter.response.send_message(
                embed=disnake.Embed(
                    title="ОШИБКА",
                    description="Сессия с указанным вами именем уже существует!",
                    color=disnake.Color.red(),
                ),
                ephemeral=True,
            )
        await inter.response.send_message(
            embed=disnake.Embed(
                title="УСПЕХ",
                description="Сессия успешно создана!\n"
                f"Название сессии: `{session_name}`",
                color=disnake.Color.green(),
            ),
            ephemeral=True,
        )


def setup(bot: commands.Bot):
    bot.add_cog(CreateNewSession(bot))
    print(f">{__name__} is launched")
