import disnake
from disnake.ext import commands
from utils import database, checks, logs


class ReplenishBalance(commands.Cog):
    def __init__(self, bot: disnake.ext.commands.Bot):
        self.bot = bot

    @commands.slash_command(
        guild_only=True,
        name="пополнить-баланс",
        description="Пополнить баланс пользователя || Для кассира",
    )
    async def replenish_balance(
        self,
        inter: disnake.ApplicationCommandInteraction,
        *,
        member: disnake.Member = commands.Param(
            name="игрок", description="Игрок баланс которого вы хотите пополнить"
        ),
        value: int = commands.Param(
            name="значение",
            description="Количество фишек, которое вы хотите добавить на счёт",
        ),
    ):
        if not await checks.is_admin(inter=inter) and not await checks.is_cashier(
            inter=inter
        ):
            return await inter.response.send_message(
                embed=disnake.Embed(
                    title="ОШИБКА",
                    description="Вы должны быть кассиром или администратором для использования данной команды!",
                    color=disnake.Color.red(),
                ),
                ephemeral=True,
            )
        current_session = await database.get_current_session_name()
        if not current_session:
            return await inter.response.send_message(
                embed=disnake.Embed(
                    title="ОШИБКА",
                    description="Активная сессия не установлена!",
                    color=disnake.Color.red(),
                ),
                ephemeral=True,
            )
        if value == 0:
            return await inter.response.send_message(
                embed=disnake.Embed(
                    title="ОШИБКА",
                    description="Вы не можете пополнить баланс на 0 фишек!",
                    color=disnake.Color.red(),
                ),
                ephemeral=True,
            )
        if value < 0:
            return await inter.response.send_message(
                embed=disnake.Embed(
                    title="ОШИБКА",
                    description="Вы не можете вводить отрицательное число!",
                    color=disnake.Color.red(),
                ),
                ephemeral=True,
            )
        await database.replenish_balance(
            discord_id=member.id, session_name=current_session, value=value
        )
        current_balance = await database.get_user_balance(
            discord_id=member.id, session_name=current_session
        )
        await inter.response.send_message(
            embed=disnake.Embed(
                title="УСПЕХ",
                description="Баланс пользователя пополнен!\n\n"
                f"**Текущий баланс пользователя:** `{current_balance}`",
                color=disnake.Color.green(),
            ),
            ephemeral=True,
        )
        await logs.replenish_balance_log(
            balance_before=current_balance - value,
            balance_after=current_balance,
            count=value,
            session_name=current_session,
            inter=inter,
            target_user=member,
        )


def setup(bot: commands.Bot):
    bot.add_cog(ReplenishBalance(bot))
    print(f">{__name__} is launched")
