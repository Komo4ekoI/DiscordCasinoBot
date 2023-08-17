import disnake
from disnake.ext import commands
from utils import database, checks, logs


class ChangeBalance(commands.Cog):
    def __init__(self, bot: disnake.ext.commands.Bot):
        self.bot = bot

    @commands.slash_command(
        guild_only=True,
        name="изменить-баланс",
        description="Изменить баланс пользователя || Для крупье"
        " Укажите отрицательное или положительное число!",
    )
    async def change_balance(
        self,
        inter: disnake.ApplicationCommandInteraction,
        *,
        member: disnake.Member = commands.param(
            name="игрок", description="Игрок баланс которого вы хотите изменить"
        ),
        value: int = commands.Param(
            name="значение",
            description="Значение, на сколько вы хотите изменить баланс относительно нынешнего баланса",
        ),
    ):
        if not await checks.is_admin(inter=inter) and not await checks.is_croupier(
            inter=inter
        ):
            return await inter.response.send_message(
                embed=disnake.Embed(
                    title="ОШИБКА",
                    description="Вы должны быть крупье или администратором для использования данной команды!",
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
        if not await database.check_session_member(
            session_name=current_session, discord_id=member.id
        ):
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
                    description="Вы не можете изменить баланс на 0 фишек!",
                    color=disnake.Color.red(),
                ),
                ephemeral=True,
            )
        old_balance = await database.get_user_balance(
            session_name=current_session, discord_id=member.id
        )
        if value < 0 and old_balance - abs(value) < 0:
            return await inter.response.send_message(
                embed=disnake.Embed(
                    title="ОШИБКА",
                    description="У пользователя не может быть минусового баланса!\n"
                    f"Текущий баланс пользователя: `{old_balance}`",
                    color=disnake.Color.red(),
                ),
                ephemeral=True,
            )
        await database.change_user_balance(
            discord_id=member.id, session_name=current_session, value=value
        )
        new_balance = await database.get_user_balance(
            session_name=current_session, discord_id=member.id
        )
        embed = disnake.Embed(
            title="УСПЕХ",
            description="Баланс пользователя изменён!\n\n"
            f"**Баланс до изменения:** `{old_balance}`\n"
            f"**Баланс после изменения:** `{new_balance}`",
            color=disnake.Color.green(),
        )
        if old_balance > new_balance:
            embed.color = disnake.Color.orange()
        await inter.response.send_message(embed=embed, ephemeral=True)
        await logs.change_balance_log(
            balance_before=old_balance,
            balance_after=new_balance,
            count=value,
            session_name=current_session,
            inter=inter,
            target_user=member,
        )


def setup(bot: commands.Bot):
    bot.add_cog(ChangeBalance(bot))
    print(f">{__name__} is launched")
