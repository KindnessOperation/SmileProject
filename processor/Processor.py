from PIL import Image, ImageFont, ImageDraw
import requests
import io
import textwrap
import logging

logger = logging.getLogger("processor")
logger.setLevel(logging.INFO)

def getEmojiMask(font: ImageFont, emoji: str, size: tuple[int, int]) -> Image:
    """ Makes an image with an emoji using AppleColorEmoji.ttf, this can then be pasted onto the image to show emojis
    
    Parameter:
    (ImageFont)font: The font with the emojis (AppleColorEmoji.ttf); Passed in so font is only loaded once
    (str)emoji: The unicoded emoji
    (tuple[int, int])size: The size of the mask
    
    Returns:
    (Image): A transparent image with the emoji
    
    """

    mask = Image.new("RGBA", (160, 160), color=(255, 255, 255, 0))
    draw = ImageDraw.Draw(mask)
    draw.text((0, 0), emoji, font=font, embedded_color=True)
    mask = mask.resize(size)

    return mask

def getDimensions(draw: ImageDraw, text: str, font: ImageFont) -> tuple[int, int]:
    """ Gets the size of text using the font
    
    Parameters:
    (ImageDraw): The draw object of the image
    (str)text: The text you are getting the size of
    (ImageFont)font: The font being used in drawing the text
    
    Returns:
    (tuple[int, int]): The width and height of the text
    
    """
    left, top, right, bottom = draw.multiline_textbbox((0, 0), text, font=font)
    return (right-left), (bottom-top)

def createPostImage(response: str, backgroundURI: str) -> Image.Image:
    """ Creates a post with the response to be uploaded to Instagram 
    
    Parameters:
    (str)response: The raw response from the google form
    (str)backgroundURI: The URI for the background photo
    
    Returns:
    (Image.Image): The processed image

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
    response = "\n".join(["\n".join(textwrap.wrap(subtext, width=70)) for subtext in response.split("\n")]) # Response is separated by newlines so it doesn't run off the screen
    poppinsFont = ImageFont.truetype("./fonts/Poppins-Regular.ttf", 25)
    dancingScriptFont = ImageFont.truetype("./fonts/DancingScript.ttf", 55)
    emojiFont = ImageFont.truetype(r"./fonts/AppleColorEmoji.ttf", 137)
    DANCINGHEIGHT = 50 # The height of the font is 50px since the text doesn't change
    PADDING = 80 # Padding between the two parts of text

    _, poppinsHeight = getDimensions(draw, response, poppinsFont)

    marginHeight = (1080 - (poppinsHeight + PADDING + DANCINGHEIGHT)) / 2 # [ Total height of image (1080) - PADDING (80) - content height of both pieces of text ] /2

    # Add the Dancing Script text first

    draw.text((50, marginHeight), "Make someone smile; Say something kind:", fill=(255, 255, 255), font=dancingScriptFont)
    draw.text((51, marginHeight), "Make someone smile; Say something kind:", fill=(255, 255, 255), font=dancingScriptFont) # Makes it a little bolder since the bold font is not supported by PIL
    logger.debug("Added dancing script font text")

    # Now add the response
    modifiedResponse = "".join(filter(lambda x: not (u"\uFE00" <= x <= "\uFE0F"), response)) # Filter through variation selectors
    draw.text((75, marginHeight+PADDING), modifiedResponse, fill=(255, 255, 255), font=poppinsFont)
    logger.debug("Added the response")

    # Now add any emojis that weren't embedded correctly
    responseL = response.split("\n")
    for i, line in enumerate(responseL):
        for j, char in enumerate(line):
            if (not char.isascii()):


                # Get variation selector if possible
                if (j+1 != len(line) and not (var_selector := line[j+1]).isascii() and u"\uFE00" <= var_selector <= "\uFE0F"): # Checks if next char is unicode and in var selector range
                    char += var_selector
                
                # If the current char is a var selector, ignore
                if (u"\uFE00" <= char <= "\uFE0F"): continue

                # Get the height of the text ABOVE the emoji in modifiedResponse
                aboveText = "\n".join(responseL[:i])
                _, aboveTextHeight = getDimensions(draw, aboveText, poppinsFont)

                # The height that we paste at is aboveTextHeight + (marginHeight+PADDING) + (Some error)
                # (marginHeight+PADDING) is where we pasted the entire paragraph
                y = aboveTextHeight + (marginHeight+PADDING) + 7

                # Get the length of the text on the line up to the emoji
                beforeLength, _ = getDimensions(draw, line[:j], poppinsFont)

                # The x position is beforeLength + 75; 75px is where we pasted the entire paragraph
                x = (75) + beforeLength

                # Create the mask
                emojiMask = getEmojiMask(emojiFont, char, (30, 30))

                # Paste the mask onto the image
                img.paste(emojiMask, (int(x), int(y)), emojiMask)

    return img



if __name__ == "__main__":
    createPostImage("""Sebbyyy Matoess you are so sweet and thoughtful, I'm so glad that I got to meet you at school. You give me a good start to my day at school and always cheer me up when I'm down, ilyyy \u2764\ufe0f""",
                    "https://images.unsplash.com/photo-1615839377917-bc950e77a6d1?ixid=M3w1ODU1ODV8MHwxfHJhbmRvbXx8fHx8fHx8fDE3MTI4NTQ0NDd8&ixlib=rb-4.0.3?w=1080&h=1080&fit=crop").show()
    # emojiFont = ImageFont.truetype(r"fonts\AppleColorEmoji.ttf", 137)
    # getEmojiMask(emojiFont, "\U0001f602", (100, 100)).show()
