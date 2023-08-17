import disnake
from disnake.ext import commands
from utils import database, autocompletes, checks


class CheckUserBalance(commands.Cog):
    def __init__(self, bot: disnake.ext.commands.Bot):
        self.bot = bot

    @commands.slash_command(
        guild_only=True,
        name="проверить-баланс",
        description="Показывает информацию о том, "
        "сколько алмазов было Пополнено | Текущий баланс| Снято",
    )
    async def check_balance(
        self,
        inter: disnake.ApplicationCommandInteraction,
        member: disnake.Member = commands.Param(
            name="игрок", description="Игрок, баланс которого вы хотите пополнить"
        ),
        session: str = commands.Param(
            default=None,
            autocomplete=autocompletes.sessions_autocompleter,
            name="сессия",
            description="Сессия за которую вы хотите посмотреть данные",
        ),
    ):
        if (
            not await checks.is_admin(inter=inter)
            and not await checks.is_croupier(inter=inter)
            and not await checks.is_cashier(inter=inter)
        ):
            return await inter.response.send_message(
                embed=disnake.Embed(
                    title="ОШИБКА",
                    description="Вы должны быть сотрудником казино для использования данный команды!",
                    color=disnake.Color.red(),
                ),
                ephemeral=True,
            )
        current_session = False
        if session is None:
            session = await database.get_current_session_name()
            current_session = True
            if session is None:
                await inter.response.send_message(
                    embed=disnake.Embed(
                        title="ОШИБКА",
                        description="Активная сессия не установлена, укажите сессию вручную!",
                        color=disnake.Color.red(),
                    ),
                    ephemeral=True,
                )
        else:
            sessions_list = await database.get_sessions_list()
            if not sessions_list or (sessions_list and session not in sessions_list):
                return await inter.response.send_message(
                    embed=disnake.Embed(
                        title="ОШИБКА",
                        description="Указанного вами названия сессии нету в списке сессий!",
                        color=disnake.Color.red(),
                    ),
                    ephemeral=True,
                )
        balance = await database.get_user_balance(
            session_name=session, discord_id=member.id
        )
        if balance is None:
            if current_session:
                description = "Пользователя нету в активной сессии!"
            else:
                description = "Пользователя нету в указанной вами сессией!"
            return await inter.response.send_message(
                embed=disnake.Embed(
                    title="ОШИБКА", description=description, color=disnake.Color.red()
                ),
                ephemeral=True,
            )
        topped_balance = await database.get_topped_balance(
            discord_id=member.id, session_name=session
        )
        withdraw_balance = await database.get_withdrawn_balance(
            discord_id=member.id, session_name=session
        )
        description = (
            f"Пользователь: {member.mention}\n\n"
            f"**Информация за сессию:** `{session}`\n\n"
            f"**Пополнил баланс на:** `{topped_balance} фишек`\n"
            f"**Текущий баланс:** `{balance} фишек`\n"
        )
        if withdraw_balance == 0:
            description += "**Пользователь не выводил средства!**"
        else:
            description += f"**Снял:** `{withdraw_balance} фишек`"
        embed = disnake.Embed(
            title="ИНФОРМАЦИЯ", description=description, color=disnake.Color.yellow()
        )
        await inter.response.send_message(embed=embed, ephemeral=True)


def setup(bot: commands.Bot):
    bot.add_cog(CheckUserBalance(bot))
    print(f">{__name__} is launched")
