import disnake
from disnake.ext import commands
from utils import database, autocompletes, checks


class DeleteSession(commands.Cog):
    def __init__(self, bot: disnake.ext.commands.Bot):
        self.bot = bot

    @commands.slash_command(
        guild_only=True,
        name="удалить-сессию",
        description="Удалить одну из существующих сессий",
    )
    async def delete_session(
        self,
        inter: disnake.ApplicationCommandInteraction,
        session: str = commands.param(
            autocomplete=autocompletes.sessions_autocompleter,
            name="сессия",
            description="Сессия которую вы хотите удалить",
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
        sessions_list = await database.get_sessions_list()
        if not sessions_list or (sessions_list and session not in sessions_list):
            return await inter.response.send_message(
                embed=disnake.Embed(
                    title="ОШИБКА",
                    description="Указанного вами названия нету в списке сессий!",
                    color=disnake.Color.red(),
                ),
                ephemeral=True,
            )
        value = await database.delete_session(session)
        embed = disnake.Embed(
            title="УСПЕХ",
            description="Указанная вами сессия успешно удалена!",
            color=disnake.Color.green(),
        )
        if value:
            embed.add_field(
                name="ВАЖНО",
                value="```Указанная вами сессия использовалась как активная, вам нужно создать новую сессию для продолжения работы!```",
            )
        await inter.response.send_message(embed=embed, ephemeral=True)


def setup(bot: commands.Bot):
    bot.add_cog(DeleteSession(bot))
    print(f">{__name__} is launched")
