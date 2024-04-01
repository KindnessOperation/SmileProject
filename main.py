import json
from form import Form
import processor
from instagram import Instagram
import time
CONFIG = None
with open("./config.json", "r") as f:
    CONFIG = json.load(f)


class SmileProject:
    def __init__(self, formId: str, unsplashAccessToken: str, igUser: str, igPwd: str) -> None:
        self.PATH = "./images/post.png" # Path to store the processed image
        self.formId = formId
        self.responses = Form(self.formId).getResponse_pks()
        self.unsplashAccessToken = unsplashAccessToken
        self.igUser, self.igPwd = igUser, igPwd


    def loop(self) -> None:
        form = Form(self.formId)
        unsplash = processor.Unsplash(self.unsplashAccessToken)
        # ig = Instagram(self.igUser, self.igPwd)
        responses = form.getResponses()
        for response_pk, response in responses:
            if (response_pk not in self.responses): # New response!
                print(response_pk)
                self.responses.append(response_pk) # Add the new pk

                imgURI = unsplash.getRandomImage(query="flower")
                img = processor.createPostImage(response, imgURI)

                img.save(self.PATH)
                # ig.uploadPost(self.PATH)



if __name__ == "__main__":
    sp = SmileProject(
        CONFIG['formId'], 
        CONFIG['unsplashAccessToken'],
        CONFIG['instagram']['username'],
        CONFIG['instagram']['password']
    )
    while True:
        sp.loop()
        time.sleep(5)



