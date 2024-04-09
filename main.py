import json
from form import Form
import time
import discord
import logging
import threading


basic_config = logging.basicConfig(filename="logs/main.log", 
    format="%(name)s-%(asctime)s-%(levelname)s:%(message)s", 
    datefmt="%X")
logger = logging.getLogger("main")
logger.setLevel(logging.DEBUG)

CONFIG = None
with open("./config.json", "r") as f:
    CONFIG = json.load(f)


class SmileProject:
    def __init__(self, formId: str, webhookURL: str, school: str) -> None:
        self.formId = formId
        self.responses = Form(self.formId).getResponse_pks()
        self.webhook = discord.SyncWebhook.from_url(webhookURL)
        self.school = school
        self.FLOWERURI = "https://cdn.discordapp.com/attachments/891493636611641345/1224211649288867870/IMG_9125.jpg?ex=661caaf1&is=660a35f1&hm=d1e2fa5fff66b33b0327bb81e1b973134f3a9935f2bd60776433484c72b5a51d&"


    def loop(self) -> None:
        form = Form(self.formId)
        responses = form.getResponses()
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
                
                self.webhook.send(embed=embed, username="Smile Project", avatar_url=self.FLOWERURI)
                logger.info("Webhook sent")
    
    def startLoop(self) -> None:
        while True:
            sp.loop()
            time.sleep(5)



if __name__ == "__main__":
    threads: list[threading.Thread] = []

    for school, data in CONFIG['accounts'].items(): 
        sp = SmileProject(
            data['formId'], 
            CONFIG['webhook'], # Global
            school
        )
        thread = threading.Thread(None, sp.startLoop)
        thread.start()
        threads.append(thread)

    for thread in threads: # Blocks the program to allow threads to work
        thread.join()


