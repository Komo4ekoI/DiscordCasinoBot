import disnake
from disnake.ext import commands
from utils import database, checks, logs


class WithdrawnBalance(commands.Cog):
    def __init__(self, bot: disnake.ext.commands.Bot):
        self.bot = bot

    @commands.slash_command(
        guild_only=True, name="вывести-со-счёта", description="Вывести фишки со счёта || Для кассира"
    )
    async def withdraw_balance(
        self,
        inter: disnake.ApplicationCommandInteraction,
        member: disnake.Member = commands.Param(
            name="игрок",
            description="Игрок, с баланса которого вы хотите снять фишки",
        ),
        value: int = commands.Param(
            name="значение",
            description="Количество фишек, которое вы хотите снять со счёт",
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
        old_balance = await database.get_user_balance(
            session_name=current_session, discord_id=member.id
        )
        if old_balance is None:
            return await inter.response.send_message(
                embed=disnake.Embed(
                    title="ОШИБКА",
                    description="Пользователя нет в активной сессии!",
                    color=disnake.Color.red(),
                ),
                ephemeral=True,
            )
        if value == 0:
            return await inter.response.send_message(
                embed=disnake.Embed(
                    title="ОШИБКА",
                    description="Вы не можете снять 0 фишек!",
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
        if old_balance - value < 0:
            return await inter.response.send_message(
                embed=disnake.Embed(
                    title="ОШИБКА",
                    description="У пользователя недостаточно фишек для снятия!\n\n"
                    f"**Текущий баланс пользователя:** `{old_balance}`",
                    color=disnake.Color.red(),
                ),
                ephemeral=True,
            )
        await database.withdraw(
            session_name=current_session, discord_id=member.id, value=value
        )
        current_balance = await database.get_user_balance(
            session_name=current_session, discord_id=member.id
        )
        await inter.response.send_message(
            embed=disnake.Embed(
                title="УСПЕХ",
                description="Фишки успешно сняты!\n\n"
                f"**Баланс до снятия:** `{old_balance}`\n"
                f"**Текущий баланс:** `{current_balance}`",
                color=disnake.Color.orange(),
            ),
            ephemeral=True,
        )
        await logs.withdraw_balance_log(
            balance_before=old_balance,
            balance_after=current_balance,
            count=value,
            session_name=current_session,
            inter=inter,
            target_user=member,
        )


def setup(bot: commands.Bot):
    bot.add_cog(WithdrawnBalance(bot))
    print(f">{__name__} is launched")
