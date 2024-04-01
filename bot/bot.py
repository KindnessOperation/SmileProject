import discord
from discord.ext import commands
import json

CONFIG = None

with open("./config.json", "r") as f:
    CONFIG = json.load(f)

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready() -> None:
    print(f"{bot.user.name} is ready!")


@bot.event
async def on_message(message: discord.Message) -> None:
    if (message.webhook_id):
        await message.add_reaction("\u2705") # U+2705 is a white check mark

    await bot.process_commands(message)



bot.run(CONFIG['discordToken'])