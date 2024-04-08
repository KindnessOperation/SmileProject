import discord
from discord.ext import commands
import json
import processor
from instagram import Instagram
import logging
import aiohttp
import aiofiles
import asyncio

CONFIG = None
with open("./config.json", "r") as f:
    CONFIG = json.load(f)

basic_config = logging.basicConfig(filename="logs/bot.log", 
    format="%(name)s - %(asctime)s-%(levelname)s:%(message)s", 
    datefmt="%X")
logger = logging.getLogger("bot")
logger.setLevel(logging.DEBUG)

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
bot.POSTPATH = "./images/post.png"
bot.VERIFYPATH = "./images/verify.png" # Path to store the processed image
bot.FLOWERURI = "https://cdn.discordapp.com/attachments/891493636611641345/1224211649288867870/IMG_9125.jpg?ex=661caaf1&is=660a35f1&hm=d1e2fa5fff66b33b0327bb81e1b973134f3a9935f2bd60776433484c72b5a51d&"
bot.ig = None

@bot.event
async def on_ready() -> None:
    logger.info(f"{bot.user.name} is ready!")
    print(f"{bot.user.name} is ready!")
    bot.verifyChannel = bot.get_channel(CONFIG['channels']['verify'])
    bot.successChannel = bot.get_channel(CONFIG['channels']['success'])
    
    bot.ig = Instagram(CONFIG['instagram']['username'], CONFIG['instagram']['password'])

@bot.event
async def on_message(message: discord.Message) -> None:

    if (message.webhook_id):
        await message.add_reaction("\u2705") # U+2705 is a white check mark
        logger.info("New Response - %s" % (message.embeds[0].description))

    await bot.process_commands(message)



async def sendVerifyMessage(response: str) -> None:
    """ Sends the embed with image to be verified """
    unsplash = processor.Unsplash(CONFIG['unsplashAccessToken'])
    imgURI = unsplash.getRandomImage(query="flower")
    img = processor.createPostImage(response, imgURI)
    img.save(bot.VERIFYPATH) # In the future make an io buffer but the code already works so leave it

    # Send in verified channel to make sure that the generated image is appropriate
    embed = discord.Embed(color=discord.Color.green(), 
        title="Upload Post?", 
        description=response
        )
    file = discord.File(fp=bot.VERIFYPATH, filename="verify.png")
    embed.set_image(url="attachment://verify.png")
    embed.set_author(
        name="Smile Project", 
        icon_url=bot.FLOWERURI
    )

    msg = await bot.verifyChannel.send(file=file, embed=embed)
    await msg.add_reaction("\u2705") # Check
    await msg.add_reaction("\u274C") # X

@bot.event
async def on_reaction_add(reaction: discord.Reaction, user: discord.Member) -> None:
    # Ensure user is reacting to a message sent by a bot/webhook and the bot isn't the one reacting
    if ((not reaction.message.webhook_id and not reaction.message.author.bot) or user.bot):
        return
    
    channelId = reaction.message.channel.id
    response = reaction.message.embeds[0].description # The description of the embed is the response

    # If the message has 2 other reactions; The response is sent to the verify channel
    if (channelId == CONFIG['channels']['responses']): # Responses Channel

        # If the message isn't a check, then return
        if (reaction.emoji == "\u2705" and reaction.count == 3): pass
        elif (reaction.emoji == "\u2764" and reaction.count == 1): pass
        else: return
        


        logger.info("Reaction minimum met - Moving to verified step: %s" % (response))
        await reaction.message.delete()
        await sendVerifyMessage(response)
    
    # After the message has been approved by responses, we move on to approve the background image in #verify
    elif (channelId == CONFIG['channels']['verify']): # Verify Channel
        if (reaction.emoji == "\u2705"): # If it's a check, upload
            logger.info("Uploading response to Instagram: %s" % response)


            # Save the image from the embed to bot.POSTPATH
            # Quality isn't downgraded that much and makes the code a lot more simpler
            imageURI = reaction.message.embeds[0].image.url
            async with aiohttp.ClientSession() as sess:
                async with sess.get(imageURI) as req:
                    async with aiofiles.open(bot.POSTPATH, "wb") as f:
                        async for data, _ in req.content.iter_chunks():
                            await f.write(data)

            # Upload to instagram
            loop = asyncio.get_event_loop()
            loop.run_in_executor(None, bot.ig.uploadPost, bot.POSTPATH)


            # Post in success
            await reaction.message.delete()
            await bot.successChannel.send(file=discord.File(fp=bot.POSTPATH, filename="post.png"))
        
        elif (reaction.emoji == "\u274C"): # If it's an X, reroll
            logger.info("Rerolling post - %s" % response)
            await reaction.message.delete() # Delete old msg
            await sendVerifyMessage(response)



bot.run(CONFIG['discordToken'])