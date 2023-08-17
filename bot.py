from disnake.ext import commands
import disnake

owners = [302065849722732544]


class CasinoBot(commands.Bot):
    @classmethod
    def create(cls) -> "CasinoBot":
        return cls(
            owner_ids=set(owners),
            status=disnake.Status.online,
            intents=disnake.Intents.all(),
            command_prefix="!",
            allowed_mentions=disnake.AllowedMentions(),
            activity=disnake.Game("казино!"),
            description="BeeTools",
        )

    async def on_ready(self):
        print(f"Logged in as {self.user.name}")
