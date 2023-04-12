import discord
from discord import app_commands
import json
import logging

with open("config.json", "r") as file:
    TOKEN = json.load(file)["token"]

MY_GUILD = discord.Object(id=1092498525536919643)

class ChessClient(discord.Client):
    def __init__(self, *, intents: discord.Intents=None):
        super().__init__(intents=(intents or discord.Intents.default()))

        self.tree = app_commands.CommandTree(self)

        self.games = []

    async def setup_hook(self) -> None:
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)


client = ChessClient()

@client.event
async def on_ready():
    print(f"yoooooo logged on as {client.user} ({client.user.id})")

@client.tree.command()
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"**Pong!** ({client.latency * 1000:.2f})ms")

@client.tree.command(name="new-game")
async def game(interaction: discord.Interaction, other: discord.Member):
    pass

client.run(TOKEN, log_level=logging.DEBUG)