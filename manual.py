import discord
import json
import datetime

CONFIG = None
with open("./config.json") as f:
    CONFIG = json.load(f)

FLOWERURI = "https://cdn.discordapp.com/attachments/891493636611641345/1224211649288867870/IMG_9125.jpg?ex=661caaf1&is=660a35f1&hm=d1e2fa5fff66b33b0327bb81e1b973134f3a9935f2bd60776433484c72b5a51d&"
webhook = discord.SyncWebhook.from_url(CONFIG['webhook'])

while True:
    embed = discord.Embed(color=discord.Color.blue(), title="New Response", description=input("Response: "))
    embed.set_author(
        name="LOLHS"
    )
    embed.set_footer(
        text="Smile Project",
        icon_url=FLOWERURI
    )
    embed.timestamp = datetime.datetime.now(datetime.UTC)

    webhook.send(embed=embed, username="Smile Project", avatar_url=FLOWERURI)
