from PIL import Image, ImageFont, ImageDraw
import requests
import io
import textwrap
import logging

logger = logging.getLogger("processor")
logger.setLevel(logging.INFO)
def createPostImage(response: str, backgroundURI: str) -> Image.Image:
    """ Creates a post with the response to be uploaded to Instagram 
    
    Parameters:
    (str)response: The raw response from the google form
    (str)backgroundURI: The URI for the background photo
    
    Returns:
    (Image): The processed image

    """
    logger.info("Creating post image")

    resp = requests.get(backgroundURI) # Get the image
    img = Image.open(io.BytesIO((resp.content)))
    logger.debug("Set background image")

    # Make the image dimmer
    mask = Image.new("RGBA", img.size, (0, 0, 0, 160))
    img.paste(mask, (0, 0), mask)
    logger.debug("Dimming background with mask")

    # Make draw object
    draw = ImageDraw.Draw(img)

    modifiedResponse = "\n".join(textwrap.wrap(response, width=90)) # Response is separated by newlines so it doesn't run off the screen
    poppinsFont = ImageFont.truetype(r"C:\Users\austi\Downloads\code\py\SmileProject\fonts\Poppins-Regular.ttf", 20)
    dancingScriptFont = ImageFont.truetype("./fonts/DancingScript.ttf", 50)
    DANCINGHEIGHT = 50 # The height of the font is 50px since the text doesn't change
    PADDING = 80 # Padding between the two parts of text

    left, top, right, bottom = poppinsFont.getbbox(modifiedResponse)
    # length = right - left
    poppinsHeight = bottom - top # Height of the response in px

    marginHeight = (1080 - (poppinsHeight + PADDING + 50)) / 2 # [ Total height of image (1080) - PADDING (80) - content height of both pieces of text ] /2


    # Add the Dancing Script text first

    draw.text((50, marginHeight), "Make someone smile; Say something kind:", fill=(255, 255, 255), font=dancingScriptFont)
    draw.text((51, marginHeight), "Make someone smile; Say something kind:", fill=(255, 255, 255), font=dancingScriptFont) # Makes it a little bolder since the bold font is not supported by PIL
    logger.debug("Added dancing script font text")


    # Now add the response
    draw.text((75, marginHeight+PADDING), modifiedResponse, fill=(255, 255, 255), font=poppinsFont)
    logger.debug("Added the response")

    return img



if __name__ == "__main__":
    createPostImage("You are loved and I hope you had a very happy day indeed. Spring break was very fun and I hope you enjoyed it!",
                    "https://images.unsplash.com/photo-1678791564760-725c8798f458?ixid=M3w1ODU1ODV8MHwxfHJhbmRvbXx8fHx8fHx8fDE3MTE5MzE1NDZ8&ixlib=rb-4.0.3?w=1080&h=1080&fit=crop")