import json
from form import Form
import time
import discord
import logging
import threading
import datetime
import traceback
import random

basic_config = logging.basicConfig(filename="logs/main.log", 
    format="%(name)s-%(asctime)s-%(levelname)s:%(message)s", 
    datefmt="%X")
logger = logging.getLogger("main")
logger.setLevel(logging.DEBUG)

console = logging.StreamHandler() # sys.stderr
console.setLevel(logging.WARNING)
logging.getLogger().addHandler(console)

CONFIG = None
with open("./config/config.json", "r") as f:
    CONFIG = json.load(f)


class SmileProject:
    def __init__(self, formId: str, webhookURL: str, school: str) -> None:
        self.formId = formId
        self.responses = Form(self.formId).getResponse_pks()
        self.webhook = discord.SyncWebhook.from_url(webhookURL)
        self.school = school
        self.FLOWERURI = "https://cdn.discordapp.com/attachments/891493636611641345/1224211649288867870/IMG_9125.jpg?ex=661caaf1&is=660a35f1&hm=d1e2fa5fff66b33b0327bb81e1b973134f3a9935f2bd60776433484c72b5a51d&"

    def send_error_webhook(self, exception: Exception) -> None:

        embed = discord.Embed(title="⚠️ Exception Occurred  Retrieving Responses", color=discord.Color.red())
        embed.add_field(name="Type", value=f"`{type(exception)}`", inline=False)
        embed.add_field(name="Message", value=f"`{exception}`", inline=False)
        tb_text = "".join(traceback.format_tb(exception.__traceback__))
        embed.add_field(name="Traceback", value=f"```{tb_text[-1000:]}```", inline=False)  # Truncate to avoid Discord limit

        self.webhook.send(embed=embed, username="Smile Project", avatar_url=self.FLOWERURI)

        logging.error(exception)


    def loop(self) -> None:
        try:
            form = Form(self.formId)
            responses = form.getResponses()
        except Exception as e:
            self.send_error_webhook(e)
            return
        
        for response_pk, response in responses:
            if (response_pk not in self.responses): # New response!
                logger.info("New Response @ %s - %s - %s" % (self.school, response_pk, response))
                self.responses.append(response_pk) # Add the new pk

                embed = discord.Embed(color=discord.Color.blue(), title="New Response", description=response)
                embed.set_author(
                    name=self.school
                )
                embed.set_footer(
                    text="Smile Project",
                    icon_url=self.FLOWERURI
                )
                embed.timestamp = datetime.datetime.now(datetime.UTC)
                
                self.webhook.send(embed=embed, username="Smile Project", avatar_url=self.FLOWERURI)
                logger.info("Webhook sent")
    
    def startLoop(self) -> None:
        consecutive_failures = 0
        MAX_BACKOFF = 300  # 5 minutes cap
        while True:
            try:
                self.loop()
                consecutive_failures = 0
                time.sleep(20)
            except Exception as e:
                consecutive_failures += 1
                backoff = min(MAX_BACKOFF, (2 ** consecutive_failures))
                jitter = random.uniform(0, backoff * 0.5)
                sleep_time = backoff + jitter
                logger.error(
                    "Thread %s crashed (attempt %d), retrying in %.1fs: %s",
                    self.school, consecutive_failures, sleep_time, e
                )
                time.sleep(sleep_time)



if __name__ == "__main__":
    threads: list[threading.Thread] = []

    for school, data in CONFIG['accounts'].items():
        sp = SmileProject(
            data['formId'], 
            data['webhook'], 
            school
        )
        thread = threading.Thread(None, sp.startLoop, daemon=True)
        thread.start()
        threads.append(thread)

    while True: time.sleep(100) # Sleep forever


