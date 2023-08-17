import disnake
from disnake.ext import commands
from utils import database, checks


class Test(commands.Cog):
    def __init__(self, bot: disnake.ext.commands.Bot):
        self.bot = bot

    # @commands.slash_command(guild_only=True)
    # async def test(self, inter: disnake.ApplicationCommandInteraction):
    #     await checks.is_role(inter=inter, role_id=1141708330709037126)


def setup(bot: commands.Bot):
    bot.add_cog(Test(bot))
    print(f">{__name__} is launched")
